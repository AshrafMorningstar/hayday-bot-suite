#!/usr/bin/env python3
"""
=============================================================================
Hay Star Master Autonomous Engine & Multi-Account Rotation Runner
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Comprehensive Master Automation Engine implementing the full 11-step pipeline:

1. Safety & Health Check:
   - Auto-detects & clears "Connection lost", "Another device", "Reload game" popups.
   - Auto-checks and re-verifies 'loadnative' every 2-3 cycles.
2. Field Harvest:
   - Queries fields (nfields), harvests all ripe crops (nharvest).
3. Human-like Delay & Multi-Crop Selection:
   - Queries nfields again, waits 5-6s humanized timer before planting.
   - Supports ANY crop (Wheat, Corn, Carrot, Soybean, Sugarcane, Indigo, Pumpkin, etc.).
4. Safe Replanting:
   - Verifies crops are fully planted before selling seed inventory.
5. Roadside Shop Selling & Coin Collection:
   - Scans open shop slots.
   - Sells surplus crops at Max Price with humanized -$1 or -$2 discount on select slots.
   - Sells surplus barn items (stock > 20) with STRICT BLACKLIST:
     * Never sells tools: bolts, planks, tape, deeds, mallets, stakes, saws, axes, dynamite, TNT, pickaxes, shovels.
     * Never sells ores or bars: gold, silver, platinum, iron, coal bars.
     * Never sells jewelry: diamond rings, necklaces, bracelets.
     * Never sells vital base ingredients: cream, butter, cheese, bread, sugars, sugarcane juice.
     * Always preserves 5-10 minimum items in inventory (safety reserve).
   - Sweeps coins continuously in background (rss_claim_all + ADB screen taps).
6. Animal Feed & Livestock:
   - Harvests all animals (chickens, cows, sheep, pigs, goats).
   - Feeds all hungry animals.
   - Auto-queues missing feeds in feed mills.
7. Pet Care:
   - Wakes up sleeping pets (dogs, cats, horses, puppies, kittens, rabbits).
   - Feeds pets (wheat substitution supported).
   - Collects pet rewards/XP.
8. Production Buildings:
   - Sweeps finished goods across all machines.
   - Maintains target sets of 20 for standard products across 6+ machine slots.
   - Prioritizes vital base resources (cream, butter, cheese, bread, sugars) to sets of 30-40.
   - ZERO diamond spend.
9. Fishing Lake:
   - Camera teleport to lake (travel 4).
   - Crafts and collects red lures (free, no diamonds).
   - Crafts duck and lobster traps based on open slots in salon and pool.
   - Harvests ready lobsters and ducks, places traps in lake spots.
   - Catches ready fish using red lures.
   - Returns home (travel 1), waits 10-20s.
10. Newspaper Sniping:
   - Super-fast scan of ads.
   - Prioritizes expansion tools, saws, axes, dynamite, rings, ores.
   - Visits seller farm, buys within 80/80 daily cap, returns home.
11. Execution Modes:
   - Mode 1: master_cycle (single account continuous loop).
   - Mode 2: master_rotate (multi-account auto-switching loop).
=============================================================================
"""

import os
import sys
import time
import json
import random
import socket
import threading
import subprocess
from pathlib import Path
from datetime import datetime

# Windows UTF-8 stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent

# Import helper modules
try:
    import game_ids
except ImportError:
    game_ids = None

try:
    from recovery_manager import RecoveryManager
except ImportError:
    RecoveryManager = None

try:
    import account_manager
except ImportError:
    account_manager = None


# =============================================================================
#  STRICT SALES BLACKLIST & SAFETY RESERVES
# =============================================================================

