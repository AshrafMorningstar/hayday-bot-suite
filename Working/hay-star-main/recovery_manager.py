#!/usr/bin/env python3
"""
=============================================================================
Hay Star Connection Recovery & Auto-Healing Manager
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Handles:
1. "Connection lost" / "Another device is connecting to this farm" popups:
   - Dismisses dialogs by tapping "Reload game" / "Okay" button via ADB.
2. Loading screen hangs / ANR / EMFILE crash recovery:
   - Detects when game is stuck on loading screen or killed.
   - Force-stops and cleanly relaunches com.supercell.hayday.
3. TCP control server & loadnative safety verification:
   - Re-checks port 31350 every 2-3 cycles.
   - Sends 'loadnative' to ensure ARM64 engine is live inside Hay Day.
4. Standalone CLI testing command 'rc' / 'reconnect' / 'auto_heal'.
=============================================================================
"""

import os
import sys
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# Windows UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent
PACKAGE_NAME = "com.supercell.hayday"
COMMON_ADB_PATHS = [
    r"C:\LDPlayer\LDPlayer9\adb.exe",
    r"D:\LDPlayer\LDPlayer9\adb.exe",
    r"C:\Program Files\LDPlayer\LDPlayer9\adb.exe",
    str(WORKSPACE_ROOT / "Assest" / "adb" / "adb.exe"),
    "adb"
]


