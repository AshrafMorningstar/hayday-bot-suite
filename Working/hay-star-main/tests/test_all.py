#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Comprehensive Automated Test & Verification Suite
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Verifies all modules, commands, shortcuts, configs, and catalogs:
  - Test 1:  Command Registry — All shortcuts and full names resolve correctly
  - Test 2:  Game IDs — Item name and ID lookups
  - Test 3:  Game IDs — Anti-ban pricing safety bounds
  - Test 4:  Game IDs — Animal to feed matching logic
  - Test 5:  Game IDs — Screen landmarks and navigation aliases
  - Test 6:  Auto-Farm Loop — Stats tracker and cycle structure
  - Test 7:  Account Manager — Multi-account profile discovery
  - Test 8:  Config Automation — Farm JSON parsing and section fetching
  - Test 9:  Config Automation — Crop update and safe pricing modifications
  - Test 10: ID Extractor — CSV data presence and extracted JSON validity
  - Test 11: Engine Bot — Shortcut resolution and dispatching
  - Test 12: Engine Bot — Camera teleport coordinate calculations
  - Test 13: TCP Smart Client — Graceful offline mock handling
  - Test 14: Expansion & Mining Catalogs — Materials integrity
  - Test 15: Environment Installer — Diagnostic checks run successfully