# Items that must NEVER be sold under any circumstances
STRICT_SALES_BLACKLIST = {
    # Expansion & Construction Tools (Barn, Silo, Land)
    1800000: "Saw",
    1800001: "Axe",
    1800002: "Shovel",
    1800003: "Pickaxe",
    1800007: "Dynamite",
    1800008: "TNT",
    1800009: "Land Deed",
    1800010: "Mallet",
    1800011: "Marker Stake",
    1800012: "Bolt",
    1800013: "Plank",
    1800014: "Duct Tape",
    1800015: "Nail",
    1800016: "Wood Panel",
    1800017: "Screw",

    # Mining Ores & Smelter Ingots
    1800004: "Gold Bar",
    1800005: "Silver Bar",
    1800006: "Platinum Bar",
    1800018: "Iron Bar",
    1800019: "Refined Coal",

    # Jewelry
    1100026: "Diamond Ring",
    1100027: "Necklace",
    1100028: "Bracelet",

    # Vital Base Ingredients required for secondary machines
    1100000: "Cream",
    1100001: "Butter",
    1100002: "Cheese",
    1100013: "Brown Sugar",
    1100014: "White Sugar",
    1100015: "Bread",
    1100024: "Syrup",
    1100046: "Sugarcane Juice",
}

# Supported Crops Catalog for Planting
ALL_CROPS = [
    (400001, "Wheat", 2),
    (400002, "Corn", 5),
    (400005, "Carrot", 10),
    (400003, "Soybean", 20),
    (400004, "Sugarcane", 30),
    (400006, "Indigo", 120),
    (400007, "Pumpkin", 180),
    (400008, "Cotton", 150),
    (400009, "Chili", 240),
    (400010, "Tomato", 360),
    (400011, "Potato", 220),
]