class RecoveryManager:
    """Detects connection errors, dismisses popups, and heals the game pipeline."""

    def __init__(self, adb_path=None, host="127.0.0.1", port=31350):
        self.adb = adb_path or self.find_adb()
        self.host = host
        self.port = port
        self.last_heal_time = None
        self.heal_count = 0

    @staticmethod
    def find_adb():
        for p in COMMON_ADB_PATHS:
            if os.path.isfile(p):
                return p
        return "adb"

    def log(self, msg, level="INFO"):
        t = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "[*]",
            "OK": "[+]",
            "WARN": "[!]",
            "ERR": "[-]"
        }.get(level, "[*]")
        print(f"  {prefix} [{t}] [recovery] {msg}", flush=True)

    def get_online_device(self):
        """Returns the active ADB device identifier."""
        try:
            res = subprocess.run([self.adb, "devices"], capture_output=True, text=True, timeout=5)
            lines = [line.split("\t")[0].strip() for line in res.stdout.splitlines() if "\tdevice" in line]
            if lines:
                return lines[0]
            # Try connecting to LDPlayer default port
            subprocess.run([self.adb, "connect", "127.0.0.1:5555"], capture_output=True, timeout=3)
            return "127.0.0.1:5555"
        except Exception:
            return "127.0.0.1:5555"

    def run_adb(self, cmd_args, timeout=10):
        dev = self.get_online_device()
        cmd = [self.adb, "-s", dev] + cmd_args
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)

    def is_game_running(self):
        """Checks if com.supercell.hayday process is active."""
        try:
            res = self.run_adb(["shell", f"pidof {PACKAGE_NAME}"], timeout=5)
            return res.returncode == 0 and bool(res.stdout.strip())
        except Exception:
            return False

    def is_game_foreground(self):
        """Checks if com.supercell.hayday is the focused window."""
        try:
            res = self.run_adb(["shell", "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"], timeout=5)
            return PACKAGE_NAME in res.stdout
        except Exception:
            return False

    def dismiss_popups(self):
        """
        Detects and dismisses:
        - 'Another device is connecting to this farm.' (TID_ERROR_POP_UP_LOGGED_FROM_ANOTHER_DEVICE)
        - 'Connection lost' / 'Reload game' dialog
        - 'Load farm?' Supercell ID confirm dialog
        """
        self.log("Scanning screen for connection / reload popups...", "INFO")
        dev = self.get_online_device()

        # Coordinate set for 'Reload game' / 'Okay' / Center confirmation buttons
        # In LDPlayer 1280x720 (landscape):
        # Dialog confirm button is centered horizontally: x ~ 640, y ~ 460-520
        # In 960x540: x ~ 480, y ~ 360
        # In portrait: x ~ 360, y ~ 640
        popup_tap_coordinates = [
            (640, 480),  # Landscape 720p center reload button
            (640, 520),  # Landscape 720p lower dialog button
            (480, 360),  # 540p center
            (720, 540),  # 1080p center
            (640, 420),  # Error prompt center
        ]

        tapped = False
        try:
            # 1. Check and dismiss Google Sign-In (MinuteMaidActivity)
            focus_chk = self.run_adb(["shell", "dumpsys window | grep -E 'mCurrentFocus|mFocusedApp'"], timeout=4)
            if "MinuteMaidActivity" in focus_chk.stdout or "com.google.android.gms" in focus_chk.stdout:
                self.log("Detected Google Sign-In modal; force-stopping com.google.android.gms...", "WARN")
                self.run_adb(["shell", "am force-stop com.google.android.gms"], timeout=4)
                self.run_adb(["shell", f"am start -n {PACKAGE_NAME}/.GameApp"], timeout=4)
                self.run_adb(["shell", "input keyevent 4"], timeout=3)
                time.sleep(1.0)
                tapped = True

            # 2. Check logcat for recent connection loss / another device log
            logcat = self.run_adb(["shell", "logcat -d -t 30 | grep -iE 'another device|connection lost|reload'"], timeout=4)
            has_error_in_logcat = bool(logcat.stdout.strip())

            # Tap center button to dismiss any popup / scarecrow dialog
            for (x, y) in popup_tap_coordinates[:2]:
                self.run_adb(["shell", "input", "tap", str(x), str(y)], timeout=3)
                time.sleep(0.3)
                tapped = True

            if has_error_in_logcat:
                self.log("Detected connection loss in logcat; tapped Reload button.", "WARN")
                time.sleep(2.0)
            else:
                self.log("Popup tap check dispatched.", "OK")
        except Exception as e:
            self.log(f"Popup dismiss error: {e}", "WARN")

        return tapped

    def reload_game(self, wait_seconds=12):
        """Cleanly restarts Hay Day to clear loading screen hangs."""
        self.log("Restarting Hay Day to clear loading screen hang...", "WARN")
        try:
            self.run_adb(["shell", f"am force-stop {PACKAGE_NAME}"], timeout=5)
            time.sleep(1.5)
            self.run_adb(["shell", f"monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1"], timeout=6)
            self.log(f"Launched Hay Day; waiting {wait_seconds}s for game to load...", "INFO")
            time.sleep(wait_seconds)
            # Dismiss any startup prompt (e.g. Supercell ID notice)
            self.dismiss_popups()
            return True
        except Exception as e:
            self.log(f"Failed to reload game: {e}", "ERR")
            return False

    def test_tcp_control(self):
        """Verifies connection to hay-star control server (port 31350)."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((self.host, self.port))
            s.sendall(b"status\n")
            res = s.recv(1024).decode(errors="replace").strip()
            s.close()
            return bool(res and "OK" in res)
        except Exception:
            return False

    def ensure_native_engine_loaded(self):
        """Sends 'loadnative' command to port 31350 and verifies engine status."""
        self.log("Verifying native ARM64 engine status via TCP...", "INFO")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4.0)
            s.connect((self.host, self.port))
            s.sendall(b"status\n")
            res = s.recv(1024).decode(errors="replace").strip()
            
            # If gate is down, send loadnative
            if "gate=down" in res or "loadnative" not in res:
                self.log("Gate is down. Sending 'loadnative' to stage libmstar.so...", "INFO")
                s.sendall(b"loadnative\n")
                time.sleep(1.0)
                native_res = s.recv(1024).decode(errors="replace").strip()
                self.log(f"Native engine response: {native_res}", "OK")
            else:
                self.log(f"Native engine verified live: {res}", "OK")
            s.close()
            return True
        except Exception as e:
            self.log(f"TCP control communication failed: {e}", "WARN")
            return False

    def check_and_heal(self, force_reload=False):
        """
        Master auto-healing routine. Runs every 2-3 cycles.
        Checks:
        1. Emulator connection
        2. Game running & not stuck
        3. Dismisses connection / another device popups
        4. Reconnects TCP control & loads native engine if needed
        """
        self.heal_count += 1
        self.last_heal_time = datetime.now()
        self.log(f"=== Health Check #{self.heal_count} Starting ===", "INFO")

        # 1. Device check
        dev = self.get_online_device()
        self.log(f"Active emulator device: {dev}", "OK")

        # 2. Check game running
        running = self.is_game_running()
        if not running or force_reload:
            self.log("Hay Day is not running. Launching...", "WARN")
            self.reload_game(wait_seconds=12)
        else:
            # Dismiss any popups that may have appeared during play
            self.dismiss_popups()

        # 3. Check TCP control & native engine
        tcp_ok = self.test_tcp_control()
        if not tcp_ok:
            self.log("TCP control port 31350 is not responding.", "WARN")
            self.log("Tip: Ensure hay-star.exe is running in background.", "INFO")
        else:
            self.ensure_native_engine_loaded()

        self.log(f"=== Health Check #{self.heal_count} Complete ===\n", "OK")
        return True


# Standalone runner for testing: python recovery_manager.py
if __name__ == "__main__":
    mgr = RecoveryManager()
    print("============================================================")
    print("  HAY STAR CONNECTION RECOVERY & HEALTH CHECK")
    print("============================================================")
    mgr.check_and_heal()