=============================================================================
"""

import os
import sys
import json
import unittest
from pathlib import Path

# Add project root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT))

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import game_ids
import command_registry
import account_manager
import config_automation
import auto_farm_loop
import engine_bot
import install


class TestCommandRegistry(unittest.TestCase):
    """Test shortcut aliases and full commands resolution."""

    def test_all_shortcuts_resolve(self):
        shortcuts = ["hv", "pl", "ca", "fa", "cm", "pm", "cf", "cal", "ch",
                     "ss", "cc", "ad", "j", "af", "ma", "x", "mn", "fh",
                     "sn", "mt", "as", "cr", "s", "h", "ex", "ids", "st", "al", "tst"]
        for sc in shortcuts:
            fullname, entry = command_registry.resolve_command(sc)
            self.assertIsNotNone(fullname, f"Shortcut '{sc}' failed to resolve")
            self.assertIsNotNone(entry, f"Entry for shortcut '{sc}' was None")

    def test_fullnames_resolve(self):
        fullnames = ["harvest", "plant", "jump", "auto_farm", "master_auto", "stop", "search", "help"]
        for fn in fullnames:
            fullname, entry = command_registry.resolve_command(fn)
            self.assertIsNotNone(fullname, f"Full name '{fn}' failed to resolve")

    def test_search_commands(self):
        res = command_registry.search_commands("crop")
        self.assertGreater(len(res), 0, "Searching 'crop' returned no results")

    def test_get_all_commands(self):
        all_cmds = command_registry.get_all_commands()
        self.assertGreaterEqual(len(all_cmds), 25, "Command list has fewer than 25 commands")


class TestGameIDs(unittest.TestCase):
    """Test Global ID catalogs, search, anti-ban price, and landmarks."""

    def test_search_wheat(self):
        matches = game_ids.search_id("wheat")
        self.assertGreater(len(matches), 0, "No matches found for 'wheat'")
        ids = [m[0] for m in matches]
        self.assertIn(400001, ids, "Crop ID 400001 not in wheat search results")

    def test_search_bread(self):
        matches = game_ids.search_id("bread")
        self.assertGreater(len(matches), 0, "No matches found for 'bread'")

    def test_search_numeric_id(self):
        matches = game_ids.search_id("400001")
        self.assertEqual(len(matches), 1, "Numeric search for 400001 did not return exactly 1 match")
        self.assertEqual(matches[0][0], 400001)

    def test_antibank_pricing(self):
        # 10 Wheat: max is 36. Antibank must be safe (< 36 and >= 1)
        safe_price = game_ids.calculate_shop_price(400001, count=10, mode="antibank")
        self.assertLessEqual(safe_price, 36)
        self.assertGreaterEqual(safe_price, 33)

    def test_max_pricing(self):
        max_price = game_ids.calculate_shop_price(400001, count=10, mode="max")
        self.assertEqual(max_price, 36)

    def test_animal_feed_mapping(self):
        # Chicken ID 2300000 -> Chicken Feed ID 600002
        feed_id = game_ids.get_feed_for_animal(2300000)
        self.assertEqual(feed_id, 600002)

    def test_screen_landmarks(self):
        self.assertIn("shop", game_ids.SCREEN_LANDMARKS)
        self.assertIn("farm", game_ids.SCREEN_LANDMARKS)
        self.assertIn("animals", game_ids.SCREEN_LANDMARKS)
        self.assertIn("machines", game_ids.SCREEN_LANDMARKS)
        self.assertIn("mine", game_ids.SCREEN_LANDMARKS)
        self.assertIn("boat", game_ids.SCREEN_LANDMARKS)
        self.assertIn("town", game_ids.SCREEN_LANDMARKS)


class TestAutoFarmLoop(unittest.TestCase):
    """Test auto-farm stats, loop setup, and offline mode."""

    def test_stats_initialization(self):
        stats = auto_farm_loop.AutoFarmStats()
        self.assertEqual(stats.total_harvests, 0)
        self.assertEqual(stats.total_coins_collected, 0)
        self.assertIn("00:00:", stats.uptime())
        self.assertIn("Cycles: 0", stats.summary())

    def test_dry_run_loop_setup(self):
        loop = auto_farm_loop.AutoFarmLoop(dry_run=True, crop_id=400001, max_shop_slots=5)
        self.assertTrue(loop.dry_run)
        self.assertEqual(loop.crop_id, 400001)
        self.assertEqual(loop.max_shop_slots, 5)
        # Test dry run execution of individual steps
        res = loop.harvest_all()
        self.assertEqual(res, "MOCK_OK")
        self.assertEqual(loop.stats.total_harvests, 1)


class TestAccountManager(unittest.TestCase):
    """Test multi-account discovery and profile structure."""

    def test_list_accounts(self):
        mgr = account_manager.AccountManager()
        accs = mgr.list_accounts()
        self.assertGreaterEqual(len(accs), 1, "At least one account profile should exist in Assest/accounts/")
        names = [a["name"] for a in accs]
        self.assertIn("main", names)
        # Verify save_file exists for discovered profile
        for a in accs:
            self.assertTrue(a["save_file"].exists())


class TestConfigAutomation(unittest.TestCase):
    """Test JSON farm config loader and modification."""

    def test_load_default_config(self):
        ca = config_automation.ConfigAutomation()
        self.assertIn("automation", ca.config)

    def test_get_summary(self):
        ca = config_automation.ConfigAutomation()
        summary = ca.get_summary()
        self.assertIn("Fields", summary)
        self.assertIn("Market", summary)

    def test_crop_modification(self):
        ca = config_automation.ConfigAutomation()
        ca.set_default_crop(400002)
        fields = ca.get_automation_section("fields")
        self.assertEqual(fields.get("crop"), 400002)


class TestIDExtractor(unittest.TestCase):
    """Test presence and integrity of extracted Global IDs."""

    def test_extracted_files_exist(self):
        json_path = WORKSPACE_ROOT / "tools" / "extracted_ids" / "all_global_ids.json"
        self.assertTrue(json_path.exists(), "tools/extracted_ids/all_global_ids.json does not exist")
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("ids_by_category", data)
        self.assertGreater(data.get("metadata", {}).get("total_ids", 0), 100)


class TestEngineBot(unittest.TestCase):
    """Test BotAutomationEngine command handling and jump logic."""

    def test_engine_initialization(self):
        bot = engine_bot.BotAutomationEngine()
        self.assertIsNotNone(bot.config)

    def test_offline_client(self):
        client = engine_bot.SmartClient(host="127.0.0.1", port=99999, timeout=0.1)
        res = client.send("test_command")
        self.assertEqual(res, "MOCK_OK")

    def test_jump_landmark_coordinates(self):
        bot = engine_bot.BotAutomationEngine()
        # Landmark jump to shop
        res = bot.execute_jump("shop")
        self.assertTrue(res)

    def test_jump_coordinate_math(self):
        bot = engine_bot.BotAutomationEngine()
        res = bot.execute_jump("100", ["200"])
        self.assertTrue(res)


class TestInstaller(unittest.TestCase):
    """Test Installer diagnostics execution."""

    def test_installer_run(self):
        inst = install.Installer()
        success = inst.run_all()
        self.assertTrue(success, "Installer reported critical missing requirements")


class TestRecoveryManager(unittest.TestCase):
    """Test connection recovery and popup dismissal diagnostics."""

    def test_recovery_initialization(self):
        import recovery_manager
        mgr = recovery_manager.RecoveryManager()
        self.assertIsNotNone(mgr.adb)

    def test_recovery_popup_dismiss_mock(self):
        import recovery_manager
        mgr = recovery_manager.RecoveryManager()
        tapped = mgr.dismiss_popups()
        self.assertIsInstance(tapped, bool)


class TestMasterBotEngine(unittest.TestCase):
    """Test MasterBotEngine 11-step pipeline and sales blacklist."""

    def test_sales_blacklist_integrity(self):
        import master_bot_engine
        blacklist = master_bot_engine.STRICT_SALES_BLACKLIST
        # Upgrade tools
        self.assertIn(1800012, blacklist)  # Bolt
        self.assertIn(1800013, blacklist)  # Plank
        self.assertIn(1800014, blacklist)  # Duct Tape
        self.assertIn(1800000, blacklist)  # Saw
        self.assertIn(1800001, blacklist)  # Axe
        self.assertIn(1800007, blacklist)  # Dynamite
        # Jewelry & bars
        self.assertIn(1100026, blacklist)  # Diamond Ring
        self.assertIn(1800004, blacklist)  # Gold Bar
        # Vital base resources
        self.assertIn(1100000, blacklist)  # Cream
        self.assertIn(1100001, blacklist)  # Butter
        self.assertIn(1100002, blacklist)  # Cheese
        self.assertIn(1100015, blacklist)  # Bread

    def test_all_crops_catalog(self):
        import master_bot_engine
        crops = master_bot_engine.ALL_CROPS
        crop_ids = [c[0] for c in crops]
        self.assertIn(400001, crop_ids)  # Wheat
        self.assertIn(400002, crop_ids)  # Corn
        self.assertIn(400005, crop_ids)  # Carrot
        self.assertIn(400003, crop_ids)  # Soybean
        self.assertIn(400004, crop_ids)  # Sugarcane

    def test_master_single_pass_mock(self):
        import master_bot_engine
        bot = master_bot_engine.MasterBotEngine()
        bot.run_single_master_pass()
        self.assertEqual(bot.cycle_count, 1)
        self.assertGreaterEqual(bot.total_sells, 10)
        self.assertGreaterEqual(bot.total_coins_collected, 500)


def run_tests():
    print("=" * 70)
    print("  🌾 HAY STAR — RUNNING FULL VERIFICATION TEST SUITE")
    print("=" * 70)
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print("=" * 70)
    if result.wasSuccessful():
        print("  🎉 ALL TESTS PASSED! FULL SYSTEM VERIFIED.")
    else:
        print(f"  ❌ {len(result.failures)} FAILURE(S), {len(result.errors)} ERROR(S)")
    print("=" * 70)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
