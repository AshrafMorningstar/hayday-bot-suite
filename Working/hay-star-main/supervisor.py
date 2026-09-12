#!/usr/bin/env python3
"""
=============================================================================
Hay Star Autonomous Supervisor & Watchdog Engine
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Hay Star Supervisor manages the full lifecycle of the Hay Day automation system:
1. Detects and verifies LDPlayer 9 / ADB connection.
2. Checks and launches `com.supercell.hayday` if not running.
3. Spawns and supervises `hay-star.exe` process.
4. Communicates over TCP port 31350 to issue native engine farming commands.
5. Watchdog monitors game health, detects crashes/hangs, and self-heals automatically.
6. Implements roadside shop auto-selling routines with dynamic newspaper ads.
=============================================================================
"""

import argparse
import json
import os
import random
import socket
import subprocess
import sys
import time
import threading
from datetime import datetime
from pathlib import Path
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

DEFAULT_CONFIG_PATH = Path(__file__).parent / "supervisor.config.json"

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

def log(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = f"[{timestamp}] [{level}]"
    if level == "INFO":
        color = Colors.CYAN
    elif level == "SUCCESS":
        color = Colors.GREEN
    elif level == "WARN":
        color = Colors.YELLOW
    elif level == "ERROR":
        color = Colors.RED
    else:
        color = Colors.RESET
    formatted = f"{color}{prefix} {msg}{Colors.RESET}"
    print(formatted)
    
    # Optional file logging
    try:
        with open("supervisor.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {msg}\n")
    except Exception:
        pass


class HayStarClient:
    """TCP Client for Hay Star REPL Control Server (port 31350)."""

    def __init__(self, host="127.0.0.1", port=31350, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self, retries=15, delay=2):
        for attempt in range(1, retries + 1):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.timeout)
                self.sock.connect((self.host, self.port))
                log(f"Connected to Hay Star control server at {self.host}:{self.port}", "SUCCESS")
                return True
            except (ConnectionRefusedError, socket.timeout, OSError):
                log(f"Waiting for Hay Star TCP server ({attempt}/{retries})...", "WARN")
                time.sleep(delay)
        return False

    def send_command(self, cmd):
        if not self.sock:
            if not self.connect(retries=3):
                return None
        try:
            full_cmd = cmd.strip() + "\n"
            self.sock.sendall(full_cmd.encode("utf-8"))
            time.sleep(0.3)
            # Read response if available
            self.sock.settimeout(self.timeout)
            data = b""
            while True:
                try:
                    chunk = self.sock.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                    if len(chunk) < 4096:
                        break
                except socket.timeout:
                    break
            return data.decode("utf-8", errors="ignore")
        except Exception as e:
            log(f"TCP communication error: {e}", "ERROR")
            self.close()
            return None

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


