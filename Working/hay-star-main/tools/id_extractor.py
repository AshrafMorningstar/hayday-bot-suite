#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Global ID Auto-Extractor from Game Asset Pack
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Automatically scans ALL 378+ CSV files in install_time_asset_pack/assets/data/
and extracts every Global ID found. Outputs organized per-category files.
=============================================================================
"""

import os
import sys
import csv
import json
import re
from pathlib import Path
from collections import defaultdict

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
ASSET_DATA_DIR = WORKSPACE_ROOT / "install_time_asset_pack" / "assets" / "data"
OUTPUT_DIR = Path(__file__).resolve().parent / "extracted_ids"

# Global ID class ranges based on Supercell Titan engine
CLASS_RANGES = {
    4:  "Crops & Seeds",
    6:  "Animal Feeds",
    7:  "Fishing Items",
    8:  "Sanctuary Items",
    11: "Goods, Recipes & Harvests",
    13: "Buildings, Machines & Structures",
    14: "Decorations",
    15: "Obstacles & Terrain",
    18: "Tools & Expansion Materials",
    23: "Livestock Animals",
    30: "Farm Config Items",
    98: "Fishing Lures & Nets",
}

def classify_id(global_id):
    """Determine the class/category of a Global ID."""
    if global_id < 100000:
        return None  # Too small, likely not a Global ID
    class_id = global_id // 1000000
    if class_id in CLASS_RANGES:
        return class_id, CLASS_RANGES[class_id]
    instance = global_id % 1000000
    if instance > 50000:
        return None  # Likely not a real ID
    return class_id, f"Unknown Class {class_id}"


def extract_ids_from_csv(csv_path):
    """Extract potential Global IDs from a single CSV file."""
    found_ids = []
    try:
        with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            headers = None
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    headers = row
                    continue
                for col_idx, cell in enumerate(row):
                    cell = cell.strip()
                    if not cell:
                        continue
                    # Check if cell looks like a Global ID (6-7 digit number)
                    if re.match(r'^\d{6,7}$', cell):
                        try:
                            val = int(cell)
                            classification = classify_id(val)
                            if classification:
                                col_name = headers[col_idx] if headers and col_idx < len(headers) else f"col_{col_idx}"
                                found_ids.append({
                                    "id": val,
                                    "class_id": classification[0],
                                    "class_name": classification[1],
                                    "source_file": csv_path.name,
                                    "column": col_name,
                                    "row": row_num + 1,
                                })
                        except (ValueError, TypeError):
                            pass
    except Exception as e:
        print(f"  [!] Error reading {csv_path.name}: {e}")
    return found_ids


def extract_names_from_csv(csv_path):
    """Try to extract ID-to-name mappings from CSVs that have both."""
    name_map = {}
    try:
        with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            headers = None
            id_col = None
            name_col = None
            for row_num, row in enumerate(reader):
                if row_num == 0:
                    headers = [h.strip().lower() for h in row]
                    # Find ID and Name columns
                    for i, h in enumerate(headers):
                        if h in ("globalid", "global_id", "id", "tid", "itemid", "item_id", "globalid "):
                            id_col = i
                        if h in ("name", "tid", "exportname", "exportnameconvention", "tidname"):
                            if name_col is None:
                                name_col = i
                    continue
                if id_col is not None and name_col is not None and id_col < len(row) and name_col < len(row):
                    cell_id = row[id_col].strip()
                    cell_name = row[name_col].strip()
                    if cell_id and cell_name and re.match(r'^\d{6,7}$', cell_id):
                        name_map[int(cell_id)] = cell_name
    except Exception:
        pass
    return name_map


def run_extraction():
    """Main extraction pipeline."""
    print("=" * 70)
    print("  HAY DAY GLOBAL ID AUTO-EXTRACTOR")
    print("  Scanning install_time_asset_pack/assets/data/")
    print("=" * 70)

    if not ASSET_DATA_DIR.exists():
        print(f"\n[!] Asset data directory not found: {ASSET_DATA_DIR}")
        print("[!] Make sure install_time_asset_pack is in the project root.")
        return False

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(ASSET_DATA_DIR.glob("*.csv"))
    print(f"\n[*] Found {len(csv_files)} CSV files to scan.\n")

    all_ids = []
    all_names = {}
    files_processed = 0

    for csv_file in csv_files:
        ids = extract_ids_from_csv(csv_file)
        names = extract_names_from_csv(csv_file)
        all_ids.extend(ids)
        all_names.update(names)
        files_processed += 1
        if ids:
            print(f"  [+] {csv_file.name}: {len(ids)} IDs found")

    # Deduplicate by ID value
    unique_ids = {}
    for entry in all_ids:
        gid = entry["id"]
        if gid not in unique_ids:
            unique_ids[gid] = entry

    # Organize by class
    by_class = defaultdict(list)
    for gid, entry in sorted(unique_ids.items()):
        by_class[entry["class_name"]].append(entry)

    print(f"\n{'=' * 70}")
    print(f"  EXTRACTION COMPLETE")
    print(f"  Files scanned: {files_processed}")
    print(f"  Total unique Global IDs found: {len(unique_ids)}")
    print(f"  ID-to-Name mappings found: {len(all_names)}")
    print(f"{'=' * 70}\n")

    # --- Write output files ---

    # 1. all_global_ids.json
    json_out = OUTPUT_DIR / "all_global_ids.json"
    json_data = {
        "metadata": {
            "total_ids": len(unique_ids),
            "total_named": len(all_names),
            "files_scanned": files_processed,
            "source": str(ASSET_DATA_DIR),
        },
        "ids_by_category": {},
        "name_map": {str(k): v for k, v in sorted(all_names.items())},
    }
    for class_name, entries in sorted(by_class.items()):
        json_data["ids_by_category"][class_name] = [
            {"id": e["id"], "name": all_names.get(e["id"], ""), "source": e["source_file"], "column": e["column"]}
            for e in entries
        ]
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    print(f"  [+] Written: {json_out}")

    # 2. all_global_ids.txt (human readable)
    txt_out = OUTPUT_DIR / "all_global_ids.txt"
    with open(txt_out, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("  HAY DAY - COMPLETE AUTO-EXTRACTED GLOBAL ID DATABASE\n")
        f.write(f"  Total IDs: {len(unique_ids)} | Named: {len(all_names)} | Files: {files_processed}\n")
        f.write("=" * 70 + "\n\n")
        for class_name, entries in sorted(by_class.items()):
            f.write(f"\n{'─' * 60}\n")
            f.write(f"  {class_name} ({len(entries)} IDs)\n")
            f.write(f"{'─' * 60}\n")
            for e in entries:
                name = all_names.get(e["id"], "")
                name_str = f" = {name}" if name else ""
                f.write(f"  {e['id']:<10}{name_str:<35} (from {e['source_file']})\n")
    print(f"  [+] Written: {txt_out}")

    # 3. Per-category files
    category_file_map = {
        "Crops & Seeds": "crops.txt",
        "Animal Feeds": "feeds.txt",
        "Goods, Recipes & Harvests": "recipes.txt",
        "Buildings, Machines & Structures": "buildings.txt",
        "Tools & Expansion Materials": "tools.txt",
        "Livestock Animals": "animals.txt",
        "Decorations": "decorations.txt",
        "Fishing Items": "fishing.txt",
    }
    for class_name, filename in category_file_map.items():
        if class_name in by_class:
            cat_out = OUTPUT_DIR / filename
            with open(cat_out, "w", encoding="utf-8") as f:
                f.write(f"  {class_name}\n")
                f.write("=" * 50 + "\n")
                for e in by_class[class_name]:
                    name = all_names.get(e["id"], "")
                    name_str = f" = {name}" if name else ""
                    f.write(f"  {e['id']:<10}{name_str}\n")
            print(f"  [+] Written: {cat_out}")

    print(f"\n[*] All output files saved to: {OUTPUT_DIR}")
    print("[*] Extraction finished successfully!\n")
    return True


if __name__ == "__main__":
    run_extraction()
