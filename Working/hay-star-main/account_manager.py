#!/usr/bin/env python3
"""
=============================================================================
Hay Star Multi-Account Manager & Save State Switcher
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Manages account profiles in Assest/accounts/:
- Discovers available farm accounts (e.g., main/86, lolas r/55).
- Safely swaps save state (storage_new.xml) into /data/data/com.supercell.hayday/shared_prefs/
- Adjusts Linux filesystem permissions (chmod 660, chown) so Hay Day reads the save.
- Captures and saves inventory_snapshot.json per account after each run.
- Interactive CLI menu & command shortcut 'as' support.
- Scheduled automatic account rotation.
=============================================================================
"""

import os
import sys
import json
import time
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
ACCOUNTS_DIR = WORKSPACE_ROOT / "Assest" / "accounts"


def locate_adb():
    candidates = [
        r"C:\LDPlayer\LDPlayer9\adb.exe",
        r"D:\LDPlayer\LDPlayer9\adb.exe",
        r"C:\Program Files\LDPlayer\LDPlayer9\adb.exe",
        str(WORKSPACE_ROOT / "Assest" / "adb" / "adb.exe"),
        "adb"
    ]
    for c in candidates:
        if os.path.isfile(c) or c == "adb":
            try:
                res = subprocess.run([c, "version"], capture_output=True, timeout=3)
                if res.returncode == 0:
                    return c
            except Exception:
                pass
    return "adb"


class AccountManager:
    def __init__(self, accounts_root=None):
        self.accounts_root = Path(accounts_root or ACCOUNTS_DIR)
        self.adb = locate_adb()

    def list_accounts(self):
        """
        Scans accounts directory and returns a list of account profiles:
        [{ 'name': 'main', 'level': '86', 'dir': Path, 'save_file': Path }, ...]
        """
        accounts = []
        if not self.accounts_root.exists():
            return accounts

        for acc_folder in self.accounts_root.iterdir():
            if acc_folder.is_dir():
                for level_folder in acc_folder.iterdir():
                    if level_folder.is_dir():
                        save_file = level_folder / "storage_new.xml"
                        if save_file.exists():
                            accounts.append({
                                "name": acc_folder.name,
                                "level": level_folder.name,
                                "dir": level_folder,
                                "save_file": save_file,
                                "snapshot_file": level_folder / "inventory_snapshot.json"
                            })
        return sorted(accounts, key=lambda a: a["name"])

    def check_device_connected(self):
        """Check if an Android emulator/device is online via ADB."""
        try:
            res = subprocess.run([self.adb, "devices"], capture_output=True, text=True, timeout=3)
            lines = [l.strip() for l in res.stdout.strip().splitlines()[1:] if l.strip()]
            connected = [l for l in lines if "\tdevice" in l]
            return len(connected) > 0
        except Exception:
            return False

    def switch_account(self, account_profile, dry_run=False):
        """
        Safely stops the game and pushes the specified account's storage_new.xml to Hay Day.
        """
        save_file = account_profile.get("save_file")
        if not save_file or not save_file.exists():
            print(f"[!] Save file not found for account {account_profile.get('name')}")
            return False

        print(f"\n[*] Switching to account: {account_profile['name']} (Level {account_profile['level']})...")
        pkg = "com.supercell.hayday"

        if dry_run or not self.check_device_connected():
            print(f"[*] [Simulation/Dry-Run] Target save: {save_file}")
            print(f"[+] Account profile '{account_profile['name']}' selected (emulator offline or dry-run).")
            return True

        # 1. Force stop Hay Day
        print("[*] Stopping game before save injection...")
        subprocess.run([self.adb, "shell", "am", "force-stop", pkg], capture_output=True)
        time.sleep(1)

        # 2. Push save file to /data/local/tmp
        remote_tmp = "/data/local/tmp/storage_new.xml"
        target_prefs = f"/data/data/{pkg}/shared_prefs"
        target_file = f"{target_prefs}/storage_new.xml"

        print("[*] Pushing save file via ADB...")
        push_res = subprocess.run([self.adb, "push", str(save_file), remote_tmp], capture_output=True, text=True)
        if push_res.returncode != 0:
            print(f"[!] Failed to push save file: {push_res.stderr}")
            return False

        # 3. Move into shared_prefs and set ownership
        cmd_install = f"su -c 'mkdir -p {target_prefs} && mv {remote_tmp} {target_file} && chmod 660 {target_file}'"
        subprocess.run([self.adb, "shell", cmd_install], capture_output=True)

        # Get Hay Day UID to set correct chown
        uid_res = subprocess.run([self.adb, "shell", f"su -c 'stat -c %u /data/data/{pkg}'"], capture_output=True, text=True)
        uid = uid_res.stdout.strip()
        if uid.isdigit():
            subprocess.run([self.adb, "shell", f"su -c 'chown {uid}:{uid} {target_file}'"], capture_output=True)

        print(f"[+] Account {account_profile['name']} save successfully installed!")
        return True

    def rotate_accounts(self, interval_seconds=1800, callback_per_account=None):
        """
        Continuously rotate through all accounts at a specified interval.
        """
        accounts = self.list_accounts()
        if not accounts:
            print("[!] No accounts found to rotate.")
            return

        print(f"[*] Starting Account Rotation across {len(accounts)} accounts (Interval: {interval_seconds}s)...")
        idx = 0
        try:
            while True:
                acc = accounts[idx % len(accounts)]
                print(f"\n{'='*60}")
                print(f"[*] ROTATION CYCLE: Account #{idx + 1} -> {acc['name']} (Level {acc['level']})")
                print(f"{'='*60}")
                self.switch_account(acc)

                if callback_per_account:
                    callback_per_account(acc)

                print(f"[*] Sleeping for {interval_seconds} seconds before next rotation...")
                time.sleep(interval_seconds)
                idx += 1
        except KeyboardInterrupt:
            print("\n[*] Account rotation stopped by user.")

    def save_snapshot(self, account_profile, snapshot_data):
        """
        Saves updated inventory snapshot to account directory.
        """
        snap_file = account_profile.get("snapshot_file")
        if snap_file:
            with open(snap_file, "w", encoding="utf-8") as f:
                json.dump(snapshot_data, f, indent=2)
            print(f"[+] Saved inventory snapshot for account {account_profile['name']}.")


