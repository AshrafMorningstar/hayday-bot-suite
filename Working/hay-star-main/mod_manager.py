#!/usr/bin/env python3
"""
=============================================================================
Hay Star Game Assets & Mod Staging Engine
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Manages, patches, and stages modded asset files into the emulator's Hay Day 
installation (/data/data/com.supercell.hayday/update/) with SHA-1 fingerprinting.
Matches the 10 game asset mod selection modes displayed in the launcher menu.
=============================================================================
"""

import os
import sys
import json
import shutil
import hashlib
import subprocess
import time
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent
MODS_SRC_DIR = WORKSPACE_ROOT / "Assest" / "mods"
STOCK_SRC_DIR = WORKSPACE_ROOT / "Assest" / "stock_clean"
STAGE_CACHE_DIR = WORKSPACE_ROOT / "stage_cache"

MOD_MODES = {
    "1": {
        "id": "mod_01_decision_box",
        "title": "Decision Box / Shop Rewards",
        "description": "Decision Box & Shop mystery rewards boost",
        "csv_files": ["decision_box.csv", "catalogue_gifts.csv", "catalogue_layout.csv"]
    },
    "2": {
        "id": "mod_02_mystery_boxes",
        "title": "Mystery Boxes & Calendar",
        "description": "Mystery Boxes & Calendar event drop multipliers",
        "csv_files": ["mystery_boxes.csv", "mystery_box_spawners.csv", "calendar_events.csv", "calendar_event_rewards.csv", "calendar_event_gift_box.csv"]
    },
    "3": {
        "id": "mod_03_greg_shop",
        "title": "Greg Roadside Shop Inventory",
        "description": "Greg Roadside Shop inventory & Tom lowest price (< $10)",
        "csv_files": ["roadside_shop.csv", "boy.csv", "boy_box.csv"]
    },
    "4": {
        "id": "mod_04_storage_expansion",
        "title": "Barn, Silo & Tackle Box Expansion",
        "description": "Barn, Silo & Tackle Box storage upgrade requirements",
        "csv_files": ["warehouses.csv", "silos.csv", "silo_pricing.csv", "tackle_box.csv", "expansions.csv"]
    },
    "5": {
        "id": "mod_05_truck_boat_orders",
        "title": "Truck & Boat Predefined Orders",
        "description": "Truck & Boat predefined high-reward orders & faster delivery",
        "csv_files": ["predefined_orders.csv", "predefined_boat_orders.csv", "cars.csv", "order_track_configs.csv", "order_tables.csv"]
    },
    "6": {
        "id": "mod_06_animal_pet_feed",
        "title": "Animal Feed Times & Pet Houses",
        "description": "Fast animal feed cycles & pet house instant wake-up (All feeds to Wheat)",
        "csv_files": ["animals.csv", "animal_feed.csv", "pets.csv", "baby_pets.csv", "pet_habitats.csv", "sanctuary_animal_habitats.csv"]
    },
    "7": {
        "id": "mod_07_valley_fuel_spin",
        "title": "Valley Fuel & Map Game Config",
        "description": "Valley Fuel unlimited spin, map rewards & bonus coins",
        "csv_files": ["mapgame_config.csv", "mapgame_reward_sets.csv", "mapgame_coins.csv", "mapgame_daily_quests_progression.csv"]
    },
    "8": {
        "id": "mod_08_personal_quests",
        "title": "Birthday Events & Farm Pass",
        "description": "Birthday events, Farm Pass road rewards & perk unlock",
        "csv_files": ["farm_pass_road.csv", "farm_pass_perks.csv", "farm_pass_tasks.csv", "events.csv", "eventboard.csv"]
    },
    "9": {
        "id": "mod_09_wheel_of_fortune",
        "title": "Daily Wheel of Fortune Rewards",
        "description": "Daily Wheel of Fortune high tier loot & jackpots",
        "csv_files": ["wheel_cars.csv", "weighted_reward_groups.csv"]
    },
    "10": {
        "id": "mod_10_seasonal_and_diamonds",
        "title": "Seasonal Catalogue Gifts & Diamonds",
        "description": "Seasonal catalogue gifts, milestone claims & diamond rewards",
        "csv_files": ["seasonal_catalogue_gifts.csv", "diamond_packages.csv", "cash_packages.csv", "seasonal_currencies.csv"]
    }
}

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

def compute_sha1(filepath):
    sha = hashlib.sha1()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()

def update_fingerprint_file(stage_update_dir):
    """Computes SHA1 hashes for all files in update directory and saves fingerprint.json."""
    fingerprint_path = stage_update_dir / "fingerprint.json"
    files_list = []
    
    data_dir = stage_update_dir / "data"
    if data_dir.exists():
        for f in data_dir.glob("*.csv"):
            rel_path = f"data/{f.name}"
            files_list.append({"file": rel_path, "sha": compute_sha1(f)})
            
    loc_dir = stage_update_dir / "localization"
    if loc_dir.exists():
        for f in loc_dir.glob("*.csv"):
            rel_path = f"localization/{f.name}"
            files_list.append({"file": rel_path, "sha": compute_sha1(f)})
            
    fp_data = {
        "files": files_list,
        "sha": hashlib.sha1(str(time.time()).encode()).hexdigest(),
        "version": "1.0.0"
    }
    
    with open(fingerprint_path, "w", encoding="utf-8") as out:
        json.dump(fp_data, out, indent=2)
    return fingerprint_path

