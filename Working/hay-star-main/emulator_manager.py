"""
emulator_manager.py — Hay★Star LDPlayer Emulator Manager
=========================================================
Zero-click emulator controller using ldconsole.exe.

Features
--------
* Auto-detect LDPlayer installation path
* List all instances (list2)
* Clone (copy) an existing instance
* Launch / Quit / Reboot any instance
* Install APK into an instance
* Run / Kill a package in an instance
* ADB pass-through command runner
* Interactive REPL (if run directly)
* Importable API for launcher.py / supervisor.py

CLI Usage
---------
    python emulator_manager.py                   # Interactive REPL
    python emulator_manager.py list              # List instances
    python emulator_manager.py launch            # Launch default instance
    python emulator_manager.py clone             # Clone default source
    python emulator_manager.py status            # Running instances
    python emulator_manager.py auto              # Full auto-setup

Commands inside REPL
---------------------
    list          - Show all instances
    status        - Show running instances
    launch [name] - Launch instance (default: HayStarBot)
    stop [name]   - Stop instance
    reboot [name] - Reboot instance
    clone [f] [t] - Clone from f to t
    runapp [name] - Run Hay Day in instance
    killapp [name]- Kill Hay Day in instance
    adb <cmd>     - Run ADB command in default instance
    backup [name] - Backup instance to backups folder
    restore [name]- Restore instance from backup
    auto          - Full zero-click auto-setup
    help          - Show this help
    exit          - Exit REPL
"""

import sys
import os
import subprocess
import time
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

LDCONSOLE_PATHS = [
    r"C:\LDPlayer\LDPlayer9\ldconsole.exe",
    r"C:\Program Files\LDPlayer\LDPlayer9\ldconsole.exe",
    r"C:\Program Files (x86)\LDPlayer\LDPlayer9\ldconsole.exe",
]

DEFAULT_SOURCE_INSTANCE = "LDPlayer"       # base instance to clone from
DEFAULT_BOT_INSTANCE    = "HayStarBot"     # bot-dedicated clone
HAYDAY_PACKAGE          = "com.supercell.hayday"

BACKUP_DIR = Path(__file__).parent / "emulator_backups"

# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def _find_ldconsole() -> Path:
    for p in LDCONSOLE_PATHS:
        path = Path(p)
        if path.exists():
            return path
    found = shutil.which("ldconsole")
    if found:
        return Path(found)
    raise FileNotFoundError(
        "ldconsole.exe not found. Install LDPlayer 9 or add it to PATH.\n"
        f"Searched: {LDCONSOLE_PATHS}"
    )

LDCONSOLE = None

def get_ldconsole() -> Path:
    global LDCONSOLE
    if LDCONSOLE is None:
        LDCONSOLE = _find_ldconsole()
    return LDCONSOLE


def _run(args: list, capture: bool = True, timeout: int = 60) -> subprocess.CompletedProcess:
    cmd = [str(get_ldconsole())] + args
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Command timed out after {timeout}s: {' '.join(args)}")
        raise
    except Exception as exc:
        print(f"[ERROR] Failed to run ldconsole: {exc}")
        raise


def _stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _ok(msg):   print(f"  [OK]  [{_stamp()}] {msg}")
def _err(msg):  print(f"  [ERR] [{_stamp()}] {msg}")
def _info(msg): print(f"  [..] {msg}")

# ---------------------------------------------------------------------------
# Core API
# ---------------------------------------------------------------------------

def list_instances() -> list:
    result = _run(["list2"])
    instances = []
    for line in result.stdout.strip().splitlines():
        parts = line.strip().split(",")
        if len(parts) >= 9:
            idx, name, top, left, opacity, running, _, width, height = parts[:9]
            dpi = parts[9].strip() if len(parts) > 9 else "160"
            instances.append({
                "index":   int(idx),
                "name":    name,
                "running": running.strip() == "1",
                "width":   width,
                "height":  height,
                "dpi":     dpi,
            })
    return instances


def running_instances() -> list:
    result = _run(["runninglist"])
    if result.returncode != 0 or not result.stdout.strip():
        return []
    names = []
    for line in result.stdout.strip().splitlines():
        parts = line.strip().split(",")
        if len(parts) >= 2:
            names.append(parts[1])
    return names


