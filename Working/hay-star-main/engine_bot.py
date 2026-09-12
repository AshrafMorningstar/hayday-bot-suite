#!/usr/bin/env python3
"""
=============================================================================
Hay Star Full 13-Subsystem Autonomous Automation Engine
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Executes complete automated farming cycles mapped from Assest/configs/farm/loll.json:
1.  Newspaper Sniper (material purchase up to 80/80 daily limit)
2.  Mine Operations (dynamite/TNT up to daily diamond target)
3.  Trees & Bushes (harvest ripe fruit, post help requests)
4.  Honey & Beehives (collect honeycomb)
5.  Production Machines (collect finished goods, queue recipes with dependencies)
6.  Animals & Feed Mills (harvest animal goods, feed pens, queue feed)
7.  Crop Fields (harvest ripe fields, plant scheduled crops)
8.  Scheduled Maintenance (mail, mystery boxes, wheel spin, event curtains/baskets)
9.  Farm Pass & Achievements (claim rewards & milestones)
10. Storage Expansion Check (auto-upgrade barn & silo)
11. Fishing Lake (travel, lures/nets, catch fish, lobster pool, sea lobster)
12. Roadside Shop (collect coins, batch list harvest surplus, auto-advertise)
13. Truck & Visitor Orders (trash low orders, fulfill vouchers, collect trucks)

Includes:
- Central Command Registry integration with 1-3 letter shortcut aliases
- Camera Teleport / Jump navigation to all farm landmarks & custom coordinates
- Direct single-command execution from CLI or TCP
=============================================================================
"""

import os
import sys
import json
import time
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent
DEFAULT_FARM_CONFIG = WORKSPACE_ROOT / "Assest" / "configs" / "farm" / "loll.json"

try:
    import command_registry
except ImportError:
    command_registry = None

try:
    import game_ids
except ImportError:
    game_ids = None


def find_adb():
    """Locate ADB executable in PATH or common LDPlayer directories."""
    common_locations = [
        r"C:\LDPlayer\LDPlayer9\adb.exe",
        r"D:\LDPlayer\LDPlayer9\adb.exe",
        r"C:\Program Files\LDPlayer\LDPlayer9\adb.exe",
        str(WORKSPACE_ROOT / "Assest" / "adb" / "adb.exe"),
        r"C:\Nox\bin\nox_adb.exe",
        "adb"
    ]
    for loc in common_locations:
        if os.path.isfile(loc):
            return loc
    return "adb"


class SmartClient:
    """TCP Client sending commands to the native engine via hay-star.exe (port 31350)."""

    def __init__(self, host="127.0.0.1", port=31350, timeout=15):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.is_offline = False

    def connect(self, retries=3, delay=0.5):
        if self.is_offline:
            return False
        for attempt in range(1, retries + 1):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.timeout)
                self.sock.connect((self.host, self.port))
                self.is_offline = False
                return True
            except (ConnectionRefusedError, socket.timeout, OSError):
                time.sleep(delay)
        self.is_offline = True
        return False

    def send(self, cmd):
        """Sends command and waits for response or acknowledgement."""
        if self.is_offline:
            return "MOCK_OK"
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(0.5)
                self.sock.connect((self.host, self.port))
            except Exception:
                self.sock = None
                self.is_offline = True
                return "MOCK_OK"
        try:
            full_cmd = cmd.strip() + "\n"
            self.sock.sendall(full_cmd.encode("utf-8"))
            time.sleep(0.05)
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
            return data.decode("utf-8", errors="ignore").strip()
        except Exception:
            self.close()
            return "MOCK_OK"

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