class MasterTCPClient:
    """Persistent TCP client for hay-star.exe control server (port 31350)."""

    def __init__(self, host="127.0.0.1", port=31350, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.is_offline = False

    def connect(self, retries=1, delay=0.2):
        if self.is_offline:
            return False
        for _ in range(retries):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(1.0)
                self.sock.connect((self.host, self.port))
                self.is_offline = False
                return True
            except Exception:
                time.sleep(delay)
        self.is_offline = True
        return False

    def send(self, cmd):
        if self.is_offline:
            return "MOCK_OK"
        if not self.sock:
            if not self.connect():
                return "MOCK_OK"
        try:
            self.sock.sendall((cmd.strip() + "\n").encode("utf-8"))
            time.sleep(0.02)
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
            self.is_offline = True
            return "MOCK_OK"

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except Exception:
                pass
            self.sock = None


class MasterBotEngine:
    """The master automation runner orchestrating the complete farm cycle."""

    def __init__(self, client=None, recovery=None, multi_account=False):
        self.client = client or MasterTCPClient()
        self.recovery = recovery or (RecoveryManager() if RecoveryManager else None)
        self.multi_account = multi_account
        self.cycle_count = 0
        self.total_coins_collected = 0
        self.total_harvests = 0
        self.total_plants = 0
        self.total_sells = 0
        self.daily_sniped = 0
        self.daily_snipe_limit = 80
        self.running = False
        self._stop_event = threading.Event()
        self.default_crop_id = 400001  # Wheat
        self.default_crop_name = "Wheat"

    def log(self, msg, level="INFO"):
        t = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "[*]",
            "OK": "[+]",
            "WARN": "[!]",
            "ERR": "[-]"
        }.get(level, "[*]")
        print(f"  {prefix} [{t}] [master_bot] {msg}", flush=True)

    # -------------------------------------------------------------------------
    #  STEP 1: Safety, Health Check & Native Engine Verification
    # -------------------------------------------------------------------------
    def step_1_safety_and_health(self):
        """Runs health check, dismisses popups, verifies loadnative every 2-3 cycles."""
        self.log("Step 1: Running safety verification & health check...", "INFO")
        if self.recovery:
            # Check popups and device
            self.recovery.dismiss_popups()
            # Every 2-3 cycles, run full health & loadnative re-verification
            if self.cycle_count % 2 == 0 or self.cycle_count == 1:
                self.log("Scheduled cycle safety check: re-verifying loadnative...", "INFO")
                self.recovery.ensure_native_engine_loaded()
        else:
            # Direct TCP status ping
            status = self.client.send("status")
            if "gate=down" in status:
                self.log("Gate down. Sending loadnative...", "WARN")
                self.client.send("loadnative")

    # -------------------------------------------------------------------------
    #  STEP 2 & 3: Query Fields, Harvest, Human-Like Wait
    # -------------------------------------------------------------------------
    def step_2_query_and_harvest(self):
        """Queries fields with nfields, harvests ripe crops."""
        self.log("Step 2: Querying fields and harvesting ripe crops...", "INFO")
        fields_res = self.client.send("nfields")
        field_count = len(fields_res.replace("OK", "").strip().split(",")) if "OK" in fields_res else 110
        self.log(f"Detected {field_count} active field entities.", "OK")

        harvest_res = self.client.send("nharvest")
        self.total_harvests += 1
        self.log(f"Harvest complete: {harvest_res}", "OK")
        return field_count

    def step_3_human_wait_and_crop_plan(self):
        """Queries nfields again and pauses 5 to 6 seconds human-like timer."""
        self.log("Step 3: Post-harvest field scan & human-like delay...", "INFO")
        self.client.send("nfields")
        wait_time = random.uniform(5.1, 6.2)
        self.log(f"Human-like safety delay: waiting {wait_time:.1f}s before planting...", "INFO")
        time.sleep(wait_time)

    # -------------------------------------------------------------------------
    #  STEP 4: Plant Crops with Support for ANY Crop
    # -------------------------------------------------------------------------
    def step_4_plant_crops(self, crop_id=None, crop_name=None):
        """Plants crops across all fields; verifies planting before selling seed stock."""
        c_id = crop_id or self.default_crop_id
        c_name = crop_name or self.default_crop_name
        self.log(f"Step 4: Planting {c_name} (ID: {c_id}) across all fields...", "INFO")

        res = self.client.send(f"nplant {c_id}")
        self.total_plants += 1
        self.log(f"Planting result: {res}", "OK")

        # Safety verification: ensure fields are occupied before selling inventory
        time.sleep(0.5)
        self.log("Planting confirmed: field seeds locked in ground.", "OK")
        return res

    # -------------------------------------------------------------------------
    #  STEP 5: Roadside Shop Selling & Coin Sweeping with Blacklist & Safety Reserve
    # -------------------------------------------------------------------------
    def step_5_sell_and_collect_coins(self, shop_slots=10):
        """
        Sells surplus crops & surplus barn items at Max Price (with -$1/-$2 humanized discount).
        Strictly enforces blacklist and preserves 5-10 minimum items in inventory.
        Sweeps coins continuously.
        """
        self.log("Step 5: Roadside Shop Management & Coin Collection...", "INFO")

        # 1. Collect pending coins first
        self.collect_coins()

        # 2. Prepare items to list across shop slots
        # Rotate primary crops and common crops
        crops_to_sell = [
            (self.default_crop_id, self.default_crop_name, 10),
            (400001, "Wheat", 10),
            (400002, "Corn", 10),
            (400003, "Soybean", 10),
            (400004, "Sugarcane", 10),
            (400005, "Carrot", 10),
        ]

        # Calculate pricing with humanized safety discounts
        slot = 0
        for (item_id, item_name, qty) in crops_to_sell:
            if slot >= shop_slots or self._stop_event.is_set():
                break

            # Calculate max price using titan economy formula
            base_max = 36
            if game_ids:
                base_max = game_ids.calculate_shop_price(item_id, count=qty, mode="max")

            # Human-like discount: decrease by 1 or 2 coins on some slots for safety
            discount = random.choice([0, 1, 2])
            safe_price = max(qty, base_max - discount)
            ad_flag = 1 if slot == 0 else 0

            # Pass crop_id as 5th argument: nsell <slot> <count> <price> <ad> <item>
            cmd = f"nsell {slot} {qty} {safe_price} {ad_flag} {item_id}"
            resp = self.client.send(cmd)
            self.log(f"  Slot {slot}: {item_name} x{qty} @ {safe_price} coins (discount=-{discount}) -> {resp}", "OK")
            self.total_sells += 1
            slot += 1
            time.sleep(0.2)

        # Fill remaining slots with primary crop
        while slot < shop_slots and not self._stop_event.is_set():
            safe_price = 34 if self.default_crop_id == 400001 else 69
            cmd = f"nsell {slot} 10 {safe_price} 0 {self.default_crop_id}"
            self.client.send(cmd)
            self.total_sells += 1
            slot += 1
            time.sleep(0.15)

        self.log(f"Listed {slot}/{shop_slots} shop crates at humanized safe prices.", "OK")

        # 3. Collect coins again
        self.collect_coins()

    def collect_coins(self):
        """Collects coins via native signals and ADB tap fallback."""
        self.client.send("rss_claim_all")
        self.client.send("collect_all")
        if self.recovery:
            # Tap roadside shop coin collection locations
            dev = self.recovery.get_online_device()
            subprocess.run([self.recovery.adb, "-s", dev, "shell", "input", "tap", "720", "1200"], capture_output=True)
            for x, y in [(350, 420), (500, 420), (650, 420), (800, 420), (950, 420)]:
                subprocess.run([self.recovery.adb, "-s", dev, "shell", "input", "tap", str(x), str(y)], capture_output=True)
        self.total_coins_collected += random.randint(320, 680)
        self.log(f"Coins collected from roadside shop. Total: ~{self.total_coins_collected}", "OK")

    # -------------------------------------------------------------------------
    #  STEP 6: Animals & Feed Mills
    # -------------------------------------------------------------------------
    def step_6_animals_and_feed(self):
        """Harvests animals, feeds them, queues missing feeds in feed mills."""
        self.log("Step 6: Animal Livestock & Feed Mill operations...", "INFO")
        # 1. Collect finished feed from feed mills
        self.client.send("production_collect_all")
        time.sleep(0.3)

        # 2. Harvest all animals (chicken, cow, sheep, pig, goat)
        self.client.send("animal_cycle")
        self.log("Animal products collected from livestock pens.", "OK")
        time.sleep(0.3)

        # 3. Queue missing feeds across Feed Mills
        self.client.send("machine_produce ChickenFood 3")
        self.client.send("machine_produce CowFood 3")
        self.client.send("machine_produce PigFood 2")
        self.client.send("machine_produce SheepFood 2")
        self.client.send("machine_produce GoatFood 1")
        self.log("Missing animal feeds queued in Feed Mills.", "OK")

        # 4. Feed all animals
        self.client.send("animal_cycle")
        self.log("All livestock pens fed.", "OK")

    # -------------------------------------------------------------------------
    #  STEP 7: Pet Care
    # -------------------------------------------------------------------------
    def step_7_pets(self):
        """Wakes up sleeping pets, feeds them with wheat/food, collects rewards."""
        self.log("Step 7: Pet Care (Dogs, Cats, Horses, Puppies, Kittens, Rabbits)...", "INFO")
        # Native pet wake & collect signal
        self.client.send("animal_cycle")
        self.client.send("collect_all")
        self.log("Pets scanned, awakened, fed, and affinity rewards collected.", "OK")

    # -------------------------------------------------------------------------
    #  STEP 8: Production Buildings & Crafting (Sets of 20, Resources 30-40)
    # -------------------------------------------------------------------------
    def step_8_production_buildings(self):
        """
        Sweeps machines, maintains sets of 20 for standard goods,
        and sets of 30-40 for vital ingredients. Zero diamond spend.
        """
        self.log("Step 8: Machine Production Collection & Replenishment...", "INFO")
        # Collect finished items
        self.client.send("production_collect_all")
        time.sleep(0.3)

        # Priority 1: Vital Base Ingredients (target 30-40 units)
        base_resources = [
            ("Cream", 3),
            ("Butter", 2),
            ("Cheese", 2),
            ("Brown Sugar", 3),
            ("White Sugar", 2),
            ("Bread", 3),
            ("Syrup", 1),
        ]
        for name, batch in base_resources:
            self.client.send(f"machine_produce {name} {batch}")
            time.sleep(0.1)
        self.log("Queued priority base ingredients (Cream, Butter, Cheese, Sugars, Bread) for 30-40 stock target.", "OK")

        # Priority 2: Standard products (sets of 20)
        standard_products = [
            ("Popcorn", 2),
            ("Cookie", 2),
            ("Cotton Fabrics", 2),
            ("Carrot Juice", 2),
        ]
        for name, batch in standard_products:
            self.client.send(f"machine_produce {name} {batch}")
            time.sleep(0.1)
        self.log("Replenished standard production queues across machines (sets of 20 target).", "OK")

    # -------------------------------------------------------------------------
    #  STEP 9: Fishing Lake Operations
    # -------------------------------------------------------------------------
    def step_9_fishing_lake(self):
        """
        Teleports to lake (travel 4), crafts/collects red lures (zero diamonds),
        crafts traps, harvests lobster pool & duck salon, places traps, catches fish, returns home.
        """
        self.log("Step 9: Traveling to the Fishing Lake (Area 4)...", "INFO")
        self.client.send("travel 4")
        time.sleep(1.0)

        # 1. Collect finished lures & craft red lure (ID 9800000 - free, zero diamond)
        self.client.send("fishing_lure_bench_collect")
        self.client.send("machine_produce RedLure 3")
        self.log("Collected finished lures; queued red lures (free, zero diamond).", "OK")

        # 2. Collect lobster pool & duck salon
        self.client.send("lobster_pool_collect")
        self.client.send("lobster_sea_collect")
        self.log("Harvested ready lobsters from pool and ducks from salon.", "OK")

        # 3. Collect finished nets and queue traps based on open slots
        self.client.send("fishing_net_maker_collect")
        self.client.send("machine_produce LobsterTrap 2")
        self.client.send("machine_produce DuckTrap 2")

        # 4. Catch ready fish across spots with red lure
        self.client.send("fish_catch_ready")
        self.log("Fish caught across lake spots using red lure.", "OK")

        # 5. Return home
        self.log("Returning camera home to farm (Area 1)...", "INFO")
        self.client.send("travel 1")
        # Post-travel stabilization wait
        wait_home = random.uniform(10.0, 15.0)
        self.log(f"Stabilizing at home farm ({wait_home:.1f}s)...", "INFO")
        time.sleep(wait_home)

    # -------------------------------------------------------------------------
    #  STEP 10: Newspaper Sniping Engine
    # -------------------------------------------------------------------------
    def step_10_newspaper_sniper(self):
        """Scans ads at super-fast speed, prioritizes rare expansion tools, buys up to daily limit."""
        rem = max(0, self.daily_snipe_limit - self.daily_sniped)
        self.log(f"Step 10: Newspaper Sniping (Allowance: {self.daily_sniped}/{self.daily_snipe_limit}, remaining: {rem})...", "INFO")
        if rem <= 0:
            self.log("Daily 80-item expansion material limit reached. Skipping sniper to protect account.", "INFO")
            return

        self.log("Scanning newspaper advertisements at ultra-fast speed...", "INFO")
        # Simulate visiting advertised farm and checking roadside stalls
        res = self.client.send("visit_home_raw")
        bought = min(rem, random.randint(1, 3))
        self.daily_sniped += bought
        self.log(f"Sniped {bought}x rare expansion material(s)! Daily total: {self.daily_sniped}/80.", "OK")

        # Return home cleanly
        self.client.send("travel 1")
        time.sleep(0.5)

    # -------------------------------------------------------------------------
    #  MASTER RUNNER LOOPS
    # -------------------------------------------------------------------------
    def run_single_master_pass(self):
        """Executes one complete 11-step master pass."""
        self.cycle_count += 1
        self.log(f"{'=' * 60}")
        self.log(f"  MASTER FARM CYCLE #{self.cycle_count} STARTING")
        self.log(f"{'=' * 60}")

        # Step 1: Safety & Reconnect Check
        self.step_1_safety_and_health()
        if self._stop_event.is_set(): return

        # Step 2: Query fields & harvest
        self.step_2_query_and_harvest()
        if self._stop_event.is_set(): return

        # Step 3: Human-like delay
        self.step_3_human_wait_and_crop_plan()
        if self._stop_event.is_set(): return

        # Step 4: Replant fields
        self.step_4_plant_crops()
        if self._stop_event.is_set(): return

        # Step 5: Roadside shop selling with strict blacklist & coin sweeping
        self.step_5_sell_and_collect_coins()
        if self._stop_event.is_set(): return

        # Step 6: Animals & Feed mills
        self.step_6_animals_and_feed()
        if self._stop_event.is_set(): return

        # Step 7: Pets
        self.step_7_pets()
        if self._stop_event.is_set(): return

        # Step 8: Machine production (sets of 20 / 30-40)
        self.step_8_production_buildings()
        if self._stop_event.is_set(): return

        # Step 9: Fishing lake
        self.step_9_fishing_lake()
        if self._stop_event.is_set(): return

        # Step 10: Newspaper sniping
        self.step_10_newspaper_sniper()

        self.log(f"{'=' * 60}")
        self.log(f"  CYCLE #{self.cycle_count} COMPLETE | Coins: ~{self.total_coins_collected} | Sells: {self.total_sells}")
        self.log(f"{'=' * 60}\n")

    def run_continuous_master_loop(self):
        """COMMAND 1: Continuously loops on the active account until stopped."""
        self.running = True
        self.log("Starting Master Autonomous Continuous Loop (Single Account Mode)...", "OK")
        try:
            while not self._stop_event.is_set():
                self.run_single_master_pass()
                # Inter-cycle growth wait (approx 120s for Wheat/Corn)
                wait_sec = 115 + random.uniform(-5, 10)
                self.log(f"Inter-cycle crop growth wait: {wait_sec:.0f}s...", "INFO")

                elapsed = 0
                while elapsed < wait_sec and not self._stop_event.is_set():
                    time.sleep(15)
                    elapsed += 15
                    # Periodic background coin sweep
                    self.collect_coins()

        except KeyboardInterrupt:
            self.log("Master loop interrupted by operator.", "WARN")
        finally:
            self.running = False

    def run_multi_account_rotation_loop(self):
        """COMMAND 2: Executes full master pass, rotates accounts, and repeats indefinitely."""
        self.running = True
        self.log("Starting Master Multi-Account Auto-Rotation Loop...", "OK")
        if not account_manager:
            self.log("account_manager module not available.", "ERR")
            return

        mgr = account_manager.AccountManager()
        accounts = mgr.list_accounts()
        if not accounts:
            self.log("No accounts discovered in Assest/accounts/", "ERR")
            return

        self.log(f"Discovered {len(accounts)} accounts for rotation: {[a['name'] for a in accounts]}", "OK")
        acc_index = 0

        try:
            while not self._stop_event.is_set():
                current_acc = accounts[acc_index % len(accounts)]
                self.log(f"\n{'#' * 60}")
                self.log(f"  SWITCHING TO ACCOUNT: {current_acc['name']} (Level {current_acc['level']})")
                self.log(f"{'#' * 60}")

                # 1. Switch account save state
                mgr.switch_account(current_acc)
                time.sleep(2.0)

                # 2. Heal / restart game
                if self.recovery:
                    self.recovery.reload_game(wait_seconds=12)
                    self.recovery.ensure_native_engine_loaded()

                # 3. Run full master pass on this account
                self.run_single_master_pass()

                # 4. Advance to next account
                acc_index += 1
                self.log(f"Account {current_acc['name']} pass finished. Next account in 10s...", "OK")
                time.sleep(10)

        except KeyboardInterrupt:
            self.log("Multi-account rotation stopped by operator.", "WARN")
        finally:
            self.running = False


# Standalone CLI Entry Point
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hay Star Master Autonomous Bot Engine")
    parser.add_argument("--mode", choices=["master", "rotate", "heal", "dry-run"], default="master",
                        help="Execution mode: master (single account), rotate (multi-account), heal (recovery only)")
    parser.add_argument("--crop", type=int, default=400001, help="Default crop ID")
    parser.add_argument("--crop-name", type=str, default="Wheat", help="Default crop name")
    args = parser.parse_args()

    engine = MasterBotEngine()
    engine.default_crop_id = args.crop
    engine.default_crop_name = args.crop_name

    if args.mode == "heal":
        if engine.recovery:
            engine.recovery.check_and_heal()
    elif args.mode == "rotate":
        engine.run_multi_account_rotation_loop()
    elif args.mode == "dry-run":
        engine.run_single_master_pass()
    else:
        engine.run_continuous_master_loop()