def interactive_cli():
    """Interactive account selection CLI."""
    mgr = AccountManager()
    accs = mgr.list_accounts()
    if not accs:
        print("[!] No accounts found in Assest/accounts/")
        return

    print("=" * 60)
    print("           HAY STAR MULTI-ACCOUNT MANAGER (as)")
    print("=" * 60)
    for i, a in enumerate(accs, 1):
        print(f"  [{i}] {a['name']:<20} (Farm Level {a['level']})")
    print("  [R] Start Automatic Account Rotation")
    print("  [Q] Exit")
    print("=" * 60)

    choice = input("\nSelect account number to switch to: ").strip()
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(accs):
            mgr.switch_account(accs[idx])
        else:
            print("[!] Invalid account number.")
    elif choice.lower() == "r":
        sec_str = input("Enter rotation interval in seconds [default 1800]: ").strip()
        secs = int(sec_str) if sec_str.isdigit() else 1800
        mgr.rotate_accounts(secs)


if __name__ == "__main__":
    mgr = AccountManager()
    accs = mgr.list_accounts()

    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("list", "ls", "al"):
            print(f"[*] Discovered {len(accs)} account(s):")
            for i, a in enumerate(accs, 1):
                print(f"  [{i}] {a['name']:<20} (Level {a['level']})")
        elif arg in ("switch", "as") and len(sys.argv) > 2:
            target = sys.argv[2]
            if target.isdigit():
                idx = int(target) - 1
                if 0 <= idx < len(accs):
                    mgr.switch_account(accs[idx])
            else:
                match = next((a for a in accs if a["name"].lower() == target.lower()), None)
                if match:
                    mgr.switch_account(match)
                else:
                    print(f"[!] Account '{target}' not found.")
        elif arg in ("rotate",):
            secs = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 1800
            mgr.rotate_accounts(secs)
        else:
            interactive_cli()
    else:
        interactive_cli()
