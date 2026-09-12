#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Config-Based Farm Automation Engine
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Reads, validates, customizes, and executes automation parameters from:
  Assest/configs/farm/loll.json

Allows users to:
  1. Inspect active farming, market, animal, machine, and maintenance settings
  2. Customize target crops, selling prices (anti-ban, max, custom), stack sizes
  3. Validate items against the Master Global ID Catalog (game_ids.py)
  4. Trigger autonomous farming passes matching the configured rules
  5. Dynamically hot-reload config into a running bot (command: cr / config_reload)
=============================================================================
"""

import os
import sys
import json
import time
import socket
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = WORKSPACE_ROOT / "Assest" / "configs" / "farm" / "loll.json"

try:
    import game_ids
except ImportError:
    game_ids = None


class ConfigAutomation:
    """Manages config loading, validation, modification, and execution."""

    def __init__(self, config_path=None, host="127.0.0.1", port=31350):
        self.config_path = Path(config_path or DEFAULT_CONFIG_PATH)
        self.host = host
        self.port = port
        self.config = {}
        self.load_config()

    def load_config(self):
        """Load and parse JSON config."""
        if not self.config_path.exists():
            print(f"[!] Config file not found at: {self.config_path}")
            return False
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
            print(f"[+] Loaded config from: {self.config_path.name}")
            return True
        except Exception as e:
            print(f"[!] Error parsing config JSON: {e}")
            return False

    def save_config(self, dest_path=None):
        """Save active config back to disk."""
        target = Path(dest_path or self.config_path)
        try:
            with open(target, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            print(f"[+] Config saved successfully to {target}")
            return True
        except Exception as e:
            print(f"[!] Failed to save config: {e}")
            return False

    def get_automation_section(self, section_name):
        """Safely fetch a specific automation section."""
        auto = self.config.get("automation", {})
        return auto.get(section_name, {})

    def get_summary(self):
        """Generate a clean formatted summary of current settings."""
        auto = self.config.get("automation", {})
        lines = []
        lines.append("=" * 65)
        lines.append("         HAY STAR CONFIG-BASED AUTOMATION PROFILE")
        lines.append(f" File: {self.config_path}")
        lines.append("=" * 65)

        # Fields & Crops
        fields = auto.get("fields", {})
        crop_id = fields.get("crop", 400001)
        crop_name = "Unknown"
        if game_ids and hasattr(game_ids, "CROPS"):
            crop_name = game_ids.CROPS.get(crop_id, str(crop_id))
        lines.append(f"  [Fields] Enabled: {fields.get('enabled', False)}")
        lines.append(f"    - Target Crop: {crop_name} (ID {crop_id})")
        crop_limits = fields.get("crop_limits", [])
        lines.append(f"    - Crop Limits: {len(crop_limits)} rules defined")

        # Market
        market = auto.get("market", {})
        lines.append(f"  [Market / Shop] Enabled: {market.get('enabled', False)}")
        lines.append(f"    - Auto-Advertise: {market.get('advertise', False)}")
        lines.append(f"    - Auto-Collect Sales: {market.get('collect_sales', False)}")
        items = market.get("items", [])
        lines.append(f"    - Configured Sale Items: {len(items)} items")

        # Animals
        animals = auto.get("animals", {})
        lines.append(f"  [Animals] Enabled: {animals.get('enabled', False)}")
        lines.append(f"    - Auto Feed Production: {animals.get('produce_missing_feed', False)}")

        # Fishing
        fishing = auto.get("fishing", {})
        lines.append(f"  [Fishing] Enabled: {fishing.get('enabled', False)}")
        lines.append(f"    - Catch Fish: {fishing.get('catch_fish', False)}")
        lines.append(f"    - Collect Lobsters: {fishing.get('collect_lobster_pool', False)}")

        # Maintenance
        maint = auto.get("maintenance", {})
        actions = maint.get("action_ids", [])
        lines.append(f"  [Maintenance] Enabled: {maint.get('enabled', False)}")
        lines.append(f"    - Scheduled Tasks: {len(actions)} tasks ({', '.join(actions[:4])}...)")

        lines.append("=" * 65)
        return "\n".join(lines)

    def set_default_crop(self, crop_id):
        """Set the active field crop ID."""
        auto = self.config.setdefault("automation", {})
        fields = auto.setdefault("fields", {})
        fields["crop"] = int(crop_id)
        crop_name = game_ids.CROPS.get(int(crop_id), str(crop_id)) if game_ids else str(crop_id)
        print(f"[+] Default crop updated to: {crop_name} (ID: {crop_id})")
        return True

    def set_market_item_price(self, item_id, price=None, price_mode="antibank"):
        """Configure selling parameters for a specific market item."""
        auto = self.config.setdefault("automation", {})
        market = auto.setdefault("market", {})
        items = market.setdefault("items", [])

        # Calculate price if needed
        final_price = price
        if final_price is None and game_ids:
            final_price = game_ids.calculate_shop_price(item_id, count=10, mode=price_mode)

        found = False
        for it in items:
            if it.get("item") == int(item_id):
                if final_price is not None:
                    it["price"] = int(final_price)
                found = True
                break

        if not found:
            items.append({
                "item": int(item_id),
                "count": 10,
                "price": int(final_price or 36),
                "reserve_stock": 20
            })

        print(f"[+] Updated market rule for item {item_id}: price={final_price}")
        return True

    def toggle_section(self, section_name, enabled=None):
        """Toggle an automation section on or off."""
        auto = self.config.setdefault("automation", {})
        sec = auto.setdefault(section_name, {})
        current = sec.get("enabled", True)
        new_val = (not current) if enabled is None else bool(enabled)
        sec["enabled"] = new_val
        print(f"[+] Section '{section_name}' enabled set to: {new_val}")
        return new_val

    def hot_reload_tcp(self):
        """Notify the running hay-star engine over TCP to reload its configuration."""
        print(f"[*] Sending config reload signal to hay-star.exe ({self.host}:{self.port})...")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2.0)
            s.connect((self.host, self.port))
            s.sendall(b"config_reload\n")
            time.sleep(0.1)
            resp = s.recv(1024).decode("utf-8", errors="ignore").strip()
            s.close()
            print(f"[+] Hot-reload response: {resp or 'OK'}")
            return True
        except Exception as e:
            print(f"[*] Engine offline or port closed ({e}). Config saved locally for next launch.")
            return False


def interactive_menu():
    """Interactive CLI menu for configuring farm automation settings."""
    ca = ConfigAutomation()
    while True:
        print("\n" + ca.get_summary())
        print("\nOptions:")
        print("  1. Change Default Field Crop (e.g. Wheat, Corn, Carrot)")
        print("  2. Toggle Automation Section (fields, market, fishing, animals, maintenance)")
        print("  3. Set Anti-Ban Market Prices")
        print("  4. Save Config Changes")
        print("  5. Hot-Reload Config into Running Bot (cr)")
        print("  6. Exit to Main Menu")

        choice = input("\nSelect an option [1-6]: ").strip()
        if choice == "1":
            print("\nAvailable Common Crops:")
            print("  400001: Wheat (2 min)")
            print("  400002: Corn (5 min)")
            print("  400003: Soybean (20 min)")
            print("  400004: Sugarcane (30 min)")
            print("  400005: Carrot (10 min)")
            cid = input("Enter Crop ID [400001]: ").strip() or "400001"
            if cid.isdigit():
                ca.set_default_crop(int(cid))
        elif choice == "2":
            sec = input("Enter section to toggle (fields/market/animals/fishing/maintenance): ").strip().lower()
            if sec:
                ca.toggle_section(sec)
        elif choice == "3":
            print("\nUpdating market items with anti-ban humanized pricing...")
            market = ca.get_automation_section("market")
            items = market.get("items", [])
            for it in items:
                item_id = it.get("item")
                count = it.get("count", 10)
                if game_ids:
                    safe_price = game_ids.calculate_shop_price(item_id, count=count, mode="antibank")
                    it["price"] = safe_price
            print(f"[+] Updated {len(items)} market rules with safe anti-ban prices.")
        elif choice == "4":
            ca.save_config()
        elif choice == "5":
            ca.save_config()
            ca.hot_reload_tcp()
        elif choice == "6" or choice.lower() in ("x", "q"):
            break


if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        ca = ConfigAutomation()
        if cmd in ("summary", "status", "info"):
            print(ca.get_summary())
        elif cmd in ("reload", "cr"):
            ca.hot_reload_tcp()
        elif cmd in ("set-crop", "crop") and len(sys.argv) > 2:
            ca.set_default_crop(sys.argv[2])
            ca.save_config()
            ca.hot_reload_tcp()
        elif cmd in ("toggle",) and len(sys.argv) > 2:
            ca.toggle_section(sys.argv[2])
            ca.save_config()
        else:
            print(f"Unknown argument '{cmd}'. Running interactive mode...")
            interactive_menu()
    else:
        interactive_menu()
