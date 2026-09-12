#!/usr/bin/env python3
"""
Comprehensive Hay Day Global IDs & Game Objects Extractor.
Extracts all official IDs, types, names, unlock levels, prices, and parameters
from Supercell CSV data tables.
"""

import csv
import json
import os
from pathlib import Path

DATA_DIR = Path(r"C:\Users\Admin\Documents\old bots\inxernal-main ggv\com.supercell.hayday\HAY_STAR\update\data")
OUTPUT_JSON = Path(__file__).resolve().parent.parent / "game_global_ids.json"
OUTPUT_MD = Path(__file__).resolve().parent.parent / "GAME_GLOBAL_IDS.md"

def read_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        for p in DATA_DIR.iterdir():
            if p.name.lower() == filename.lower():
                path = p
                break
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8-sig", errors="ignore") as f:
        reader = list(csv.reader(f))
    if len(reader) < 2:
        return None
    headers = [h.strip() for h in reader[0]]
    rows = []
    for r in reader[2:]:
        if not r or not r[0].strip():
            continue
        row_dict = {}
        for idx, val in enumerate(r):
            if idx < len(headers):
                row_dict[headers[idx]] = val.strip()
        rows.append(row_dict)
    return rows

def parse_int(val, default=0):
    try:
        return int(val) if val else default
    except ValueError:
        return default