def is_running(name: str) -> bool:
    """Check if a specific instance is currently running."""
    # Primary check: isrunning
    result = _run(["isrunning", "--name", name])
    if result.stdout.strip() == "running":
        return True
    # Fallback: check list2 running flag (bit -1 means stopped, 0/1 means running)
    try:
        for inst in list_instances():
            if inst["name"] == name:
                return inst["running"]
    except Exception:
        pass
    # Also check runninglist
    return name in running_instances()


def instance_exists(name: str) -> bool:
    return any(i["name"] == name for i in list_instances())


def launch_instance(name: str = DEFAULT_BOT_INSTANCE, wait: bool = True) -> bool:
    if not instance_exists(name):
        _err(f"Instance '{name}' does not exist. Run 'clone' first.")
        return False
    if is_running(name):
        _ok(f"Instance '{name}' is already running.")
        return True
    _info(f"Launching '{name}'...")
    result = _run(["launch", "--name", name])
    if result.returncode != 0:
        _err(f"Launch failed ({result.returncode}): {result.stderr.strip()}")
        return False
    if wait:
        _info("Waiting for instance to start (up to 60 s)...")
        for _ in range(30):
            time.sleep(2)
            if is_running(name):
                _ok(f"Instance '{name}' is now running.")
                return True
        _err(f"Instance '{name}' did not start within 60 s.")
        return False
    _ok(f"Launch command sent for '{name}'.")
    return True


def quit_instance(name: str = DEFAULT_BOT_INSTANCE) -> bool:
    if not is_running(name):
        _info(f"Instance '{name}' is not running.")
        return True
    _info(f"Stopping '{name}'...")
    result = _run(["quit", "--name", name])
    if result.returncode == 0:
        _ok(f"Instance '{name}' stopped.")
        return True
    _err(f"Quit failed: {result.stderr.strip()}")
    return False


def reboot_instance(name: str = DEFAULT_BOT_INSTANCE) -> bool:
    _info(f"Rebooting '{name}'...")
    result = _run(["reboot", "--name", name])
    if result.returncode == 0:
        _ok(f"Reboot sent for '{name}'.")
        return True
    _err(f"Reboot failed: {result.stderr.strip()}")
    return False


def clone_instance(
    source: str = DEFAULT_SOURCE_INSTANCE,
    dest:   str = DEFAULT_BOT_INSTANCE,
    overwrite: bool = False,
) -> bool:
    if not instance_exists(source):
        _err(f"Source instance '{source}' does not exist.")
        return False
    if instance_exists(dest):
        if overwrite:
            _info(f"Removing existing '{dest}' for re-clone...")
            result = _run(["remove", "--name", dest])
            if result.returncode != 0:
                _err(f"Could not remove '{dest}': {result.stderr.strip()}")
                return False
            time.sleep(2)
        else:
            _ok(f"Clone '{dest}' already exists — skipping.")
            return True
    _info(f"Cloning '{source}' -> '{dest}'...")
    result = _run(["copy", "--name", dest, "--from", source], timeout=120)
    # ldconsole 'copy' sometimes exits with code 1 even on success — verify by re-listing
    time.sleep(2)
    if instance_exists(dest):
        _ok(f"Instance '{dest}' cloned from '{source}'.")
        return True
    if result.returncode == 0:
        _ok(f"Instance '{dest}' cloned from '{source}'.")
        return True
    _err(f"Clone failed ({result.returncode}): {result.stderr.strip()}")
    return False


def run_app(name: str = DEFAULT_BOT_INSTANCE, package: str = HAYDAY_PACKAGE) -> bool:
    if not is_running(name):
        _err(f"Instance '{name}' is not running.")
        return False
    _info(f"Starting {package} in '{name}'...")
    result = _run(["runapp", "--name", name, "--packagename", package])
    if result.returncode == 0:
        _ok(f"App '{package}' launched in '{name}'.")
        return True
    _err(f"runapp failed: {result.stderr.strip()}")
    return False


def kill_app(name: str = DEFAULT_BOT_INSTANCE, package: str = HAYDAY_PACKAGE) -> bool:
    _info(f"Killing {package} in '{name}'...")
    result = _run(["killapp", "--name", name, "--packagename", package])
    if result.returncode == 0:
        _ok(f"App '{package}' killed in '{name}'.")
        return True
    _err(f"killapp failed: {result.stderr.strip()}")
    return False


