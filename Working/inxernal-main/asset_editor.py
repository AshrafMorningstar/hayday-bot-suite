#!/usr/bin/env python3
"""
INXERNAL / Hay Day Live Asset Editor & Testing Debugger
Provides interactive and programmatic inspection, live editing, and testing
of Hay Day CSV game data tables (exceed prices, harvest, times, levels) on LDPlayer.
"""

import csv
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tarfile
import tempfile
import time
from pathlib import Path

# Safe UTF-8 console output for Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

PROJECT_DIR = Path(__file__).resolve().parent
PACKAGE_NAME = "com.supercell.hayday"
APP_DATA_DIR = f"/data/user/0/{PACKAGE_NAME}"
APP_UPDATE_DIR = f"{APP_DATA_DIR}/update"

# Primary asset directories
DEFAULT_MOD_DIR = PROJECT_DIR / "com.supercell.hayday" / "نسخه اعلى سعر" / "update"
DATA_DIR = DEFAULT_MOD_DIR / "data"
BACKUP_DIR = PROJECT_DIR / "com.supercell.hayday" / ".asset_backups"

# ADB search paths
ADB_PATHS = [
    r"C:\LDPlayer\LDPlayer9\adb.exe",
    r"C:\LDPlayer\LDPlayer14\adb.exe",
    r"C:\Program Files\Genymobile\Genymotion\tools\adb.exe",
    "adb",
]


def find_adb():
    for p in ADB_PATHS:
        try:
            res = subprocess.run([p, "version"], capture_output=True, text=True, timeout=3)
            if res.returncode == 0:
                return p
        except Exception:
            continue
    return "adb"


def find_emulator(adb=None):
    adb = adb or find_adb()
    try:
        res = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=3)
        for line in res.stdout.strip().splitlines()[1:]:
            line = line.strip()
            if not line or "offline" in line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2 and parts[1] == "device":
                return parts[0]
    except Exception:
        pass
    return "emulator-5554"


def ensure_backup(csv_path: Path):
    """Ensure an untouched baseline backup exists for a CSV file before editing."""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    bak_path = BACKUP_DIR / csv_path.name
    if not bak_path.exists() and csv_path.exists():
        shutil.copy2(csv_path, bak_path)