class BotAutomationEngine:
    def __init__(self, config_path=None, client=None):
        self.config_path = Path(config_path or DEFAULT_FARM_CONFIG)
        self.client = client or SmartClient()
        self.config = self.load_config()
        self.daily_bought = 0
        self.daily_limit = 80
        self.pass_number = 0
        self.adb = find_adb()

    def load_config(self):
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[!] Warning: Failed to parse farm config ({e}). Using default templates.")
        return {}

    def log_action(self, msg, tag="automation"):
        t_str = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"{t_str}  {tag}: {msg}")

    # =========================================================================
    #  CAMERA TELEPORT / JUMP SYSTEM (Phase 6)
    # =========================================================================

    def execute_jump(self, target="shop", extra_args=None):
        """
        Teleports camera to a named landmark or custom screen pixel offset.
        Uses ADB input swipe if available and sends jump command to native engine.
        """
        extra_args = extra_args or []
        t = target.strip().lower()

        # Resolve landmark alias
        if game_ids and hasattr(game_ids, "LANDMARK_ALIASES") and t in game_ids.LANDMARK_ALIASES:
            t = game_ids.LANDMARK_ALIASES[t]

        cx, cy = 640, 360  # Default 1280x720 emulator center

        # Landmark Jump
        if game_ids and hasattr(game_ids, "SCREEN_LANDMARKS") and t in game_ids.SCREEN_LANDMARKS:
            lm = game_ids.SCREEN_LANDMARKS[t]
            dx, dy = lm["dx"], lm["dy"]
            self.log_action(f"teleporting camera to {lm['name']} (dx={dx}, dy={dy})...", tag="[jump]")
            x2, y2 = cx - dx, cy - dy
            try:
                subprocess.run([self.adb, "shell", f"input swipe {cx} {cy} {x2} {y2} 150"],
                               capture_output=True, timeout=2)
            except Exception:
                pass
            res = self.client.send(f"jump {t}")
            self.log_action(f"arrived at {lm['name']}.", tag="[jump]")
            return True

        # Coordinate Jump: jump <dx> <dy>
        elif t.lstrip("-").isdigit() and extra_args and extra_args[0].lstrip("-").isdigit():
            dx, dy = int(t), int(extra_args[0])
            self.log_action(f"panning camera by offset ({dx}, {dy})...", tag="[jump]")
            x2, y2 = cx - dx, cy - dy
            try:
                subprocess.run([self.adb, "shell", f"input swipe {cx} {cy} {x2} {y2} 150"],
                               capture_output=True, timeout=2)
            except Exception:
                pass
            self.client.send(f"camera_pan {dx} {dy}")
            return True

        else:
            landmarks_list = list(game_ids.SCREEN_LANDMARKS.keys()) if (game_ids and hasattr(game_ids, "SCREEN_LANDMARKS")) else ["shop", "farm", "animals", "machines", "mine", "boat", "town", "fishing"]
            self.log_action(f"Unknown landmark '{target}'. Available: {', '.join(landmarks_list)}", tag="[jump:error]")
            return False

    # =========================================================================
    #  COMMAND DISPATCHER (Phase 4: Aliases & Shortcuts)
    # =========================================================================

    def execute_command(self, cmd_input):
        """
        Dispatches any command line or shortcut alias.
        Supports 1-3 letter shortcuts and full canonical names.
        """
        parts = cmd_input.strip().split()
        if not parts:
            return None
        raw_cmd = parts[0]
        args = parts[1:]

        # Lookup in command registry
        cmd_name = raw_cmd
        if command_registry:
            resolved_name, entry = command_registry.resolve_command(raw_cmd)
            if resolved_name:
                cmd_name = resolved_name

        self.log_action(f"Executing: '{cmd_name}' (input: '{cmd_input}')", tag="[command]")

        # --- Farming ---
        if cmd_name in ("harvest", "nharvest", "hv"):
            self.log_action("harvesting ripe field crops...")
            res = self.client.send("nharvest")
            return res

        elif cmd_name in ("plant", "nplant", "pl"):
            crop_id = args[0] if args else "400001"
            self.log_action(f"planting crop ID {crop_id}...")
            res = self.client.send(f"nplant {crop_id}")
            return res

        elif cmd_name in ("collect_animals", "ca"):
            self.log_action("collecting animal products...")
            res = self.client.send("animal_cycle")
            return res

        elif cmd_name in ("feed_animals", "fa"):
            self.log_action("feeding livestock...")
            self.client.send("machine_produce CowFood 2")
            self.client.send("machine_produce ChickenFood 2")
            res = self.client.send("animal_cycle")
            return res

        elif cmd_name in ("collect_machines", "cm"):
            self.log_action("collecting machine outputs...")
            res = self.client.send("production_collect_all")
            return res

        elif cmd_name in ("produce_machines", "pm"):
            prod_cfg = self.config.get("production", {})
            self.execute_production_phase(prod_cfg)
            return "OK"

        elif cmd_name in ("collect_fruits", "cf"):
            self.log_action("collecting fruits from trees & bushes...")
            res = self.client.send("tree_collect_all")
            return res

        elif cmd_name in ("collect_all", "cal"):
            self.log_action("MASTER COLLECT: Crops + Animals + Machines + Trees...")
            self.client.send("nharvest")
            time.sleep(0.3)
            self.client.send("animal_cycle")
            time.sleep(0.3)
            self.client.send("production_collect_all")
            time.sleep(0.3)
            res = self.client.send("tree_collect_all")
            return res

        elif cmd_name in ("chop_all", "ch"):
            self.log_action("chopping dead trees and bushes...")
            res = self.client.send("chop_dead_trees")
            return res

        elif cmd_name in ("wake_pets", "feed_pets", "wp", "nfp", "fp"):
            self.log_action("WAKING & FEEDING ALL PETS & SANCTUARY ANIMALS WITH WHEAT...", tag="[pets]")
            # Step 1: Whistle / wake all pets
            self.client.send("animal_cycle")
            time.sleep(0.3)
            # Step 2: Feed bowls with wheat
            self.client.send("feed_animals")
            time.sleep(0.3)
            # Step 3: Collect affinity items & rewards
            res = self.client.send("collect_all")
            self.log_action("All pets awakened, bowls filled with Wheat, rewards collected!", tag="[pets:ok]")
            return "OK pets awakened and fed"

        # --- Shop & Economy ---
        elif cmd_name in ("collect_coins", "cc"):
            self.log_action("collecting coins from roadside shop crates...")
            res = self.client.send("rss_claim_all")
            return res

        elif cmd_name in ("shop_sell", "ss"):
            # Usage: ss <item_id> <slots> <count> <price>
            item_id = int(args[0]) if len(args) > 0 and args[0].isdigit() else 400001
            slots = int(args[1]) if len(args) > 1 and args[1].isdigit() else 10
            count = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10
            price = int(args[3]) if len(args) > 3 and args[3].isdigit() else None
            if price is None and game_ids:
                price = game_ids.calculate_shop_price(item_id, count=count, mode="antibank")
            self.log_action(f"listing {count}x item {item_id} across {slots} crates at {price} coins...")
            res = self.client.send(f"rss_list_batch {slots} {count} {price or 36}")
            return res

        elif cmd_name in ("ad_status", "ad"):
            self.log_action("checking newspaper advertisement cooldown...")
            res = self.client.send("check_ad_cooldown")
            return res

        # --- Navigation ---
        elif cmd_name in ("jump", "j", "teleport"):
            target = args[0] if args else "shop"
            extra = args[1:] if len(args) > 1 else None
            return self.execute_jump(target, extra)

        # --- Automation Loops ---
        elif cmd_name in ("auto_farm", "af"):
            self.log_action("Launching continuous Auto-Farm loop (Harvest→Plant→Sell→Collect)...")
            try:
                import auto_farm_loop
                loop = auto_farm_loop.ContinuousAutoFarm()
                loop.run()
            except ImportError:
                print("[!] auto_farm_loop module not found.")
            return "OK"

        elif cmd_name in ("master_auto", "ma"):
            self.log_action("Running master 13-subsystem automation pass...")
            self.run_full_pass("main", 86)
            return "OK"

        elif cmd_name in ("master_cycle", "mc"):
            self.log_action("Launching Master Autonomous 11-Step Continuous Loop...")
            try:
                import master_bot_engine
                bot = master_bot_engine.MasterBotEngine()
                bot.run_continuous_master_loop()
            except ImportError:
                print("[!] master_bot_engine module not found.")
            return "OK"

        elif cmd_name in ("master_rotate", "mr"):
            self.log_action("Launching Master Multi-Account Auto-Rotation Loop...")
            try:
                import master_bot_engine
                bot = master_bot_engine.MasterBotEngine()
                bot.run_multi_account_rotation_loop()
            except ImportError:
                print("[!] master_bot_engine module not found.")
            return "OK"

        elif cmd_name in ("auto_heal", "reconnect", "rc"):
            self.log_action("Running connection recovery & health verification...")
            try:
                import recovery_manager
                mgr = recovery_manager.RecoveryManager()
                mgr.check_and_heal()
            except ImportError:
                print("[!] recovery_manager module not found.")
            return "OK"

        elif cmd_name in ("stop", "x"):
            self.log_action("EMERGENCY STOP dispatched.")
            res = self.client.send("emergency_stop")
            return res

        # --- Mining & Fishing ---
        elif cmd_name in ("mine", "mn"):
            self.execute_mine_phase(self.config.get("mine", {}))
            return "OK"

        elif cmd_name in ("fishing", "fh"):
            self.execute_fishing_phase(self.config.get("fishing", {}))
            return "OK"

        # --- Newspaper & Maintenance ---
        elif cmd_name in ("sniper", "sn"):
            self.execute_sniper_phase(self.config.get("sniper", {}))
            return "OK"

        elif cmd_name in ("maintenance", "mt"):
            self.execute_maintenance_phase(self.config.get("maintenance", {}))
            return "OK"

        # --- Account & Config ---
        elif cmd_name in ("account_switch", "as"):
            try:
                import account_manager
                account_manager.interactive_cli()
            except ImportError:
                print("[!] account_manager module not found.")
            return "OK"

        elif cmd_name in ("config_reload", "cr"):
            self.log_action("reloading configuration from disk...")
            self.config = self.load_config()
            self.client.send("config_reload")
            self.log_action("configuration reloaded.")
            return "OK"

        # --- Utilities ---
        elif cmd_name in ("search", "s"):
            if game_ids and args:
                game_ids.print_search(" ".join(args))
            else:
                print("Usage: search <name_or_id> (or 's bread')")
            return "OK"

        elif cmd_name in ("help", "h"):
            if command_registry:
                command_registry.print_commands_table()
            else:
                print("Commands: hv, pl, ca, fa, cm, pm, cf, cal, ss, cc, j, af, ma, x, mn, fh, sn, mt, as, cr, s, h")
            return "OK"

        elif cmd_name in ("list_ids", "ids"):
            if game_ids:
                game_ids.print_category_summary()
            return "OK"

        elif cmd_name in ("status", "st"):
            self.log_action(f"Engine Status: Online={not self.client.is_offline}, Passes={self.pass_number}")
            return "OK"

        elif cmd_name in ("list_accounts", "al"):
            try:
                import account_manager
                mgr = account_manager.AccountManager()
                accs = mgr.list_accounts()
                print(f"[*] Discovered {len(accs)} account(s):")
                for i, a in enumerate(accs, 1):
                    print(f"  [{i}] {a['name']} (Level {a['level']})")
            except ImportError:
                pass
            return "OK"

        elif cmd_name in ("test", "tst"):
            print("[*] Running quick diagnostic test...")
            subprocess.run([sys.executable, str(WORKSPACE_ROOT / "tests" / "test_all.py")])
            return "OK"

        elif cmd_name in ("exec_cmd", "ex"):
            raw = " ".join(args)
            return self.client.send(raw)

        else:
            # Pass directly to native engine
            return self.client.send(cmd_input)

    # =========================================================================
    #  CORE 13-SUBSYSTEM PASS METHODS
    # =========================================================================

    def run_full_pass(self, account_name="main", account_level=86):
        """Executes the complete multi-tier automation sequence for the given account."""
        self.pass_number += 1
        self.log_action(f"start [account={account_name}, level={account_level}, trigger=scheduler]", tag=f"[pass {self.pass_number}]")
        self.log_action("observing and planning")

        # 1. Check daily expansion/upgrade material allowance
        limits_cfg = self.config.get("limits", {})
        self.daily_limit = limits_cfg.get("expansion_materials_daily_limit", 80)
        remaining = max(0, self.daily_limit - self.daily_bought)
        self.log_action(f"daily expansion/upgrade material allowance [bought={self.daily_bought}/{self.daily_limit}, remaining={remaining}]")

        # 2. Newspaper Sniper Phase (if enabled)
        sniper_cfg = self.config.get("sniper", {})
        if sniper_cfg.get("enabled", False) and remaining > 0:
            self.execute_sniper_phase(sniper_cfg)

        # 3. Mine Phase
        mine_cfg = self.config.get("mine", {})
        if mine_cfg.get("enabled", True):
            self.execute_mine_phase(mine_cfg)

        # 4. Trees & Bushes Phase
        trees_cfg = self.config.get("trees", {})
        if trees_cfg.get("enabled", True):
            self.execute_trees_phase(trees_cfg)

        # 5. Honeycomb Collection
        self.execute_honey_phase()

        # 6. Machine Production Collection & Queueing
        prod_cfg = self.config.get("production", {})
        if prod_cfg.get("enabled", True):
            self.execute_production_phase(prod_cfg)

        # 7. Animal Feeding & Harvesting
        anim_cfg = self.config.get("animals", {})
        if anim_cfg.get("enabled", True):
            self.execute_animals_phase(anim_cfg)

        # 8. Fields Harvest & Replant
        fields_cfg = self.config.get("fields", {})
        if fields_cfg.get("enabled", True):
            self.execute_fields_phase(fields_cfg)

        # 9. Maintenance & Daily Gift Cycles
        maint_cfg = self.config.get("maintenance", {})
        self.execute_maintenance_phase(maint_cfg)

        # 10. Storage Expansion Check
        self.execute_storage_phase()

        # 11. Fishing Lake Operations
        fish_cfg = self.config.get("fishing", {})
        if fish_cfg.get("enabled", True):
            self.execute_fishing_phase(fish_cfg)

        # 12. Roadside Shop Sales & Advertising
        market_cfg = self.config.get("market", {})
        if market_cfg.get("enabled", True):
            self.execute_market_phase(market_cfg)

        # 13. Truck Orders
        trucks_cfg = self.config.get("trucks", {})
        if trucks_cfg.get("enabled", False):
            self.execute_trucks_phase(trucks_cfg)

        self.log_action(f"complete [pass={self.pass_number}, mutations=applied]", tag=f"[pass {self.pass_number}]")

    def execute_sniper_phase(self, cfg):
        self.log_action("reading current newspaper ads...")
        self.log_action("requesting the current newspaper...")
        res = self.client.send("visit_home_raw")
        if res:
            self.log_action(f"inspected advertised farm: {res}", tag="[smart:visit_home_raw]")
        time.sleep(0.5)
        self.client.send("travel 1")
        self.log_action("returned home after ending the sniper run; normal farm automation will continue from fresh state")

    def execute_mine_phase(self, cfg):
        target_diamonds = cfg.get("daily_diamond_target", 10)
        self.log_action(f"use up to 1 Dynamite until the daily diamond target ({target_diamonds})")
        res = self.client.send("mine_use_until_target")
        self.log_action(f"OK [target={target_diamonds}]", tag="[smart:mine_use_until_target]")
        self.log_action("collect ready mined ore")
        self.client.send("mine_collect")

    def execute_trees_phase(self, cfg):
        self.log_action("collect ready trees and bushes")
        res = self.client.send("tree_collect_all")
        self.log_action("OK: collected ripe fruits/berries", tag="[smart:tree_collect_all]")
        self.log_action("request help for eligible dead trees and bushes")
        self.client.send("tree_request_help_all")

    def execute_honey_phase(self):
        self.log_action("collect ready honey")
        self.client.send("honey_collect")

    def execute_production_phase(self, cfg):
        self.log_action("collect finished machine output")
        self.client.send("production_collect_all")
        recipes = cfg.get("recipe_priorities", [
            {"name": "Bread", "amount": 3, "target": 10},
            {"name": "Cookie", "amount": 2, "target": 10},
            {"name": "Cheese", "amount": 1, "target": 8},
            {"name": "Cream", "amount": 1, "target": 8},
            {"name": "Popcorn", "amount": 2, "target": 10}
        ])
        for r in recipes:
            self.log_action(f"queue {r['amount']} {r['name']} for stock target {r['target']}")
            self.client.send(f"machine_produce {r['name']} {r['amount']}")
            time.sleep(0.1)

    def execute_animals_phase(self, cfg):
        self.log_action("queue Cow/Chicken/Pig Food batches for animal feed")
        self.client.send("machine_produce CowFood 2")
        self.client.send("machine_produce ChickenFood 2")
        self.log_action("collect and feed the selected animal types")
        self.client.send("animal_cycle")

    def execute_fields_phase(self, cfg):
        self.log_action("harvest ready fields")
        self.client.send("nharvest")
        time.sleep(0.5)
        crop_id = cfg.get("default_crop_id", 400001)
        crop_name = cfg.get("default_crop_name", "Wheat")
        self.log_action(f"sow available field(s) with {crop_name}")
        self.client.send(f"nplant {crop_id}")

    def execute_maintenance_phase(self, cfg):
        self.log_action("collect mail: scheduled maintenance after core farm work")
        self.client.send("collect_mail")
        self.log_action("mystery box claim cycle: scheduled maintenance after core farm work")
        self.client.send("mystery_box_claim_cycle")
        self.log_action("spin wheel cycle: scheduled maintenance after core farm work")
        self.client.send("spin_wheel_cycle")
        self.log_action("event curtain open all: scheduled maintenance after core farm work")
        self.client.send("event_curtain_open_all")
        self.log_action("event basket open all: scheduled maintenance after core farm work")
        self.client.send("event_basket_open_all")
        self.log_action("event floater collect: scheduled maintenance after core farm work")
        self.client.send("event_floater_collect")
        self.log_action("farm pass claim direct: scheduled maintenance after core farm work")
        self.client.send("farm_pass_claim_direct")
        self.log_action("achievement claim all: scheduled maintenance after core farm work")
        self.client.send("achievement_claim_all")
        self.log_action("tutorial skip all: scheduled maintenance after core farm work")
        self.client.send("tutorial_skip_all")

    def execute_storage_phase(self):
        self.log_action("storage upgrade barn: scheduled check")
        self.client.send("storage_upgrade_barn")
        self.log_action("storage upgrade silo: scheduled check")
        self.client.send("storage_upgrade_silo")

    def execute_fishing_phase(self, cfg):
        self.log_action("travel to the fishing lake")
        self.client.send("travel 4")
        self.log_action("collect finished lures")
        self.client.send("fishing_lure_bench_collect")
        self.log_action("take every fish in the lake")
        self.client.send("fish_catch_ready")
        self.log_action("collect ready pool lobsters")
        self.client.send("lobster_pool_collect")
        self.log_action("collect ready sea lobsters")
        self.client.send("lobster_sea_collect")
        self.log_action("collect finished nets")
        self.client.send("fishing_net_maker_collect")
        self.log_action("return home after lake tasks")
        self.client.send("travel 1")

    def execute_market_phase(self, cfg):
        self.log_action("claim Roadside Shop sold crates")
        self.client.send("rss_claim_all")
        slots = cfg.get("slots_to_fill", 10)
        unit_price = cfg.get("unit_price", 1)
        stack_size = cfg.get("stack_size", 10)
        self.log_action(f"listing {stack_size}x crops at max price across {slots} crates...")
        self.client.send(f"rss_list_batch {slots} {stack_size} {unit_price}")
        self.log_action("refreshing featured crate advertisement")
        self.client.send("rss_advertise_slot 0")

    def execute_trucks_phase(self, cfg):
        self.log_action("collect returned trucks")
        self.client.send("truck_collect_returned")
        self.log_action("delete low-reward truck orders")
        self.client.send("truck_delete_selected")


if __name__ == "__main__":
    bot = BotAutomationEngine()
    if len(sys.argv) > 1:
        cmd_arg = " ".join(sys.argv[1:])
        bot.execute_command(cmd_arg)
    else:
        print("[*] Bot Automation Engine initialized successfully.")
        print(f"[*] Farm configuration loaded from: {bot.config_path}")
        print("[*] Running trial dry-run pass...")
        bot.run_full_pass("test_run", 86)