def install_apk(apk_path: str, name: str = DEFAULT_BOT_INSTANCE) -> bool:
    apk = Path(apk_path)
    if not apk.exists():
        _err(f"APK not found: {apk_path}")
        return False
    _info(f"Installing {apk.name} into '{name}'...")
    result = _run(["installapp", "--name", name, "--filename", str(apk)], timeout=180)
    if result.returncode == 0:
        _ok(f"APK installed: {apk.name}")
        return True
    _err(f"installapp failed: {result.stderr.strip()}")
    return False


def run_adb(command: str, name: str = DEFAULT_BOT_INSTANCE) -> str:
    _info(f"ADB [{name}]: {command}")
    result = _run(["adb", "--name", name, "--command", command])
    if result.returncode == 0:
        output = result.stdout.strip()
        if output:
            print(f"  -> {output}")
        return output
    _err(f"ADB failed: {result.stderr.strip()}")
    return ""


def backup_instance(name: str = DEFAULT_BOT_INSTANCE) -> bool:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = BACKUP_DIR / f"{name}_{stamp}.ldbk"
    _info(f"Backing up '{name}' -> {backup_file.name}...")
    result = _run(["backup", "--name", name, "--file", str(backup_file)], timeout=300)
    if result.returncode == 0:
        _ok(f"Backup saved: {backup_file}")
        return True
    _err(f"Backup failed: {result.stderr.strip()}")
    return False


def restore_instance(name: str = DEFAULT_BOT_INSTANCE) -> bool:
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backups = sorted(BACKUP_DIR.glob(f"{name}_*.ldbk"), reverse=True)
    if not backups:
        _err(f"No backups found for '{name}' in {BACKUP_DIR}")
        return False
    latest = backups[0]
    _info(f"Restoring '{name}' from {latest.name}...")
    result = _run(["restore", "--name", name, "--file", str(latest)], timeout=300)
    if result.returncode == 0:
        _ok(f"Restored '{name}' from {latest.name}")
        return True
    _err(f"Restore failed: {result.stderr.strip()}")
    return False


# ---------------------------------------------------------------------------
# High-level convenience: full auto-setup
# ---------------------------------------------------------------------------

def auto_setup_and_launch(
    source: str = DEFAULT_SOURCE_INSTANCE,
    dest:   str = DEFAULT_BOT_INSTANCE,
    launch_game: bool = True,
) -> bool:
    """
    Zero-click full setup:
      1. Clone source -> dest (if not already cloned)
      2. Launch the dest instance
      3. Optionally launch Hay Day inside it
    """
    print(f"\n{'='*58}")
    print(f"    Hay-Star  Auto Emulator Setup")
    print(f"{'='*58}")
    if not clone_instance(source=source, dest=dest):
        return False
    if not launch_instance(name=dest, wait=True):
        return False
    if launch_game:
        _info("Waiting 10 s for Android to boot...")
        time.sleep(10)
        if not run_app(name=dest):
            _err("Could not start Hay Day. Install the APK first.")
            return False
    print(f"\n    Emulator '{dest}' is ready! Hay Day is running.")
    print(f"{'='*58}\n")
    return True


# ---------------------------------------------------------------------------
# Pretty display helpers
# ---------------------------------------------------------------------------

def print_instance_table():
    instances = list_instances()
    running   = set(running_instances())
    print(f"\n  {'#':<4} {'Name':<22} {'Size':<14} {'DPI':<6} Status")
    print(f"  {'-'*58}")
    for inst in instances:
        status = "Running" if (inst["name"] in running or inst["running"]) else "Stopped"
        size   = f"{inst['width']}x{inst['height']}"
        print(f"  {inst['index']:<4} {inst['name']:<22} {size:<14} {inst['dpi']:<6} {status}")
    print()


def print_status():
    running = running_instances()
    if not running:
        print("\n  No instances currently running.\n")
    else:
        print(f"\n  Running: {', '.join(running)}\n")


# ---------------------------------------------------------------------------
# Interactive REPL
# ---------------------------------------------------------------------------

