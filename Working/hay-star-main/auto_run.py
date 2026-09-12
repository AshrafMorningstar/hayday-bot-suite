#!/usr/bin/env python3
"""
=============================================================================
Hay Star Fully Autonomous Master Runner (Zero-Interaction Mode)
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Fully automated pipeline executing the complete suite end-to-end:
1. Automatically prepares and stages ALL 10 Mods into Hay Day assets.
2. Detects LDPlayer 9 and connects via ADB.
3. Spawns hay-star.exe native loader and attaches to com.supercell.hayday.
4. Executes continuous 13-subsystem automation passes across all accounts.
5. Self-heals crashes with diagnostic dumps (screenshot, logcat, tombstones).
=============================================================================
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = Colors.CYAN if level == "INFO" else Colors.GREEN if level == "SUCCESS" else Colors.YELLOW if level == "WARN" else Colors.RED
    print(f"{color}[{timestamp}] [{level}] {msg}{Colors.RESET}")

def main():
    print(f"""
{Colors.CYAN}{Colors.BOLD}=============================================================================
       🌾 HAY STAR FULLY AUTONOMOUS MASTER RUNNER (AUTO MODE) 🌾
         Created by Ashraf Morningstar | Zero-Interaction Pipeline
============================================================================={Colors.RESET}
""")

    import mod_manager
    from supervisor import SupervisorEngine

    # 1. Automatically stage ALL MODS
    log("Step 1/3: Preparing and staging ALL 10 Game Asset Mods...", "INFO")
    try:
        stage_res = mod_manager.prepare_stage_directory(["A"])
        log(f"Mod assets prepared with valid SHA-1 fingerprint at: {stage_res}", "SUCCESS")
    except Exception as e:
        log(f"Mod staging warning: {e}", "WARN")

    # 2. Check and wait for emulator
    log("Step 2/3: Connecting to LDPlayer 9 emulator via ADB...", "INFO")
    adb = mod_manager.locate_adb()
    
    # Try connecting to standard LDPlayer ports safely
    import socket
    for port in [5555, 5554, 5556, 5558, 62001, 7555]:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            if s.connect_ex(('127.0.0.1', port)) == 0:
                subprocess.run([adb, "connect", f"127.0.0.1:{port}"], capture_output=True, timeout=3)
            s.close()
        except Exception:
            pass

    connected = False
    for attempt in range(1, 11):
        res = subprocess.run([adb, "devices"], capture_output=True, text=True)
        devices = [l.split()[0] for l in res.stdout.splitlines() if "\tdevice" in l]
        if devices:
            log(f"Connected to Android device: {devices[0]}", "SUCCESS")
            connected = True
            break
        log(f"Waiting for LDPlayer 9 ({attempt}/10)... If LDPlayer is closed, please start LDPlayer 9 on your desktop.", "WARN")
        # Try triggering start
        if attempt == 1 and os.path.exists(r"C:\LDPlayer\LDPlayer9\dnplayer.exe"):
            try:
                subprocess.Popen([r"C:\LDPlayer\LDPlayer9\dnplayer.exe"], shell=True)
            except Exception:
                pass
        time.sleep(3)

    if not connected:
        log("No active LDPlayer 9 detected yet. The supervisor watchdog will remain active and automatically attach the moment LDPlayer 9 starts!", "WARN")

    # 3. Launch the full multi-account autonomous supervisor
    log("Step 3/3: Handing over to Hay Star Autonomous Supervisor Engine...", "INFO")
    supervisor = SupervisorEngine()
    supervisor.run()

if __name__ == "__main__":
    main()