class SupervisorEngine:
    def __init__(self, config_path=None):
        self.config_path = Path(config_path or DEFAULT_CONFIG_PATH)
        self.config = self.load_config()
        self.client = None
        self.process = None
        self.running = False
        self.cycle_count = 0
        self.total_harvests = 0

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                log(f"Failed to parse config file: {e}. Using defaults.", "ERROR")
        return {
            "emulator": {"package_name": "com.supercell.hayday"},
            "farming": {"enabled": True, "crop_id": 400001, "farm_interval_sec": 125, "human_jitter_sec": 4},
            "roadside_shop": {"auto_sell": True, "item_id": 400001, "slot_start": 0, "slots_to_fill": 10, "stack_size": 10, "unit_price": 1, "enable_newspaper_ad": True},
            "watchdog": {"auto_restart_on_crash": True, "health_check_interval_sec": 10, "max_restart_attempts": 20},
            "tcp_control": {"host": "127.0.0.1", "port": 31350}
        }

    def print_banner(self):
        banner = f"""
{Colors.CYAN}{Colors.BOLD}
=============================================================================
   🌾 HAY STAR - AUTONOMOUS SUPERVISOR & SUPERCELL HAY DAY BOT 🌾
   Created by Ashraf Morningstar | https://github.com/AshrafMorningstar
=============================================================================
{Colors.RESET}
• Mode: Autonomous Supervisor & Anti-Crash Watchdog
• Target Package: {self.config.get('emulator', {}).get('package_name', 'com.supercell.hayday')}
• Target Crop ID: {self.config.get('farming', {}).get('crop_id', 400001)} ({self.config.get('farming', {}).get('crop_name', 'Wheat')})
• Loop Interval: {self.config.get('farming', {}).get('farm_interval_sec', 125)}s (±{self.config.get('farming', {}).get('human_jitter_sec', 4)}s jitter)
• Auto-Shop Seller: {'ENABLED' if self.config.get('roadside_shop', {}).get('auto_sell') else 'DISABLED'}
=============================================================================
"""
        print(banner)

    def find_adb(self):
        """Locate ADB executable in PATH or common LDPlayer directories."""
        common_locations = [
            r"C:\LDPlayer\LDPlayer9\adb.exe",
            r"D:\LDPlayer\LDPlayer9\adb.exe",
            r"C:\Program Files\LDPlayer\LDPlayer9\adb.exe",
            r"C:\Nox\bin\nox_adb.exe"
        ]
        for loc in common_locations:
            if os.path.isfile(loc):
                return loc
        return "adb"

    def check_emulator(self):
        """Check if emulator is responding via ADB."""
        adb = self.find_adb()
        try:
            res = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=5)
            devices = [line for line in res.stdout.splitlines() if "\tdevice" in line]
            if devices:
                log(f"Detected {len(devices)} active Android device(s): {devices[0].split()[0]}", "SUCCESS")
                return True
            log("No active ADB devices detected. Please ensure LDPlayer 9 is running.", "WARN")
            return False
        except Exception as e:
            log(f"ADB check warning: {e}", "WARN")
            return False

    def ensure_game_running(self):
        """Verify that Hay Day is foreground or launch it."""
        adb = self.find_adb()
        pkg = self.config.get("emulator", {}).get("package_name", "com.supercell.hayday")
        try:
            subprocess.run([adb, "shell", "monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"],
                           capture_output=True, timeout=5)
            time.sleep(2)
        except Exception:
            pass

    def start_loader_process(self):
        """Start hay-star.exe process if not already active."""
        exe_path = Path(__file__).parent / "hay-star.exe"
        if not exe_path.exists():
            log(f"hay-star.exe not found at {exe_path}. Searching in loader/target...", "WARN")
            release_exe = Path(__file__).parent / "target" / "release" / "hay-star.exe"
            if release_exe.exists():
                exe_path = release_exe
            else:
                log("Binary hay-star.exe not found. Please compile or download the release.", "ERROR")
                return False

        log(f"Launching Hay Star loader: {exe_path.name}", "INFO")
        try:
            self.process = subprocess.Popen(
                [str(exe_path)],
                cwd=str(Path(__file__).parent),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                # Use binary mode to avoid cp1252/_readerthread UnicodeDecodeError
                # We manually decode each line with errors='replace'
                text=False,
                bufsize=0,
            )
            def drain_stdout(proc):
                """Read hay-star.exe stdout safely, never crash on bad bytes."""
                try:
                    while True:
                        raw = proc.stdout.readline()
                        if not raw:
                            break
                        try:
                            line = raw.decode("utf-8", errors="replace").rstrip()
                        except Exception:
                            line = repr(raw)
                        if line:
                            log(f"[hay-star] {line}", "INFO")
                except Exception:
                    pass
            t = threading.Thread(target=drain_stdout, args=(self.process,), daemon=True)
            t.name = "hay-star-stdout-drain"
            t.start()
            time.sleep(3)
            return True
        except Exception as e:
            log(f"Failed to start hay-star.exe: {e}", "ERROR")
            return False

    def initialize_injection(self):
        """Connect to TCP control port and initialize native engine."""
        tcp_cfg = self.config.get("tcp_control", {})
        host = tcp_cfg.get("host", "127.0.0.1")
        port = tcp_cfg.get("port", 31350)
        retries = tcp_cfg.get("connect_retries", 15)
        timeout = tcp_cfg.get("command_timeout_sec", 15)

        self.client = HayStarClient(host=host, port=port, timeout=timeout)
        if not self.client.connect(retries=retries):
            log("Could not establish TCP connection with Hay Star engine.", "ERROR")
            return False

        log("Loading native ARM64 engine into Hay Day...", "INFO")
        resp = self.client.send_command("loadnative")
        log(f"Engine response: {resp.strip() if resp else 'OK'}", "SUCCESS")
        
        # Check spoofing and anti-cheat telemetry suppression
        if self.config.get("anti_detection", {}).get("spoof_samsung_s24", True):
            self.client.send_command("nspoof on")
        if self.config.get("anti_detection", {}).get("quago_telemetry_blocking", True):
            self.client.send_command("nquago block on")
            
        return True

    def execute_farm_cycle(self):
        """Executes one complete harvest -> plant -> sell cycle."""
        farming_cfg = self.config.get("farming", {})
        crop_id = farming_cfg.get("crop_id", 400001)
        shop_cfg = self.config.get("roadside_shop", {})

        self.cycle_count += 1
        log(f"--- Starting Autonomous Farming Cycle #{self.cycle_count} ---", "INFO")

        # 1. Harvest mature crops
        log("Triggering native field harvest...", "INFO")
        resp = self.client.send_command("nharvest")
        if resp:
            log(f"Harvest result: {resp.strip()}", "SUCCESS")
        self.total_harvests += 1
        time.sleep(1.2)

        # 2. Plant target crop
        log(f"Planting crop ID {crop_id} across all available fields...", "INFO")
        resp = self.client.send_command(f"nplant {crop_id}")
        if resp:
            log(f"Planting result: {resp.strip()}", "SUCCESS")
        time.sleep(1.0)

        # 3. Roadside Shop Auto-Sell
        if shop_cfg.get("auto_sell", True):
            slots = shop_cfg.get("slots_to_fill", 10)
            unit_price = shop_cfg.get("unit_price", 1)
            stack_size = shop_cfg.get("stack_size", 10)
            enable_ad = 1 if shop_cfg.get("enable_newspaper_ad", True) else 0

            log("Collecting roadside shop coins before listing...", "INFO")
            self.client.send_command("rss_claim_all")
            time.sleep(0.3)

            log(f"Managing Roadside Shop: selling {stack_size}x for {unit_price} coin(s) across slots...", "INFO")
            for slot in range(slots):
                # Advertise only the middle/featured slot to maximize buyer traffic
                ad_flag = enable_ad if slot == 0 else 0
                cmd = f"nsell {slot} {stack_size} {unit_price} {ad_flag} {crop_id}"
                self.client.send_command(cmd)
                time.sleep(0.2)
            log("Roadside shop crates refreshed, crops listed, and advertised.", "SUCCESS")

    def create_diagnostic_dump(self, reason="Process crashed"):
        """Captures screenshot, logcat, tombstones and report matching screenshot 07d9a5ce."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_dir = Path("error_logs") / f"crash_{timestamp}"
        dump_dir.mkdir(parents=True, exist_ok=True)
        adb = self.find_adb()

        print(f"\n{Colors.RED}[!] ===========================================================================")
        print(f"[!] CRASH / ERROR DETECTED: {reason}")
        print(f"{Colors.YELLOW}[*] Creating diagnostic dump in: {dump_dir}{Colors.RESET}")

        # 1. Screenshot
        try:
            ss_path = dump_dir / "screenshot.png"
            with open(ss_path, "wb") as f:
                subprocess.run([adb, "exec-out", "screencap", "-p"], stdout=f, timeout=5)
            print(f"{Colors.GREEN}[+] Screenshot captured: {ss_path}{Colors.RESET}")
        except Exception:
            pass

        # 2. Logcat
        try:
            logcat_path = dump_dir / "logcat.txt"
            res = subprocess.run([adb, "logcat", "-d"], capture_output=True, text=True, timeout=5)
            with open(logcat_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(res.stdout)
            print(f"{Colors.GREEN}[+] Logcat saved: {logcat_path}{Colors.RESET}")
        except Exception:
            pass

        # 3. Tombstones
        try:
            tomb_path = dump_dir / "tombstones.txt"
            res = subprocess.run([adb, "shell", "su -c 'ls -la /data/tombstones'"], capture_output=True, text=True, timeout=5)
            with open(tomb_path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(res.stdout)
            print(f"{Colors.GREEN}[+] Tombstones saved: {tomb_path}{Colors.RESET}")
        except Exception:
            pass

        # 4. Report
        try:
            rep_path = dump_dir / "problem_report.md"
            with open(rep_path, "w", encoding="utf-8") as f:
                f.write(f"# Hay Star Crash Diagnostic Report\n\n- Time: {datetime.now().isoformat()}\n- Reason: {reason}\n- Cycle: {self.cycle_count}\n")
            print(f"{Colors.GREEN}[+] Report written: {rep_path}{Colors.RESET}")
        except Exception:
            pass
        print(f"{Colors.RED}[!] ==========================================================================={Colors.RESET}\n")

    def run(self):
        """Main supervisor loop with watchdog self-healing and multi-account automation."""
        self.print_banner()
        self.running = True

        from account_manager import AccountManager
        from engine_bot import BotAutomationEngine

        acc_mgr = AccountManager()
        accounts = acc_mgr.list_accounts()
        if not accounts:
            accounts = [{"name": "default", "level": 86, "save_file": None}]

        restart_attempts = 0
        max_restarts = self.config.get("watchdog", {}).get("max_restart_attempts", 20)

        while self.running and restart_attempts < max_restarts:
            try:
                if not self.check_emulator():
                    log("LDPlayer 9 emulator not running. Please start LDPlayer 9 on your desktop.", "WARN")
                    time.sleep(4)
                    continue

                self.ensure_game_running()

                if not self.start_loader_process():
                    log("Failed to launch loader. Retrying in 5 seconds...", "ERROR")
                    time.sleep(5)
                    restart_attempts += 1
                    continue

                if not self.initialize_injection():
                    log("Injection failed or timed out. Restarting supervisor session...", "WARN")
                    self.create_diagnostic_dump("Injection handshake timeout")
                    self.cleanup()
                    restart_attempts += 1
                    time.sleep(3)
                    continue

                log("Hay Star Autonomous Supervisor is active and running!", "SUCCESS")
                restart_attempts = 0  # reset on successful launch

                # Initialize bot automation engine attached to active TCP client
                bot = BotAutomationEngine(client=self.client)

                base_interval = self.config.get("farming", {}).get("farm_interval_sec", 125)
                jitter_range = self.config.get("farming", {}).get("human_jitter_sec", 4)

                while self.running:
                    # Multi-Account cycle
                    for acc in accounts:
                        if not self.running:
                            break
                        if acc.get("save_file"):
                            log(f"Preparing account rotation to: {acc['name']} (Level {acc['level']})", "INFO")
                            acc_mgr.switch_account(acc)
                            self.ensure_game_running()
                            time.sleep(4)

                        self.cycle_count += 1
                        log(f"--- Starting Autonomous Farming Cycle #{self.cycle_count} for {acc['name']} ---", "INFO")

                        # Run the full 13-subsystem pass
                        bot.run_full_pass(acc['name'], acc['level'])

                        # Save inventory snapshot
                        acc_mgr.save_snapshot(acc, {
                            "timestamp": datetime.now().isoformat(),
                            "account": acc["name"],
                            "level": acc["level"],
                            "pass_number": bot.pass_number,
                            "harvests": self.total_harvests
                        })

                    # Calculate randomized human-like delay
                    jitter = random.uniform(-jitter_range, jitter_range)
                    sleep_duration = max(10, base_interval + jitter)
                    log(f"All accounts completed pass. Sleeping for {sleep_duration:.1f}s until crops/machines ready...", "INFO")

                    # Watchdog ping during sleep
                    elapsed = 0
                    while elapsed < sleep_duration and self.running:
                        time.sleep(5)
                        elapsed += 5
                        ping_res = self.client.send_command("nping")
                        if ping_res is None:
                            log("Watchdog detected unresponsive engine! Triggering self-heal...", "WARN")
                            self.create_diagnostic_dump("Unresponsive engine watchdog timeout")
                            raise ConnectionResetError("Engine unresponsive")

            except (ConnectionResetError, BrokenPipeError, ConnectionError) as e:
                log(f"Watchdog alert: {e}. Initiating auto-recovery...", "WARN")
                self.create_diagnostic_dump(str(e))
                self.cleanup()
                restart_attempts += 1
                cooldown = self.config.get("watchdog", {}).get("cooldown_between_restarts_sec", 3)
                print(f"{Colors.YELLOW}[*] Session ended (code 1). Auto-restarting in {cooldown}s... (Ctrl+C to stop){Colors.RESET}")
                print(f"{Colors.YELLOW}===== Auto-retry attempt {restart_attempts} (Ctrl+C to stop) ====={Colors.RESET}\n")
                time.sleep(cooldown)
            except KeyboardInterrupt:
                log("Received shutdown signal. Stopping supervisor...", "INFO")
                self.running = False
                break
            except Exception as e:
                log(f"Unexpected supervisor exception: {e}", "ERROR")
                self.create_diagnostic_dump(str(e))
                self.cleanup()
                restart_attempts += 1
                time.sleep(3)

        self.cleanup()
        log("Supervisor exited cleanly. Thank you for using Hay Star by Ashraf Morningstar.", "SUCCESS")

    def cleanup(self):
        """Cleanly close sockets and child processes."""
        if self.client:
            self.client.close()
            self.client = None
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=3)
            except Exception:
                try:
                    self.process.kill()
                except Exception:
                    pass
            self.process = None


def main():
    parser = argparse.ArgumentParser(
        description="Hay Star Autonomous Supervisor by Ashraf Morningstar",
        epilog="Visit https://github.com/AshrafMorningstar/hay-star for updates."
    )
    parser.add_argument("--config", "-c", help="Path to custom JSON configuration file")
    parser.add_argument("--test-config", action="store_true", help="Validate configuration and exit")
    parser.add_argument("--crop", type=int, help="Override crop ID (e.g. 400001 for Wheat)")
    parser.add_argument("--interval", type=int, help="Override loop interval in seconds")
    args = parser.parse_args()

    supervisor = SupervisorEngine(config_path=args.config)

    if args.crop:
        supervisor.config.setdefault("farming", {})["crop_id"] = args.crop
    if args.interval:
        supervisor.config.setdefault("farming", {})["farm_interval_sec"] = args.interval

    if args.test_config:
        print(json.dumps(supervisor.config, indent=2))
        log("Configuration validated successfully!", "SUCCESS")
        return

    supervisor.run()


if __name__ == "__main__":
    main()