REPL_HELP = """
  +----------------------------------------------------------+
  |          Hay-Star  Emulator Manager REPL                 |
  +----------------------------------------------------------+
  |  list                  List all instances                |
  |  status                Show running instances            |
  |  launch [name]         Launch instance                   |
  |  stop [name]           Stop instance                     |
  |  reboot [name]         Reboot instance                   |
  |  clone [from] [to]     Clone instance                    |
  |  runapp [name]         Launch Hay Day in instance        |
  |  killapp [name]        Kill Hay Day in instance          |
  |  adb <cmd>             ADB pass-through                  |
  |  backup [name]         Backup instance                   |
  |  restore [name]        Restore latest backup             |
  |  auto                  Full zero-click auto-setup        |
  |  help                  Show this help                    |
  |  exit                  Exit REPL                         |
  +----------------------------------------------------------+
"""


def run_repl():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(REPL_HELP)
    while True:
        try:
            raw = input("  emu> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Goodbye!")
            break
        if not raw:
            continue
        parts = raw.split()
        cmd   = parts[0].lower()
        args  = parts[1:]

        if cmd in ("exit", "x"):
            print("  Goodbye!")
            break
        elif cmd == "help":
            print(REPL_HELP)
        elif cmd == "list":
            print_instance_table()
        elif cmd == "status":
            print_status()
        elif cmd == "launch":
            launch_instance(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "stop":
            quit_instance(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "reboot":
            reboot_instance(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "clone":
            src  = args[0] if len(args) > 0 else DEFAULT_SOURCE_INSTANCE
            dest = args[1] if len(args) > 1 else DEFAULT_BOT_INSTANCE
            clone_instance(source=src, dest=dest)
        elif cmd == "runapp":
            run_app(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "killapp":
            kill_app(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "adb":
            if not args:
                _err("Usage: adb <command>")
            else:
                run_adb(" ".join(args))
        elif cmd == "backup":
            backup_instance(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "restore":
            restore_instance(args[0] if args else DEFAULT_BOT_INSTANCE)
        elif cmd == "auto":
            auto_setup_and_launch()
        else:
            _err(f"Unknown command: '{cmd}'. Type 'help'.")


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def _parse_args():
    p = argparse.ArgumentParser(
        prog="emulator_manager",
        description="Hay-Star LDPlayer Emulator Manager",
    )
    sub = p.add_subparsers(dest="command")
    sub.add_parser("list",   help="List all instances")
    sub.add_parser("status", help="Show running instances")

    lp = sub.add_parser("launch", help="Launch an instance")
    lp.add_argument("name", nargs="?", default=DEFAULT_BOT_INSTANCE)

    sp = sub.add_parser("stop", help="Stop an instance")
    sp.add_argument("name", nargs="?", default=DEFAULT_BOT_INSTANCE)

    rp = sub.add_parser("reboot", help="Reboot an instance")
    rp.add_argument("name", nargs="?", default=DEFAULT_BOT_INSTANCE)

    cp = sub.add_parser("clone", help="Clone an instance")
    cp.add_argument("source", nargs="?", default=DEFAULT_SOURCE_INSTANCE)
    cp.add_argument("dest",   nargs="?", default=DEFAULT_BOT_INSTANCE)
    cp.add_argument("--overwrite", action="store_true")

    ap = sub.add_parser("auto", help="Full auto-setup and launch")
    ap.add_argument("--no-game", action="store_true")

    sub.add_parser("backup",  help="Backup default instance")
    sub.add_parser("restore", help="Restore default instance")
    return p.parse_args()


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = _parse_args()
    if args.command is None:
        run_repl()
    elif args.command == "list":
        print_instance_table()
    elif args.command == "status":
        print_status()
    elif args.command == "launch":
        sys.exit(0 if launch_instance(args.name) else 1)
    elif args.command == "stop":
        sys.exit(0 if quit_instance(args.name) else 1)
    elif args.command == "reboot":
        sys.exit(0 if reboot_instance(args.name) else 1)
    elif args.command == "clone":
        sys.exit(0 if clone_instance(args.source, args.dest, overwrite=args.overwrite) else 1)
    elif args.command == "auto":
        sys.exit(0 if auto_setup_and_launch(launch_game=not args.no_game) else 1)
    elif args.command == "backup":
        sys.exit(0 if backup_instance() else 1)
    elif args.command == "restore":
        sys.exit(0 if restore_instance() else 1)


if __name__ == "__main__":
    main()