def prepare_stage_directory(selected_modes):
    """
    Creates a staging directory with base assets and overlays selected mods.
    selected_modes: list of mode keys ('1'..'10', 'A', '0')
    """
    if STAGE_CACHE_DIR.exists():
        shutil.rmtree(STAGE_CACHE_DIR)
    STAGE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    stage_update = STAGE_CACHE_DIR / "update"
    stage_data = stage_update / "data"
    stage_loc = stage_update / "localization"
    stage_data.mkdir(parents=True, exist_ok=True)
    stage_loc.mkdir(parents=True, exist_ok=True)
    
    # 1. Base files from Stock Clean if exists
    stock_update = STOCK_SRC_DIR / "update"
    if stock_update.exists():
        stock_data = stock_update / "data"
        if stock_data.exists():
            for f in stock_data.glob("*.csv"):
                shutil.copy2(f, stage_data / f.name)
        stock_loc = stock_update / "localization"
        if stock_loc.exists():
            for f in stock_loc.glob("*.csv"):
                shutil.copy2(f, stage_loc / f.name)
    
    # If mode is '0' (Stock Clean), do not apply any mods
    if "0" in selected_modes:
        print("[*] Staging Mode [0]: Clean Vanilla Stock Assets...")
        update_fingerprint_file(stage_update)
        return stage_update

    # 2. Determine target CSVs to overlay from mods
    mods_update = MODS_SRC_DIR / "update"
    mods_data = mods_update / "data"
    mods_loc = mods_update / "localization"
    
    if "A" in selected_modes or "ALL" in selected_modes:
        print("[*] Staging Mode [A]: Applying ALL 10 Mods...")
        if mods_data.exists():
            for f in mods_data.glob("*.csv"):
                shutil.copy2(f, stage_data / f.name)
        if mods_loc.exists():
            for f in mods_loc.glob("*.csv"):
                shutil.copy2(f, stage_loc / f.name)
    else:
        applied_files = set()
        for mode_key in selected_modes:
            mode_info = MOD_MODES.get(str(mode_key).strip())
            if not mode_info:
                continue
            print(f"[*] Staging Mode [{mode_key}]: {mode_info['title']}...")
            for csv_name in mode_info["csv_files"]:
                src_csv = mods_data / csv_name
                if src_csv.exists():
                    shutil.copy2(src_csv, stage_data / csv_name)
                    applied_files.add(csv_name)
        print(f"[*] Total modded CSVs applied: {len(applied_files)}")
        
    update_fingerprint_file(stage_update)
    return stage_update

def stage_to_device(selected_modes, adb_path=None):
    """
    Stages prepared mod assets directly into LDPlayer (/data/data/com.supercell.hayday/update/)
    """
    adb = adb_path or locate_adb()
    stage_update = prepare_stage_directory(selected_modes)
    
    print(f"[*] Connecting to Android emulator via ADB: {adb}")
    # Verify device
    dev_res = subprocess.run([adb, "devices"], capture_output=True, text=True)
    if "device" not in dev_res.stdout:
        print("[!] Warning: No active emulator device detected on ADB.")
        return False

    target_update_dir = "/data/data/com.supercell.hayday/update"
    target_data_dir = f"{target_update_dir}/data"
    target_loc_dir = f"{target_update_dir}/localization"
    
    print("[*] Stopping game process to safely stage assets...")
    subprocess.run([adb, "shell", "am", "force-stop", "com.supercell.hayday"], capture_output=True, timeout=5)
    time.sleep(1)

    print("[*] Creating remote update directory structure...")
    subprocess.run([adb, "shell", f"su 0 sh -c 'mkdir -p {target_data_dir} {target_loc_dir}'"], capture_output=True, timeout=5)

    print("[*] Pushing fingerprint.json and modded assets in batch...")
    subprocess.run([adb, "push", str(stage_update), "/data/local/tmp/"], capture_output=True, timeout=15)
    subprocess.run([adb, "shell", f"su 0 sh -c 'cp -r /data/local/tmp/update/* {target_update_dir}/'"], capture_output=True, timeout=10)

    # Fix permissions
    print("[*] Setting filesystem permissions on Android...")
    subprocess.run([adb, "shell", f"su 0 sh -c 'chmod -R 777 {target_update_dir}'"], capture_output=True, timeout=5)
    print("[+] Assets and mods successfully staged into Hay Day!")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("[*] Testing mod staging directory creation...")
        stage_dir = prepare_stage_directory(["1", "2", "3"])
        print(f"[+] Prepared staging directory: {stage_dir}")
        print(f"[+] Fingerprint exists: {(stage_dir / 'fingerprint.json').exists()}")
        print(f"[+] Data CSV count: {len(list((stage_dir / 'data').glob('*.csv')))}")
    elif len(sys.argv) > 1:
        stage_to_device(sys.argv[1:])
    else:
        print("Usage: python mod_manager.py <mode_num> or --test")