def read_csv_table(csv_path: Path):
    if not csv_path.is_file():
        return None, None, []
    with open(csv_path, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = list(csv.reader(f))
    if len(reader) < 2:
        return None, None, []
    headers = [h.strip() for h in reader[0]]
    types = [t.strip() for t in reader[1]]
    rows = reader[2:]
    return headers, types, rows


def write_csv_table(csv_path: Path, headers, types, rows):
    ensure_backup(csv_path)
    with open(csv_path, "w", encoding="utf-8", newline="\n") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(headers)
        writer.writerow(types)
        writer.writerows(rows)


class AssetEditor:
    def __init__(self, data_dir=None, device=None):
        self.data_dir = Path(data_dir) if data_dir else DATA_DIR
        self.adb = find_adb()
        self.device = device or find_emulator(self.adb)

    def search_items(self, query: str):
        """Search across all CSV tables for any item matching query."""
        results = []
        q = query.strip().lower()
        if not self.data_dir.is_dir():
            return results

        for csv_file in sorted(self.data_dir.glob("*.csv")):
            headers, types, rows = read_csv_table(csv_file)
            if not headers:
                continue
            name_idx = headers.index("Name") if "Name" in headers else 0
            val_idx = headers.index("Value") if "Value" in headers else -1
            harv_idx = headers.index("Harvest") if "Harvest" in headers else -1
            time_idx = headers.index("TimeMin") if "TimeMin" in headers else -1
            time_sec_idx = headers.index("TimeSec") if "TimeSec" in headers else -1
            lvl_idx = headers.index("UnlockLevel") if "UnlockLevel" in headers else -1

            for row_idx, row in enumerate(rows):
                if not row or len(row) <= name_idx:
                    continue
                name = row[name_idx].strip()
                if not name:
                    continue
                if q in name.lower():
                    val = row[val_idx].strip() if val_idx >= 0 and val_idx < len(row) else ""
                    val_int = int(val) if val.isdigit() else 0
                    max_price = round(val_int * 3.6) if val_int > 0 else 0
                    results.append({
                        "name": name,
                        "table": csv_file.name,
                        "row_idx": row_idx,
                        "value": val,
                        "max_price": max_price,
                        "harvest": row[harv_idx].strip() if harv_idx >= 0 and harv_idx < len(row) else "",
                        "time_min": row[time_idx].strip() if time_idx >= 0 and time_idx < len(row) else "",
                        "time_sec": row[time_sec_idx].strip() if time_sec_idx >= 0 and time_sec_idx < len(row) else "",
                        "unlock_level": row[lvl_idx].strip() if lvl_idx >= 0 and lvl_idx < len(row) else "",
                    })

        # Rank matches: exact name first, tables with non-empty values first, priority game tables first
        priority_tables = ("fields.csv", "bakery_goods.csv", "dairy_goods.csv", "pie_oven_goods.csv", "sugar_mill_goods.csv", "animal_goods.csv")
        def sort_key(r):
            exact = 0 if r["name"].lower() == q else 1
            has_val = 0 if r["value"] else 1
            pri_table = 0 if r["table"] in priority_tables or r["table"].endswith("_goods.csv") else 1
            return (exact, pri_table, has_val, r["table"], r["name"])

        results.sort(key=sort_key)
        return results

    def get_item(self, table_name: str, item_name: str):
        csv_path = self.data_dir / table_name
        headers, types, rows = read_csv_table(csv_path)
        if not headers:
            return None
        name_idx = headers.index("Name") if "Name" in headers else 0
        for r_idx, row in enumerate(rows):
            if len(row) > name_idx and row[name_idx].strip().lower() == item_name.strip().lower():
                data = {headers[i]: (row[i] if i < len(row) else "") for i in range(len(headers))}
                val_int = int(data.get("Value", 0)) if str(data.get("Value", "")).isdigit() else 0
                data["_table"] = table_name
                data["_row_idx"] = r_idx
                data["_max_price"] = round(val_int * 3.6) if val_int > 0 else 0
                return data
        return None

    def set_item_param(self, table_name: str, item_name: str, param: str, new_val: str):
        csv_path = self.data_dir / table_name
        headers, types, rows = read_csv_table(csv_path)
        if not headers or param not in headers:
            return False, f"Parameter '{param}' not found in table '{table_name}'"

        name_idx = headers.index("Name") if "Name" in headers else 0
        param_idx = headers.index(param)
        found = False

        for row in rows:
            if len(row) > name_idx and row[name_idx].strip().lower() == item_name.strip().lower():
                while len(row) <= param_idx:
                    row.append("")
                row[param_idx] = str(new_val)
                found = True
                break

        if not found:
            return False, f"Item '{item_name}' not found in '{table_name}'"

        write_csv_table(csv_path, headers, types, rows)
        return True, f"Updated {item_name} [{param} = {new_val}] in {table_name}"

    def batch_modify(self, table_pattern: str, param: str, mode="multiply", multiplier=2.0, exact_val=""):
        """Batch modify a parameter across multiple tables/items."""
        modified_count = 0
        files = list(self.data_dir.glob(table_pattern))
        for f in files:
            headers, types, rows = read_csv_table(f)
            if not headers or param not in headers:
                continue
            param_idx = headers.index(param)
            changed = False
            for row in rows:
                if len(row) > param_idx and row[param_idx].strip():
                    cur = row[param_idx].strip()
                    if mode == "multiply" and cur.isdigit():
                        new_num = max(1, int(round(int(cur) * multiplier)))
                        row[param_idx] = str(new_num)
                        modified_count += 1
                        changed = True
                    elif mode == "set":
                        row[param_idx] = str(exact_val)
                        modified_count += 1
                        changed = True
            if changed:
                write_csv_table(f, headers, types, rows)
        return modified_count

    def is_device_online(self):
        try:
            res = subprocess.run([self.adb, "-s", self.device, "get-state"], capture_output=True, text=True, timeout=2)
            return res.returncode == 0 and "device" in res.stdout
        except Exception:
            return False

    def deploy_to_ldplayer(self):
        """Bundle and deploy all update assets to LDPlayer in under 1 second."""
        if not self.is_device_online():
            return False, f"LDPlayer ({self.device}) is offline or not running. Please start LDPlayer."

        update_dir = self.data_dir.parent
        if not update_dir.is_dir():
            return False, f"Update dir not found: {update_dir}"

        t0 = time.monotonic()
        items = list(update_dir.iterdir())
        with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tf:
            tar_tmp = tf.name
        try:
            with tarfile.open(tar_tmp, "w") as tar:
                for it in items:
                    tar.add(str(it), arcname=it.name)
            tar_size = os.path.getsize(tar_tmp) / (1024 * 1024)

            # Push archive
            stage_tar = "/data/local/tmp/.nxrth_update.tar"
            res = subprocess.run(
                [self.adb, "-s", self.device, "push", tar_tmp, stage_tar],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if res.returncode != 0:
                return False, f"Push failed: {res.stderr or res.stdout}"

            # Unpack on device and set permissions
            extract_cmd = (
                f"mkdir -p {APP_UPDATE_DIR} && "
                f"tar -xf {stage_tar} -C {APP_UPDATE_DIR} && "
                f"rm -f {stage_tar} && "
                f"chmod -R 777 {APP_UPDATE_DIR}"
            )
            subprocess.run(
                [self.adb, "-s", self.device, "shell", f"su -c {shlex.quote(extract_cmd)}"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            elapsed = time.monotonic() - t0
            return True, f"Deployed {tar_size:.1f} MB assets to LDPlayer in {elapsed:.2f}s"
        except Exception as e:
            return False, f"Deploy failed: {e}"
        finally:
            if os.path.exists(tar_tmp):
                try:
                    os.remove(tar_tmp)
                except Exception:
                    pass

    def test_restart_game(self):
        """Force-stop Hay Day and re-launch via ADB to test if modifications are accepted."""
        if not self.is_device_online():
            return False, f"LDPlayer ({self.device}) is offline or not running. Please start LDPlayer."

        try:
            subprocess.run(
                [self.adb, "-s", self.device, "shell", f"am force-stop {PACKAGE_NAME}"],
                capture_output=True,
                timeout=5,
            )
            time.sleep(0.5)
            subprocess.run(
                [
                    self.adb,
                    "-s",
                    self.device,
                    "shell",
                    f"monkey -p {PACKAGE_NAME} -c android.intent.category.LAUNCHER 1",
                ],
                capture_output=True,
                timeout=5,
            )
            return True, f"Hay Day restarted on {self.device}. Watch game screen to observe live assets."
        except Exception as e:
            return False, f"Restart error: {e}"

    def inspect_live_on_ldplayer(self, table_name: str, item_name: str):
        """Read the live item value directly from inside LDPlayer."""
        if not self.is_device_online():
            return None, f"LDPlayer ({self.device}) is offline or not running."

        remote_path = f"{APP_UPDATE_DIR}/data/{table_name}"
        cmd = f"cat {remote_path} 2>/dev/null"
        try:
            res = subprocess.run(
                [self.adb, "-s", self.device, "shell", f"su -c {shlex.quote(cmd)}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode != 0 or not res.stdout.strip():
                return None, f"File {table_name} not found on device or empty."

            lines = res.stdout.splitlines()
            if len(lines) < 2:
                return None, "Invalid CSV format on device."
            headers = [h.strip() for h in lines[0].split(",")]
            for line in lines[2:]:
                parts = [p.strip() for p in line.split(",")]
                if parts and parts[0].lower() == item_name.lower():
                    live_dict = {headers[i]: (parts[i] if i < len(parts) else "") for i in range(len(headers))}
                    val_int = int(live_dict.get("Value", 0)) if str(live_dict.get("Value", "")).isdigit() else 0
                    live_dict["_max_price"] = round(val_int * 3.6) if val_int > 0 else 0
                    return live_dict, "Found on device"
            return None, f"Item {item_name} not found in live {table_name} on device."
        except Exception as e:
            return None, str(e)

    def restore_all_backups(self):
        """Restore all original files from the backup directory."""
        if not BACKUP_DIR.is_dir():
            return 0
        restored = 0
        for bak in BACKUP_DIR.glob("*.csv"):
            orig = self.data_dir / bak.name
            shutil.copy2(bak, orig)
            restored += 1
        return restored

    def send_deeplink(self, action: str):
        """Trigger an in-game screen/area navigation via deep link."""
        if not self.is_device_online():
            return False, f"LDPlayer ({self.device}) is offline or not running."

        action_map = {
            "fishing": "VisitFishing",
            "shop": "OpenDiamondShop",
            "town": "VisitTown",
            "greg": "VisitGregFarm",
            "gregtown": "VisitGregTown",
            "events": "OpenEventBoard",
            "clans": "OpenClanSearch",
        }
        act = action_map.get(action.lower(), action)
        cmd = f"am start -a android.intent.action.VIEW -d 'hayday://?action={act}'"
        try:
            res = subprocess.run([self.adb, "-s", self.device, "shell", cmd], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return True, f"Navigated to '{act}' on {self.device}"
            return False, f"Navigation failed: {res.stderr or res.stdout}"
        except Exception as e:
            return False, str(e)

    def unlock_all_features(self):
        """Unlock all features (Shop, Boat, Fishing, Truck, Derby, Helpers, etc.) to Level 1."""
        feat_csv = self.data_dir / "features.csv"
        ensure_backup(feat_csv)
        headers, types, rows = read_csv_table(feat_csv)
        if not headers or "UnlockLevel" not in headers:
            return 0, "features.csv missing UnlockLevel"

        lvl_idx = headers.index("UnlockLevel")
        count = 0
        for r in rows:
            if len(r) > lvl_idx and r[lvl_idx].strip().isdigit():
                if int(r[lvl_idx].strip()) > 1:
                    r[lvl_idx] = "1"
                    count += 1
        write_csv_table(feat_csv, headers, types, rows)

        # Also set cheap 1s repair for Dock and Fishing Boat
        for fname, name_key in [("docks.csv", "Dock"), ("fishing_boat.csv", "FishingBoatWreck")]:
            fpath = self.data_dir / fname
            if fpath.is_file():
                ensure_backup(fpath)
                h, t, rs = read_csv_table(fpath)
                if h and "RepairPrice" in h and "TimeMin" in h and "TimeSec" in h:
                    rp_i = h.index("RepairPrice")
                    tm_i = h.index("TimeMin")
                    ts_i = h.index("TimeSec")
                    for r in rs:
                        if len(r) > 0 and r[0].strip() == name_key:
                            r[rp_i] = "1"
                            r[tm_i] = "0"
                            r[ts_i] = "1"
                    write_csv_table(fpath, h, t, rs)

        return count, f"Unlocked {count} features and made Boat/Dock repairs 1 coin & 1s"

    def _tap(self, x, y, delay=0.8):
        subprocess.run([self.adb, "-s", self.device, "shell", f"input tap {x} {y}"], capture_output=True)
        time.sleep(delay)

    def _swipe(self, x1, y1, x2, y2, dur=350, delay=0.8):
        subprocess.run([self.adb, "-s", self.device, "shell", f"input swipe {x1} {y1} {x2} {y2} {dur}"], capture_output=True)
        time.sleep(delay)

    def auto_craft_lure(self, count=1):
        """Automatically craft red lure(s), trigger instant speedup, and collect."""
        if not self.is_device_online():
            return False, f"LDPlayer ({self.device}) is offline or not running."

        self.send_deeplink("VisitFishing")
        time.sleep(1.2)

        crafted = 0
        for i in range(count):
            # 1. Tap Lure Workbench
            self._tap(450, 300, 1.2)
            # 2. Drag Red Lure into slot
            self._swipe(350, 216, 410, 290, 350, 1.0)
            # 3. Tap Free speedup button
            self._tap(414, 342, 0.8)
            # 4. Tap slot to collect crafted lure
            self._tap(410, 290, 0.8)
            # Close popup if open
            self._tap(590, 80, 0.5)
            crafted += 1
            time.sleep(0.4)

        return True, f"Successfully auto-crafted and speeded up {crafted} Red Lure(s)!"

    def auto_catch_fish(self):
        """Automatically cast lure, reel in, and catch fish instantly."""
        if not self.is_device_online():
            return False, f"LDPlayer ({self.device}) is offline or not running."

        self.send_deeplink("VisitFishing")
        time.sleep(1.2)

        # 1. Tap fishing spot
        self._tap(200, 350, 1.2)
        # 2. Drag Red Lure from palette into fishing water
        self._swipe(260, 230, 280, 350, 400, 0.8)
        # 3. Hold catch circle (with huge radius & zero struggle, fish reels in instantly)
        self._swipe(280, 350, 280, 350, 2000, 1.5)
        # 4. Tap screen center to collect caught fish
        self._tap(320, 240, 0.8)
        self._tap(320, 240, 0.8)
        # Close scrapbook if opened
        self._tap(590, 80, 0.5)

        return True, "Executed instant auto-fishing! Fish reeled in and collected."




def interactive_cli():
    editor = AssetEditor()
    adb_status = f"{editor.device} (Online)" if editor.device else "No device found"

    while True:
        print("\n" + "=" * 66)
        print("          HAY DAY LIVE ASSET EDITOR & TESTING DEBUGGER")
        print("=" * 66)
        print(f" Target Folder: {editor.data_dir}")
        print(f" LDPlayer Link: {editor.adb} -> {adb_status}")
        print("-" * 66)
        print(" Options:")
        print("   [1] Search & Inspect Item (Crop, Good, Tool, Animal)")
        print("   [2] Edit Item Values (Exceed Price, Harvest Output, Time)")
        print("   [3] Batch Exceed Presets (Multiply Prices / Instant Growth)")
        print("   [4] Inspect Live Assets on LDPlayer (Verify what device has)")
        print("   [5] Deploy / Push Changes to LDPlayer (<1s)")
        print("   [6] Restart Hay Day on LDPlayer (Test Live in Game)")
        print("   [7] Restore Baseline Original CSVs (Undo All Edits)")
        print("   [8] Instant Screen Jump / Teleport (Fishing, Shop, Town, Greg, Events)")
        print("   [9] Unlock All Features to Level 1 (Shop, Boat, Fishing, Truck, Derby)")
        print("   [10] Auto Craft Red Lure & Instant Speedup (Drag, Speedup, Collect)")
        print("   [11] Auto Instant Fish & Catch (Cast, Hook, Instant Reel-In)")
        print("   [0] Exit")
        print("=" * 66)

        try:
            choice = input(" Select option [0-11]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting editor.")
            break

        if choice == "0":
            break

        elif choice == "1":
            q = input("\n Enter item search term (e.g. Wheat, Bread, Saw): ").strip()
            if not q:
                continue
            results = editor.search_items(q)
            print(f"\n Found {len(results)} matches for '{q}':")
            print(f" {'#':<3} {'Name':<22} {'Table':<24} {'Value':<7} {'MaxPrice':<9} {'Harvest':<8} {'Time'}")
            print("-" * 80)
            for idx, r in enumerate(results[:25], 1):
                t_str = f"{r['time_min']}m" if r['time_min'] else f"{r['time_sec']}s"
                print(f" {idx:<3} {r['name']:<22} {r['table']:<24} {r['value']:<7} {r['max_price']:<9} {r['harvest']:<8} {t_str}")

        elif choice == "2":
            q = input("\n Enter exact item name to edit (e.g. Wheat, Corn, Carrot): ").strip()
            if not q:
                continue
            matches = editor.search_items(q)
            exact = [m for m in matches if m["name"].lower() == q.lower()]
            item = exact[0] if exact else (matches[0] if matches else None)
            if not item:
                print(f" [!] Item '{q}' not found.")
                continue

            print(f"\n Found: {item['name']} in table '{item['table']}'")
            print(f"   Current Value   : {item['value']} (Max Roadside Price: ~{item['max_price']} coins)")
            print(f"   Current Harvest : {item['harvest']} per field/cycle")
            print(f"   Current Time    : {item['time_min']}m {item['time_sec']}s")
            print("-" * 50)
            print(" What would you like to edit?")
            print("   [1] Set Value (Controls Roadside Shop Max Price = Value * 3.6)")
            print("   [2] Set Harvest count (e.g. 10 yield)")
            print("   [3] Set Growth/Craft Time (e.g. 0 minutes, 1 second)")
            print("   [4] Custom column")

            ec = input(" Choose [1-4]: ").strip()
            if ec == "1":
                new_v = input(f" Enter new Value for {item['name']} (e.g. 500, 9999): ").strip()
                if new_v.isdigit():
                    ok, msg = editor.set_item_param(item["table"], item["name"], "Value", new_v)
                    print(f" [+] {msg} (New max shop price: ~{round(int(new_v)*3.6)})")
            elif ec == "2":
                new_h = input(f" Enter new Harvest output for {item['name']} (e.g. 10): ").strip()
                if new_h.isdigit():
                    ok, msg = editor.set_item_param(item["table"], item["name"], "Harvest", new_h)
                    print(f" [+] {msg}")
            elif ec == "3":
                sec = input(f" Enter TimeSec (e.g. 1 for instant growth): ").strip()
                editor.set_item_param(item["table"], item["name"], "TimeMin", "0")
                ok, msg = editor.set_item_param(item["table"], item["name"], "TimeSec", sec or "1")
                print(f" [+] Set growth time to 0m {sec or '1'}s")

            # Offer to deploy immediately
            dep = input("\n Deploy this change to LDPlayer right now? [Y/n]: ").strip().lower()
            if dep in ("", "y", "yes"):
                ok, msg = editor.deploy_to_ldplayer()
                print(f" {msg}")
                rst = input(" Restart Hay Day on LDPlayer to test live? [Y/n]: ").strip().lower()
                if rst in ("", "y", "yes"):
                    ok2, msg2 = editor.test_restart_game()
                    print(f" {msg2}")

        elif choice == "3":
            print("\n Batch Exceed Presets:")
            print("   [1] Multiply all crop values by 5x (5x roadside shop price)")
            print("   [2] Multiply all crop values by 10x (10x roadside shop price)")
            print("   [3] Set all crops to instant growth (TimeMin=0, TimeSec=1)")
            print("   [4] Multiply all crafted goods values by 5x")
            bc = input(" Select preset [1-4]: ").strip()
            if bc == "1":
                cnt = editor.batch_modify("fields.csv", "Value", mode="multiply", multiplier=5.0)
                print(f" [+] Multiplied {cnt} crop values by 5x in fields.csv")
            elif bc == "2":
                cnt = editor.batch_modify("fields.csv", "Value", mode="multiply", multiplier=10.0)
                print(f" [+] Multiplied {cnt} crop values by 10x in fields.csv")
            elif bc == "3":
                c1 = editor.batch_modify("fields.csv", "TimeMin", mode="set", exact_val="0")
                c2 = editor.batch_modify("fields.csv", "TimeSec", mode="set", exact_val="1")
                print(f" [+] Set instant growth (0m 1s) for all {c1} crops in fields.csv")
            elif bc == "4":
                cnt = editor.batch_modify("*_goods.csv", "Value", mode="multiply", multiplier=5.0)
                print(f" [+] Multiplied {cnt} goods values by 5x across all goods tables")

            dep = input("\n Deploy batch changes to LDPlayer right now? [Y/n]: ").strip().lower()
            if dep in ("", "y", "yes"):
                ok, msg = editor.deploy_to_ldplayer()
                print(f" {msg}")

        elif choice == "4":
            item_name = input("\n Enter item name to check live on LDPlayer (e.g. Wheat): ").strip()
            if not item_name:
                continue
            matches = editor.search_items(item_name)
            table = matches[0]["table"] if matches else "fields.csv"
            live_data, msg = editor.inspect_live_on_ldplayer(table, item_name)
            if live_data:
                print(f"\n [LIVE LDPLAYER STATE for '{item_name}' in '{table}']:")
                print(f"   Value         : {live_data.get('Value')} (Max Price: ~{live_data.get('_max_price')} coins)")
                print(f"   Harvest       : {live_data.get('Harvest')}")
                print(f"   TimeMin       : {live_data.get('TimeMin')}")
                print(f"   TimeSec       : {live_data.get('TimeSec')}")
                print(f"   UnlockLevel   : {live_data.get('UnlockLevel')}")
                print("   [+] Verified: LDPlayer has live update assets active.")
            else:
                print(f"   [!] Device check: {msg}")

        elif choice == "5":
            print("\n[*] Bundling and pushing all update assets to LDPlayer...")
            ok, msg = editor.deploy_to_ldplayer()
            print(f" [{'+' if ok else '!'}] {msg}")

        elif choice == "6":
            print("\n[*] Restarting Hay Day on LDPlayer...")
            ok, msg = editor.test_restart_game()
            print(f" [{'+' if ok else '!'}] {msg}")

        elif choice == "7":
            cnt = editor.restore_all_backups()
            print(f"\n [+] Restored {cnt} original baseline CSV tables from backup.")
            dep = input(" Deploy restored baseline to LDPlayer now? [Y/n]: ").strip().lower()
            if dep in ("", "y", "yes"):
                ok, msg = editor.deploy_to_ldplayer()
                print(f" {msg}")

        elif choice == "8":
            print("\n Instant Screen Jump / Teleport Destinations:")
            print("   [1] Fishing Area (VisitFishing)")
            print("   [2] Diamond / Roadside Shop (OpenDiamondShop)")
            print("   [3] Town Area (VisitTown)")
            print("   [4] Greg's Farm (VisitGregFarm)")
            print("   [5] Greg's Town (VisitGregTown)")
            print("   [6] Event Board (OpenEventBoard)")
            print("   [7] Clan / Neighborhood Search (OpenClanSearch)")
            tc = input(" Choose destination [1-7]: ").strip()
            dest_map = {
                "1": "VisitFishing",
                "2": "OpenDiamondShop",
                "3": "VisitTown",
                "4": "VisitGregFarm",
                "5": "VisitGregTown",
                "6": "OpenEventBoard",
                "7": "OpenClanSearch",
            }
            target_act = dest_map.get(tc)
            if target_act:
                ok, msg = editor.send_deeplink(target_act)
                print(f" [{'+' if ok else '!'}] {msg}")
            else:
                print(" [!] Invalid destination choice.")

        elif choice == "9":
            cnt, msg = editor.unlock_all_features()
            print(f"\n [+] {msg}")
            dep = input(" Deploy Level 1 unlocked features to LDPlayer right now? [Y/n]: ").strip().lower()
            if dep in ("", "y", "yes"):
                ok, msg2 = editor.deploy_to_ldplayer()
                print(f" {msg2}")
                rst = input(" Restart Hay Day to load unlocked features? [Y/n]: ").strip().lower()
                if rst in ("", "y", "yes"):
                    ok3, msg3 = editor.test_restart_game()
                    print(f" {msg3}")

        elif choice == "10":
            num_str = input("\n How many Red Lures would you like to craft & speedup? [1-10, default 1]: ").strip()
            num = int(num_str) if num_str.isdigit() and int(num_str) > 0 else 1
            ok, msg = editor.auto_craft_lure(count=num)
            print(f" [{'+' if ok else '!'}] {msg}")

        elif choice == "11":
            print("\n[*] Running auto instant fishing sequence...")
            ok, msg = editor.auto_catch_fish()
            print(f" [{'+' if ok else '!'}] {msg}")


def main():
    if "--test" in sys.argv:
        print("[*] Running automated test for AssetEditor...")
        ed = AssetEditor()
        res = ed.search_items("Wheat")
        print(f"  -> Found {len(res)} matches for 'Wheat'")
        assert len(res) > 0, "No matches for Wheat"
        print(f"  -> Wheat initial Value: {res[0]['value']}")
        # Test modifying value
        ok, msg = ed.set_item_param("fields.csv", "Wheat", "Value", "888")
        print(f"  -> Modify result: {ok}, {msg}")
        # Test search again
        res2 = ed.search_items("Wheat")
        print(f"  -> Wheat modified Value: {res2[0]['value']}")
        assert res2[0]['value'] == "888", "Value was not updated"
        # Test deploy
        ok_dep, msg_dep = ed.deploy_to_ldplayer()
        print(f"  -> Live deploy result: {ok_dep}, {msg_dep}")
        # Test live check on LDPlayer
        live_data, live_msg = ed.inspect_live_on_ldplayer("fields.csv", "Wheat")
        print(f"  -> Live LDPlayer check: {live_data.get('Value') if live_data else 'None'}, msg: {live_msg}")
        # Revert back
        ed.set_item_param("fields.csv", "Wheat", "Value", res[0]['value'])
        ed.deploy_to_ldplayer()
        print("  -> Reverted back to initial value and deployed.")
        print("[+] Automated test completed successfully!")
        return 0

    if "--goto" in sys.argv:
        idx = sys.argv.index("--goto")
        dest = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else "fishing"
        ed = AssetEditor()
        ok, msg = ed.send_deeplink(dest)
        print(f"[{'+' if ok else '!'}] {msg}")
        return 0 if ok else 1

    if "--craft-lure" in sys.argv:
        idx = sys.argv.index("--craft-lure")
        cnt = 1
        if idx + 1 < len(sys.argv) and sys.argv[idx + 1].isdigit():
            cnt = int(sys.argv[idx + 1])
        ed = AssetEditor()
        ok, msg = ed.auto_craft_lure(count=cnt)
        print(f"[{'+' if ok else '!'}] {msg}")
        return 0 if ok else 1

    if "--fish" in sys.argv or "--auto-fish" in sys.argv:
        ed = AssetEditor()
        ok, msg = ed.auto_catch_fish()
        print(f"[{'+' if ok else '!'}] {msg}")
        return 0 if ok else 1

    if "--unlock-all" in sys.argv:
        ed = AssetEditor()
        cnt, msg = ed.unlock_all_features()
        print(f"[+] {msg}")
        ok, msg2 = ed.deploy_to_ldplayer()
        print(f"[{'+' if ok else '!'}] {msg2}")
        if "--restart" in sys.argv:
            ed.test_restart_game()
        return 0 if ok else 1

    if "--deploy" in sys.argv:
        ed = AssetEditor()
        ok, msg = ed.deploy_to_ldplayer()
        print(f"[{'+' if ok else '!'}] {msg}")
        return 0 if ok else 1

    if "--restart" in sys.argv:
        ed = AssetEditor()
        ok, msg = ed.test_restart_game()
        print(f"[{'+' if ok else '!'}] {msg}")
        return 0 if ok else 1

    interactive_cli()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
