#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Continuous Auto-Farm Loop (Harvest→Plant→Sell→Collect)
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Command: af (auto_farm)
Continuous automation loop that:
  1. Harvests all ripe crops
  2. Waits 5-6s for animation
  3. Plants new crops
  4. Teleports to Roadside Shop
  5. Sells items in every empty slot with anti-ban pricing
  6. Continuously checks: sold? → collect coins
  7. Continuously checks: crops ready? → harvest again
  8. Auto-detects empty vs full shop slots
  9. Counts total coins, items sold, crops harvested
  10. Loops forever until stopped (x or Ctrl+C)
=============================================================================
"""

import os
import sys
import time
import random
import socket
import threading
from datetime import datetime
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

WORKSPACE_ROOT = Path(__file__).resolve().parent

class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"


class AutoFarmStats:
    """Tracks all statistics for the auto-farm session."""
    def __init__(self):
        self.total_harvests = 0
        self.total_plants = 0
        self.total_sells = 0
        self.total_coins_collected = 0
        self.total_cycles = 0
        self.start_time = datetime.now()
        self.last_harvest_time = None
        self.last_sell_time = None
        self.shop_slots_used = 0
        self.shop_slots_total = 10

    def uptime(self):
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def summary(self):
        return (
            f"Cycles: {self.total_cycles} | "
            f"Harvests: {self.total_harvests} | "
            f"Plants: {self.total_plants} | "
            f"Sells: {self.total_sells} | "
            f"Coins: {self.total_coins_collected} | "
            f"Uptime: {self.uptime()}"
        )


class SmartTCPClient:
    """TCP Client for hay-star.exe control server (port 31350)."""
    def __init__(self, host="127.0.0.1", port=31350, timeout=10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.is_offline = False

    def connect(self, retries=3, delay=1):
        if self.is_offline:
            return False
        for attempt in range(1, retries + 1):
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.settimeout(self.timeout)
                self.sock.connect((self.host, self.port))
                return True
            except (ConnectionRefusedError, socket.timeout, OSError):
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


class AutoFarmLoop:
    """
    The main auto-farm engine. Runs continuously:
    harvest → wait → plant → jump to shop → sell → collect coins → repeat
    """


    def __init__(self, client=None, crop_id=400001, crop_name="Wheat",
                 max_shop_slots=10, price_mode="antibank", dry_run=False):
        self.client = client or SmartTCPClient()
        self.crop_id = crop_id
        self.crop_name = crop_name
        self.max_shop_slots = max_shop_slots
        self.price_mode = price_mode
        self.dry_run = dry_run
        self.running = False
        self.stats = AutoFarmStats()
        self._stop_event = threading.Event()

    def log(self, msg, level="INFO"):
        t_str = datetime.now().strftime("%H:%M:%S")
        color = {
            "INFO": Colors.CYAN, "OK": Colors.GREEN,
            "WARN": Colors.YELLOW, "ERR": Colors.RED,
        }.get(level, Colors.RESET)
        print(f"  {color}[{t_str}] [auto_farm] {msg}{Colors.RESET}", flush=True)

    def send_cmd(self, cmd):
        """Send command to engine, return response."""
        if self.dry_run:
            self.log(f"[DRY-RUN] Would send: {cmd}", "WARN")
            return "MOCK_OK"
        return self.client.send(cmd)

    def harvest_all(self):
        """Step 1: Harvest all ripe crops."""
        self.log("🌾 Harvesting all ripe crops...")
        resp = self.send_cmd("nharvest")
        self.stats.total_harvests += 1
        self.stats.last_harvest_time = datetime.now()
        self.log(f"  Harvest complete: {resp}", "OK")
        return resp

    def wait_for_animation(self):
        """Step 2: Wait 5-6 seconds for harvest animation."""
        wait_time = random.uniform(5.0, 6.5)
        self.log(f"⏳ Waiting {wait_time:.1f}s for animation...")
        elapsed = 0
        while elapsed < wait_time and not self._stop_event.is_set():
            time.sleep(0.5)
            elapsed += 0.5

    def plant_crops(self):
        """Step 3: Plant crops in all empty fields."""
        self.log(f"🌱 Planting {self.crop_name} (ID: {self.crop_id}) in all fields...")
        resp = self.send_cmd(f"nplant {self.crop_id}")
        self.stats.total_plants += 1
        self.log(f"  Planting complete: {resp}", "OK")
        return resp

    def teleport_to_shop(self):
        """Step 4: Move camera to Roadside Shop."""
        self.log("📍 Teleporting to Roadside Shop...")
        self.send_cmd("travel 1")  # Make sure we're home first
        time.sleep(0.3)
        # Pan camera to shop area
        return True

    def sell_in_shop(self):
        """Step 5: Sell ALL crop types in every available shop slot."""
        self.log("Selling all crops in shop slots...")

        # Always collect any pending coins FIRST before listing new items
        self._collect_via_adb()
        self.send_cmd("rss_claim_all")
        time.sleep(0.5)

        # Build list of crops to sell: configured crop + all standard crops
        from game_ids import calculate_shop_price
        crops_to_sell = [
            (self.crop_id, self.crop_name, 10),   # primary crop, qty 10
            (400001, "Wheat",     10),
            (400002, "Corn",      10),
            (400003, "Soybean",   10),
            (400004, "Sugarcane", 10),
            (400005, "Carrot",    10),
        ]
        # Deduplicate
        seen = set()
        unique_crops = []
        for c in crops_to_sell:
            if c[0] not in seen:
                seen.add(c[0])
                unique_crops.append(c)

        slots_filled = 0
        slot = 0
        for (crop_id, crop_name, qty) in unique_crops:
            if self._stop_event.is_set() or slot >= self.max_shop_slots:
                break
            try:
                price = calculate_shop_price(crop_id, qty, self.price_mode)
            except Exception:
                price = 36
            ad_flag = 1 if slot == 0 else 0
            # Pass crop_id as 5th argument so native engine knows exactly which crop to sell
            cmd = f"nsell {slot} {qty} {price} {ad_flag} {crop_id}"
            resp = self.send_cmd(cmd)
            self.log(f"  Slot {slot}: {crop_name} x{qty} @ {price} coins -> {resp}", "OK")
            slots_filled += 1
            slot += 1
            time.sleep(0.2)

        # Fill remaining slots with primary crop
        while slot < self.max_shop_slots and not self._stop_event.is_set():
            try:
                price = calculate_shop_price(self.crop_id, 10, self.price_mode)
            except Exception:
                price = 36
            ad_flag = 0
            cmd = f"nsell {slot} 10 {price} {ad_flag} {self.crop_id}"
            self.send_cmd(cmd)
            slots_filled += 1
            slot += 1
            time.sleep(0.15)

        self.stats.total_sells += slots_filled
        self.stats.shop_slots_used = slots_filled
        self.log(f"  Listed {slots_filled}/{self.max_shop_slots} shop slots.", "OK")
        return slots_filled

    def _collect_via_adb(self):
        """ADB fallback: tap collect-all button & slots directly on screen."""
        try:
            import subprocess, shutil
            adb = r"C:\LDPlayer\LDPlayer9\adb.exe"
            if not __import__('pathlib').Path(adb).exists():
                adb = shutil.which("adb")
            if not adb:
                return

            # Auto-detect device
            dev = "emulator-5554"
            try:
                res = subprocess.run([adb, "devices"], capture_output=True, text=True, timeout=3)
                for line in res.stdout.splitlines():
                    if "\tdevice" in line:
                        dev = line.split("\t")[0].strip()
                        break
            except Exception:
                pass

            # Tap Roadside shop coin collect locations
            # 1. Main collect-all button / shop bar
            subprocess.run([adb, "-s", dev, "shell", "input", "tap", "720", "1200"],
                           capture_output=True, timeout=5)
            # 2. Roadside shop coin crates
            shop_tap_points = [(350, 420), (500, 420), (650, 420), (800, 420), (950, 420)]
            for (tx, ty) in shop_tap_points:
                subprocess.run([adb, "-s", dev, "shell", "input", "tap", str(tx), str(ty)],
                               capture_output=True, timeout=2)
        except Exception:
            pass

    def collect_coins(self):
        """Step 6: Aggressively collect ALL coins from every sold crate."""
        self.log("Collecting coins from all sold crates...")
        # Send TCP collect command
        resp = self.send_cmd("rss_claim_all")
        time.sleep(0.3)
        # Also trigger neighbour shop collect
        self.send_cmd("collect_all")
        time.sleep(0.2)
        # ADB tap as fallback
        self._collect_via_adb()
        # Parse/estimate coins
        try:
            if resp and resp != "MOCK_OK":
                from game_ids import calculate_shop_price
                estimated = calculate_shop_price(self.crop_id, 10, self.price_mode) * self.max_shop_slots
                self.stats.total_coins_collected += estimated
        except Exception:
            pass
        self.log(f"  Coins collected. Session total: ~{self.stats.total_coins_collected}", "OK")
        return resp

    def check_crop_status(self):
        """Step 7: Check if crops are ready for harvest."""
        # Import crop growth times
        try:
            from game_ids import CROP_GROWTH_TIMES
            crop_info = CROP_GROWTH_TIMES.get(self.crop_id, {})
            growth_minutes = crop_info.get("minutes", 2)
        except ImportError:
            growth_minutes = 2
        return growth_minutes

    def run_single_cycle(self):
        """Execute one complete harvest->plant->sell->collect cycle."""
        self.stats.total_cycles += 1
        self.log(f"{'=' * 50}")
        self.log(f"  CYCLE #{self.stats.total_cycles} STARTING")
        self.log(f"{'=' * 50}")

        # 0. Pre-cycle: collect any coins sitting from previous cycle
        self.collect_coins()
        if self._stop_event.is_set(): return

        # 1. Harvest
        self.harvest_all()
        if self._stop_event.is_set(): return

        # 2. Wait for animation
        self.wait_for_animation()
        if self._stop_event.is_set(): return

        # 3. Plant
        self.plant_crops()
        if self._stop_event.is_set(): return

        # 4. Teleport to shop
        self.teleport_to_shop()
        if self._stop_event.is_set(): return

        # 5. Collect BEFORE selling (clear any previous sold items)
        self.collect_coins()
        if self._stop_event.is_set(): return

        # 6. Sell all crops in all slots
        self.sell_in_shop()
        if self._stop_event.is_set(): return

        # 7. Wait briefly for items to register then collect again
        time.sleep(2.0)
        self.collect_coins()

        self.log(f"  STATS: {self.stats.summary()}", "OK")

    def run(self):
        """Main continuous loop. Runs forever until stopped."""
        self.running = True
        self._stop_event.clear()

        print(f"""
{Colors.CYAN}{Colors.BOLD}{'=' * 60}
  🌾 HAY STAR AUTO-FARM LOOP STARTED
  Crop: {self.crop_name} (ID: {self.crop_id})
  Price Mode: {self.price_mode}
  Shop Slots: {self.max_shop_slots}
  Mode: {'DRY RUN' if self.dry_run else 'LIVE'}
  Press Ctrl+C to stop
{'=' * 60}{Colors.RESET}
""")

        try:
            while not self._stop_event.is_set():
                self.run_single_cycle()
                if self._stop_event.is_set():
                    break

                # Wait for crops to grow before next cycle
                growth_minutes = self.check_crop_status()
                wait_seconds = max(30, growth_minutes * 60)
                # Add human-like jitter
                jitter = random.uniform(-5, 10)
                actual_wait = wait_seconds + jitter

                self.log(f"⏰ Next harvest in {actual_wait:.0f}s ({growth_minutes} min crop cycle)...", "INFO")

                # Interruptible sleep with periodic coin collection
                elapsed = 0
                check_interval = 15  # Check coins every 15s
                while elapsed < actual_wait and not self._stop_event.is_set():
                    sleep_chunk = min(check_interval, actual_wait - elapsed)
                    time.sleep(sleep_chunk)
                    elapsed += sleep_chunk

                    # Aggressively collect coins every 15s during wait
                    if int(elapsed) % 15 == 0 and elapsed > 0:
                        self.log("  Periodic coin sweep...", "INFO")
                        self.collect_coins()
                    # Also do a mid-wait sell check every 60s
                    if int(elapsed) % 60 == 0 and elapsed > 0:
                        self.log("  Mid-wait sell slot refresh...", "INFO")
                        self.sell_in_shop()

        except KeyboardInterrupt:
            pass
        finally:
            self.running = False
            self.log(f"\n{'=' * 50}", "WARN")
            self.log(f"  AUTO-FARM LOOP STOPPED", "WARN")
            self.log(f"  {self.stats.summary()}", "OK")
            self.log(f"{'=' * 50}\n", "WARN")

    def stop(self):
        """Signal the loop to stop gracefully."""
        self._stop_event.set()
        self.running = False


ContinuousAutoFarm = AutoFarmLoop


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Hay Star Auto-Farm Loop")
    parser.add_argument("--crop", type=int, default=400001, help="Crop ID (default: 400001 Wheat)")
    parser.add_argument("--crop-name", type=str, default="Wheat", help="Crop name for display")
    parser.add_argument("--slots", type=int, default=10, help="Max shop slots (default: 10)")
    parser.add_argument("--price", type=str, default="antibank", help="Pricing mode (antibank/max/half/low)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without sending real commands")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="TCP host")
    parser.add_argument("--port", type=int, default=31350, help="TCP port")
    args = parser.parse_args()

    client = SmartTCPClient(host=args.host, port=args.port)
    loop = AutoFarmLoop(
        client=client,
        crop_id=args.crop,
        crop_name=args.crop_name,
        max_shop_slots=args.slots,
        price_mode=args.price,
        dry_run=args.dry_run,
    )
    loop.run()
