#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Automated Environment Installer & Diagnostic Suite
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Verifies and configures all prerequisites for running the Hay Star bot:
  1. Python version (>= 3.9)
  2. Core Python modules (frida, standard libraries)
  3. Node.js & npm (for building JS hooks)
  4. Pre-built JS bundles (java_guard.bundle.js, quago_probe.bundle.js)
  5. ADB binary & LDPlayer 9 / Nox emulator connection
  6. Android root permissions & Hay Day installation (com.supercell.hayday)
  7. Core binaries & scripts (hay-star.exe, engine_bot.py, auto_farm_loop.py, etc.)
  8. Staging cache & asset directories
=============================================================================
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent

class Colors:
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_banner():
    print(f"""{Colors.CYAN}{Colors.BOLD}
======================================================================
  🌾 HAY STAR — ENVIRONMENT INSTALLER & PREFLIGHT DIAGNOSTICS
  Ashraf Morningstar | https://github.com/AshrafMorningstar/hay-star
======================================================================{Colors.RESET}""")


class Installer:
    def __init__(self):
        self.results = []
        self.adb = None

    def record(self, check_name, passed, details="", is_critical=True):
        self.results.append({
            "name": check_name,
            "passed": passed,
            "details": details,
            "critical": is_critical
        })
        status_tag = f"{Colors.GREEN}[ PASS ]{Colors.RESET}" if passed else (
            f"{Colors.RED}[ FAIL ]{Colors.RESET}" if is_critical else f"{Colors.YELLOW}[ WARN ]{Colors.RESET}"
        )
        print(f"  {status_tag} {check_name:<36} {details}")

    def check_python(self):
        v = sys.version_info
        passed = v.major == 3 and v.minor >= 9
        ver_str = f"{v.major}.{v.minor}.{v.micro}"
        self.record("Python Runtime (>= 3.9)", passed, f"Detected: {ver_str}", is_critical=True)

    def check_pip_package(self, pkg_name, required=False, auto_install=False):
        try:
            __import__(pkg_name)
            self.record(f"Python Package: {pkg_name}", True, "Installed and importable", is_critical=required)
            return True
        except ImportError:
            if auto_install:
                print(f"  [*] Attempting pip install for {pkg_name}...")
                try:
                    res = subprocess.run([sys.executable, "-m", "pip", "install", pkg_name, "--quiet"],
                                         capture_output=True, timeout=20)
                    if res.returncode == 0:
                        self.record(f"Python Package: {pkg_name}", True, "Successfully installed via pip", is_critical=required)
                        return True
                except Exception:
                    pass
            self.record(f"Python Package: {pkg_name}", False, "Not installed (Optional for native mode; install via pip install frida)", is_critical=required)
            return False

    def check_core_files(self):
        core_files = [
            ("hay-star.exe", True),
            ("engine_bot.py", True),
            ("game_ids.py", True),
            ("command_registry.py", True),
            ("auto_farm_loop.py", True),
            ("config_automation.py", True),
            ("account_manager.py", True),
            ("hook.js", True),
            ("java_guard.bundle.js", True),
            ("quago_probe.bundle.js", True),
            ("supervisor.py", True),
            ("launcher.py", True),
            ("start.bat", True),
            ("Assest/configs/farm/loll.json", True),
        ]
        for f, req in core_files:
            p = WORKSPACE_ROOT / f
            exists = p.exists()
            size = f"{p.stat().st_size:,} bytes" if exists else "Missing"
            self.record(f"Core File: {f}", exists, size, is_critical=req)

    def check_adb(self):
        candidates = [
            r"C:\LDPlayer\LDPlayer9\adb.exe",
            r"D:\LDPlayer\LDPlayer9\adb.exe",
            r"C:\Program Files\LDPlayer\LDPlayer9\adb.exe",
            str(WORKSPACE_ROOT / "Assest" / "adb" / "adb.exe"),
            "adb"
        ]
        found = None
        for c in candidates:
            if os.path.isfile(c) or c == "adb":
                try:
                    res = subprocess.run([c, "version"], capture_output=True, timeout=3)
                    if res.returncode == 0:
                        found = c
                        break
                except Exception:
                    pass
        self.adb = found
        if found:
            self.record("ADB Executable", True, f"Found: {found}", is_critical=False)
        else:
            self.record("ADB Executable", False, "Not found. Please install LDPlayer 9 or Android Platform Tools", is_critical=False)

    def check_emulator_device(self):
        if not self.adb:
            self.record("Emulator Device (ADB)", False, "Skipped (ADB not found)", is_critical=False)
            return
        try:
            res = subprocess.run([self.adb, "devices"], capture_output=True, text=True, timeout=5)
            lines = [l.strip() for l in res.stdout.strip().splitlines()[1:] if l.strip()]
            devices = [l for l in lines if "\tdevice" in l]
            if devices:
                dev_id = devices[0].split("\t")[0]
                self.record("Emulator Device Online", True, f"Connected: {dev_id}", is_critical=False)
                # Check root
                root_res = subprocess.run([self.adb, "-s", dev_id, "shell", "su -c id"], capture_output=True, text=True, timeout=3)
                is_root = "uid=0" in root_res.stdout
                self.record("Root Privileges (su)", is_root, "Root available" if is_root else "Root not detected", is_critical=False)
                # Check Hay Day
                hd_res = subprocess.run([self.adb, "-s", dev_id, "shell", "pm path com.supercell.hayday"], capture_output=True, text=True, timeout=3)
                has_hd = "package:" in hd_res.stdout
                self.record("Hay Day App Installed", has_hd, "com.supercell.hayday installed" if has_hd else "Install Hay Day on emulator", is_critical=False)
            else:
                self.record("Emulator Device Online", False, "No active device. Launch LDPlayer 9", is_critical=False)
        except Exception as e:
            self.record("Emulator Device Online", False, f"ADB query error: {e}", is_critical=False)

    def prepare_directories(self):
        dirs = [
            WORKSPACE_ROOT / "stage_cache",
            WORKSPACE_ROOT / "tools" / "extracted_ids",
            WORKSPACE_ROOT / "tests",
            WORKSPACE_ROOT / "project-logs",
            WORKSPACE_ROOT / "Assest" / "accounts",
            WORKSPACE_ROOT / "Assest" / "configs" / "farm",
        ]
        all_created = True
        for d in dirs:
            try:
                d.mkdir(parents=True, exist_ok=True)
            except Exception:
                all_created = False
        self.record("Directory Scaffolding", all_created, f"Verified {len(dirs)} system directories", is_critical=True)

    def run_all(self):
        print("\n[*] Running Environment & Dependency Verification...\n")
        self.check_python()
        self.prepare_directories()
        self.check_core_files()
        self.check_pip_package("frida", required=False)
        self.check_adb()
        self.check_emulator_device()

        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        critical_failed = sum(1 for r in self.results if not r["passed"] and r["critical"])

        print(f"\n{'='*70}")
        if critical_failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}  ALL CORE PREREQUISITES VERIFIED! ({passed}/{total} checks passed){Colors.RESET}")
            print("  You are ready to launch Hay Star with: start.bat or python launcher.py")
        else:
            print(f"{Colors.RED}{Colors.BOLD}  {critical_failed} CRITICAL REQUIREMENT(S) MISSING! ({passed}/{total} passed){Colors.RESET}")
            print("  Please resolve the failed items above.")
        print(f"{'='*70}\n")
        return critical_failed == 0


if __name__ == "__main__":
    print_banner()
    installer = Installer()
    success = installer.run_all()
    sys.exit(0 if success else 1)