def main():
    if not DATA_DIR.exists():
        print(f"[!] Data directory not found: {DATA_DIR}")
        return

    db = {
        "metadata": {
            "title": "Hay Day Global In-Game Definitions & IDs Database",
            "version": "1.72.2",
            "source": "Supercell CSV Logic Tables",
            "formula": "GlobalID = ClassID * 1000000 + InstanceID (Type 4 Fields = 400000 + idx)"
        },
        "crops_and_fields": [],
        "production_buildings": [],
        "storage_and_infrastructure": [],
        "farm_animals": [],
        "animal_products": [],
        "expansion_and_upgrade_materials": [],
        "clearing_and_mining_tools": [],
        "fruit_trees_and_bushes": [],
        "boats_and_fishing": [],
        "trucks_and_orders": [],
        "town_and_trains": [],
        "crafted_goods_and_products": []
    }

    # 1. Crops & Fields (Class 4)
    rows = read_csv("fields.csv")
    if rows:
        for idx, r in enumerate(rows):
            name = r.get("Name", "")
            time_sec = parse_int(r.get("TimeSec", 0)) + parse_int(r.get("TimeMin", 0)) * 60
            db["crops_and_fields"].append({
                "global_id": 400000 + idx,
                "class_id": 4,
                "instance_id": idx,
                "name": name,
                "level": parse_int(r.get("UnlockLevel", 1)),
                "grow_time_seconds": time_sec,
                "harvest_yield": parse_int(r.get("Harvest", 2)),
                "xp": parse_int(r.get("ExpCollect", 0)),
                "max_price": parse_int(r.get("Price", 0)),
                "diamond_price": parse_int(r.get("DiamondPrice", 0)),
                "tid": r.get("TID", "")
            })

    # 2. Production & Processing Buildings (Class 6)
    rows = read_csv("processing_buildings.csv")
    if rows:
        for idx, r in enumerate(rows):
            name = r.get("Name", "")
            build_time = parse_int(r.get("TimeSec", 0)) + parse_int(r.get("TimeMin", 0)) * 60
            db["production_buildings"].append({
                "global_id": 600000 + idx,
                "class_id": 6,
                "instance_id": idx,
                "name": name,
                "level": parse_int(r.get("UnlockLevel", 1)),
                "build_cost_coins": parse_int(r.get("Price", 0)),
                "build_time_seconds": build_time,
                "slots": parse_int(r.get("Slots", 2)),
                "width": parse_int(r.get("TileWidth", 3)),
                "height": parse_int(r.get("TileHeight", 3)),
                "tid": r.get("TID", "")
            })

    # 3. Storage & Infrastructure
    infra = [
        ("silos.csv", "Silo (Crops)", 610001, "Silo storage for crops and fruits"),
        ("warehouses.csv", "Barn (Items)", 610002, "Barn storage for animal goods, tools, and products"),
        ("roadside_shop.csv", "Roadside Shop", 610003, "Roadside Shop marketplace for selling items"),
    ]
    for fn, name, gid, desc in infra:
        r = read_csv(fn)
        db["storage_and_infrastructure"].append({
            "global_id": gid,
            "name": name,
            "description": desc,
            "details": r[0] if r else {}
        })

    # 4. Farm Animals (Class 8)
    rows = read_csv("animals.csv")
    if rows:
        for idx, r in enumerate(rows):
            db["farm_animals"].append({
                "global_id": 800000 + idx,
                "class_id": 8,
                "instance_id": idx,
                "name": r.get("Name", ""),
                "habitat": r.get("Habitat", ""),
                "price": parse_int(r.get("Price", 0)),
                "level": parse_int(r.get("UnlockLevel", 1)),
                "tid": r.get("TID", "")
            })

    # 5. Animal Products
    rows = read_csv("animal_goods.csv")
    if rows:
        for idx, r in enumerate(rows):
            produce_time = parse_int(r.get("TimeSec", 0)) + parse_int(r.get("TimeMin", 0)) * 60
            db["animal_products"].append({
                "global_id": 810000 + idx,
                "name": r.get("Name", ""),
                "level": parse_int(r.get("UnlockLevel", 1)),
                "produce_time_seconds": produce_time,
                "xp": parse_int(r.get("ExpCollect", 0)),
                "max_price": parse_int(r.get("Price", 0)),
                "tid": r.get("TID", "")
            })

    # 6. Expansion & Upgrade Materials
    rows = read_csv("collection_tools.csv")
    if rows:
        for idx, r in enumerate(rows):
            db["expansion_and_upgrade_materials"].append({
                "global_id": 1410000 + idx,
                "name": r.get("Name", ""),
                "level": parse_int(r.get("UnlockLevel", 1)),
                "max_price": parse_int(r.get("MaxPrice", 0)),
                "diamond_cost": parse_int(r.get("DiamondPrice", 0)),
                "category": "Expansion & Building Upgrade Material"
            })

    # 7. Clearing & Mining Tools (Class 14)
    rows = read_csv("tools.csv")
    if rows:
        for idx, r in enumerate(rows):
            db["clearing_and_mining_tools"].append({
                "global_id": 1400000 + idx,
                "class_id": 14,
                "instance_id": idx,
                "name": r.get("Name", ""),
                "level": parse_int(r.get("UnlockLevel", 1)),
                "max_price": parse_int(r.get("MaxPrice", 0)),
                "diamond_cost": parse_int(r.get("DiamondPrice", 0)),
                "tid": r.get("TID", "")
            })

    # 8. Fruit Trees & Bushes (Class 10)
    rows = read_csv("fruit_trees.csv")
    if rows:
        for idx, r in enumerate(rows):
            grow_time = parse_int(r.get("TimeSec", 0)) + parse_int(r.get("TimeMin", 0)) * 60
            db["fruit_trees_and_bushes"].append({
                "global_id": 1000000 + idx,
                "class_id": 10,
                "instance_id": idx,
                "name": r.get("Name", ""),
                "level": parse_int(r.get("UnlockLevel", 1)),
                "price": parse_int(r.get("Price", 0)),
                "grow_time_seconds": grow_time,
                "harvests_before_dry": parse_int(r.get("Harvests", 3)),
                "tid": r.get("TID", "")
            })

    # 9. Boats & Fishing
    boat_r = read_csv("boats.csv")
    if boat_r:
        for idx, r in enumerate(boat_r):
            db["boats_and_fishing"].append({
                "global_id": 2000000 + idx,
                "name": f"Cargo River Boat: {r.get('Name', '')}",
                "level": parse_int(r.get("UnlockLevel", 17)),
                "category": "Cargo Boat"
            })
    fboat_r = read_csv("fishing_boat.csv")
    if fboat_r:
        for idx, r in enumerate(fboat_r):
            db["boats_and_fishing"].append({
                "global_id": 2010000 + idx,
                "name": f"Fishing Boat: {r.get('Name', '')}",
                "level": parse_int(r.get("UnlockLevel", 27)),
                "category": "Fishing Boat"
            })
    farea_r = read_csv("fishing_areas.csv")
    if farea_r:
        for idx, r in enumerate(farea_r):
            db["boats_and_fishing"].append({
                "global_id": 2020000 + idx,
                "name": f"Fishing Lake Spot: {r.get('Name', '')}",
                "level": parse_int(r.get("UnlockLevel", 27)),
                "category": "Fishing Area"
            })
    net_r = read_csv("nets.csv")
    if net_r:
        for idx, r in enumerate(net_r):
            db["boats_and_fishing"].append({
                "global_id": 2030000 + idx,
                "name": f"Fishing Net/Trap: {r.get('Name', '')}",
                "level": parse_int(r.get("UnlockLevel", 27)),
                "category": "Net / Trap"
            })

    # 10. Trucks & Delivery Orders
    rows = read_csv("orders.csv")
    if rows:
        for idx, r in enumerate(rows):
            db["trucks_and_orders"].append({
                "global_id": 700000 + idx,
                "name": r.get("Name", ""),
                "description": f"Truck Delivery Customer: {r.get('Name', '')}",
                "category": "Truck Order Board"
            })

    # 11. Town & Personal Train
    rows = read_csv("service_buildings.csv")
    if rows:
        for idx, r in enumerate(rows):
            db["town_and_trains"].append({
                "global_id": 1800000 + idx,
                "name": r.get("Name", ""),
                "category": "Town Service Building",
                "level": parse_int(r.get("UnlockLevel", 34)),
                "cost_coins": parse_int(r.get("Price", 0))
            })
    t_rows = read_csv("train.csv")
    if t_rows:
        for idx, r in enumerate(t_rows):
            db["town_and_trains"].append({
                "global_id": 1810000 + idx,
                "name": f"EGGspress Train: {r.get('Name', '')}",
                "category": "Town Train Transport"
            })

    # 12. Crafted Goods & Products (Class 12)
    goods_files = [f for f in os.listdir(DATA_DIR) if f.endswith("_goods.csv") and f != "animal_goods.csv"]
    goods_counter = 0
    for gf in sorted(goods_files):
        building_source = gf.replace("_goods.csv", "").replace("_", " ").title()
        rows = read_csv(gf)
        if not rows:
            continue
        for r in rows:
            name = r.get("Name", "")
            if not name:
                continue
            cook_time = parse_int(r.get("TimeSec", 0)) + parse_int(r.get("TimeMin", 0)) * 60
            db["crafted_goods_and_products"].append({
                "global_id": 1200000 + goods_counter,
                "class_id": 12,
                "instance_id": goods_counter,
                "name": name,
                "building": building_source,
                "level": parse_int(r.get("UnlockLevel", 1)),
                "produce_time_seconds": cook_time,
                "xp": parse_int(r.get("ExpCollect", 0)),
                "max_price": parse_int(r.get("Price", 0)),
                "tid": r.get("TID", "")
            })
            goods_counter += 1

    # Save JSON database
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)
    print(f"[+] Exported JSON to {OUTPUT_JSON}")

    # Generate Markdown Reference
    md = [
        "# Hay Day - Complete Global Game IDs & In-Game Objects Reference",
        "",
        "This official reference contains the reverse-engineered in-game Global IDs and data attributes",
        "for Hay Day (`com.supercell.hayday`). Used directly by the `inxernal` native engine and loader.",
        "",
        "> **Global ID Architecture**:",
        "> - Type 4 Objects (Plots / Fields): `400000 + Index` (e.g. Wheat = `400001`, Corn = `400002`).",
        "> - Standard Supercell Entity IDs: `ClassID * 1000000 + InstanceID`.",
        "",
        "---",
        ""
    ]

    # Section 1: Plots & Crops
    md.append("## 1. Plots & Crops (`fields.csv` - Class 4)")
    md.append("These IDs are passed directly to `nplant <cropId>` and field automation.\n")
    md.append("| Global ID | Crop Name | Unlock Level | Grow Time | Harvest Yield | Max Coin Price | XP |")
    md.append("|:---|:---|:---:|:---:|:---:|:---:|:---:|")
    for item in db["crops_and_fields"]:
        mins = item['grow_time_seconds'] // 60
        secs = item['grow_time_seconds'] % 60
        t_str = f"{mins}m {secs}s" if mins else f"{secs}s"
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['level']} | {t_str} | {item['harvest_yield']} | {item['max_price']} | {item['xp']} |")

    # Section 2: Storage & Marketplace
    md.append("\n## 2. Storage & Marketplace Infrastructure")
    md.append("| Global ID | Name | Category | Description |")
    md.append("|:---|:---|:---|:---|")
    for item in db["storage_and_infrastructure"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | Storage / Market | {item['description']} |")

    # Section 3: Production & Processing Buildings
    md.append(f"\n## 3. Production Buildings (`processing_buildings.csv` - Class 6) [{len(db['production_buildings'])} Buildings]")
    md.append("| Global ID | Building Name | Level | Build Coins | Build Time | Grid Size | Slots |")
    md.append("|:---|:---|:---:|:---:|:---:|:---:|:---:|")
    for item in db["production_buildings"]:
        b_min = item['build_time_seconds'] // 60
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['level']} | {item['build_cost_coins']:,} | {b_min}m | {item['width']}x{item['height']} | {item['slots']} |")

    # Section 4: Expansion & Upgrade Materials
    md.append(f"\n## 4. Expansion & Upgrade Materials (`collection_tools.csv`) [{len(db['expansion_and_upgrade_materials'])} Items]")
    md.append("Essential upgrade parts for Silo, Barn, Land Expansion, and Town service buildings.\n")
    md.append("| Global ID | Item Name | Category |")
    md.append("|:---|:---|:---|")
    for item in db["expansion_and_upgrade_materials"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['category']} |")

    # Section 5: Clearing & Mining Tools
    md.append(f"\n## 5. Clearing & Mining Tools (`tools.csv` - Class 14)")
    md.append("| Global ID | Tool Name | Unlock Level | Max Price | Diamond Price |")
    md.append("|:---|:---|:---:|:---:|:---:|")
    for item in db["clearing_and_mining_tools"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['level']} | {item['max_price']} | {item['diamond_cost']} |")

    # Section 6: Farm Animals & Products
    md.append(f"\n## 6. Farm Animals & Products (`animals.csv` & `animal_goods.csv`)")
    md.append("### Farm Animals")
    md.append("| Global ID | Animal Name | Habitat | Level | Buy Price |")
    md.append("|:---|:---|:---|:---:|:---:|")
    for item in db["farm_animals"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['habitat']} | {item['level']} | {item['price']} |")

    md.append("\n### Animal Products")
    md.append("| Global ID | Product Name | Unlock Level | Produce Time | Max Coin Price | XP |")
    md.append("|:---|:---|:---:|:---:|:---:|:---:|")
    for item in db["animal_products"]:
        p_min = item['produce_time_seconds'] // 60
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['level']} | {p_min}m | {item['max_price']} | {item['xp']} |")

    # Section 7: Fruit Trees & Bushes
    md.append(f"\n## 7. Fruit Trees & Bushes (`fruit_trees.csv` - Class 10)")
    md.append("| Global ID | Tree / Bush Name | Unlock Level | Buy Price | Harvests | Grow Time |")
    md.append("|:---|:---|:---:|:---:|:---:|:---:|")
    for item in db["fruit_trees_and_bushes"]:
        g_min = item['grow_time_seconds'] // 60
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['level']} | {item['price']} | {item['harvests_before_dry']} | {g_min}m |")

    # Section 8: Boats & Fishing
    md.append(f"\n## 8. Boats & Fishing Lake (`boats.csv`, `fishing_boat.csv`, `fishing_areas.csv`, `nets.csv`)")
    md.append("| Global ID | Name | Category | Unlock Level |")
    md.append("|:---|:---|:---|:---:|")
    for item in db["boats_and_fishing"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['category']} | {item['level']} |")

    # Section 9: Delivery Truck & Orders
    md.append(f"\n## 9. Delivery Truck & Orders (`orders.csv`)")
    md.append("| Global ID | Destination / Customer | Description |")
    md.append("|:---|:---|:---|")
    for item in db["trucks_and_orders"]:
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['description']} |")

    # Section 10: Town & Trains
    md.append(f"\n## 10. Town & Trains (`service_buildings.csv`, `train.csv`)")
    md.append("| Global ID | Name | Category | Level | Cost |")
    md.append("|:---|:---|:---|:---:|:---:|")
    for item in db["town_and_trains"]:
        cost_str = f"{item.get('cost_coins', 0):,}" if item.get('cost_coins') else "-"
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['category']} | {item.get('level', '-')} | {cost_str} |")

    # Section 11: Produced Goods & Food Products
    md.append(f"\n## 11. Produced Goods & Food Recipes (Class 12) [{len(db['crafted_goods_and_products'])} Items]")
    md.append("All manufactured items across all production buildings (Bakery, Dairy, Grill, Pie Oven, Jam Maker, Smelter, etc.).\n")
    md.append("| Global ID | Item Name | Machine / Facility | Unlock Level | Time | Max Price | XP |")
    md.append("|:---|:---|:---|:---:|:---:|:---:|:---:|")
    for item in db["crafted_goods_and_products"]:
        c_min = item['produce_time_seconds'] // 60
        c_sec = item['produce_time_seconds'] % 60
        c_str = f"{c_min}m {c_sec}s" if c_min else f"{c_sec}s"
        md.append(f"| `{item['global_id']}` | **{item['name']}** | {item['building']} | {item['level']} | {c_str} | {item['max_price']} | {item['xp']} |")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(md))
    print(f"[+] Exported Markdown documentation to {OUTPUT_MD}")

if __name__ == "__main__":
    main()
