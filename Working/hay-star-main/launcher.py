#!/usr/bin/env python3
"""
=============================================================================
Hay Star Interactive Launcher, Mod Manager & Command Terminal
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Comprehensive control center providing:
  1. Interactive Game Assets & Mod Staging Menu (Modes 1-10, ALL, Clean, Skip)
  2. Full Autonomous Supervisor & Watchdog Mode
  3. Continuous Auto-Farm Loop (Harvest→Plant→Sell→Collect)
  4. Live Interactive REPL Terminal (supports all shortcuts: hv, pl, ss, j, etc.)
  5. Multi-Account Switcher & Auto-Rotation (as)
  6. Farm Config & Anti-Ban Pricing (cr)
  7. Global ID Catalog & Search (s / ids)
  8. Environment Preflight Diagnostics & Installer
  9. System Verification Test Suite
=============================================================================
"""

import os
import sys
import subprocess
import time
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


def run_mod_menu():
    """Interactive game asset modification menu."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}=============================================================================
              GAME ASSETS & MOD SELECTION MENU (HAY STAR)
               Created by Ashraf Morningstar | MIT License
============================================================================={Colors.RESET}
Select which game asset modifications to stage into Hay Day before launch:

  {Colors.GREEN}[Mode 1]{Colors.RESET}  mod_01_decision_box        -> Decision Box / Shop rewards & gifts
  {Colors.GREEN}[Mode 2]{Colors.RESET}  mod_02_mystery_boxes        -> Mystery Boxes & Calendar events
  {Colors.GREEN}[Mode 3]{Colors.RESET}  mod_03_greg_shop            -> Greg Roadside Shop & Low Tom price
  {Colors.GREEN}[Mode 4]{Colors.RESET}  mod_04_storage_expansion    -> Barn, Silo & Tackle Box expansion
  {Colors.GREEN}[Mode 5]{Colors.RESET}  mod_05_truck_boat_orders    -> Truck & Boat Predefined Orders
  {Colors.GREEN}[Mode 6]{Colors.RESET}  mod_06_animal_pet_feed      -> Animal Feed Times & Pet Houses
  {Colors.GREEN}[Mode 7]{Colors.RESET}  mod_07_valley_fuel_spin     -> Valley Fuel & Map Game Config
  {Colors.GREEN}[Mode 8]{Colors.RESET}  mod_08_personal_quests      -> Birthday Events & Farm Pass
  {Colors.GREEN}[Mode 9]{Colors.RESET}  mod_09_wheel_of_fortune     -> Daily Wheel of Fortune Rewards
  {Colors.GREEN}[Mode 10]{Colors.RESET} mod_10_seasonal_and_diamonds -> Seasonal Catalogue Gifts & Diamonds

  {Colors.YELLOW}[Mode A]{Colors.RESET}  ALL MODS                    -> Stage ALL 10 Mods combined
  {Colors.CYAN}[Mode 0]{Colors.RESET}  Stock Clean Assets          -> Restore vanilla default assets
  {Colors.DIM}[Mode S]{Colors.RESET}  Skip Staging                -> Skip asset patching & start bot
=============================================================================
"""
    print(banner)
    try:
        import mod_manager
        adb = mod_manager.locate_adb()
    except Exception:
        adb = "adb"

    choice = input(f"{Colors.BOLD}Enter selection [1-10, A, 0, S] (default: S): {Colors.RESET}").strip().upper()
    if not choice:
        choice = "S"

    if choice == "S":
        print("[*] Skipping asset staging...")
    elif choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "A", "0"]:
        print(f"\n[*] Processing selection: Mode [{choice}]...")
        try:
            import mod_manager
            success = mod_manager.stage_to_device([choice], adb_path=adb)
            if success:
                print(f"{Colors.GREEN}[+] Mode [{choice}] successfully staged!{Colors.RESET}\n")
            else:
                print(f"{Colors.YELLOW}[!] Device not currently reachable via ADB. Asset cache prepared locally.{Colors.RESET}\n")
        except Exception as e:
            print(f"{Colors.RED}[!] Staging error: {e}{Colors.RESET}\n")


def run_interactive_repl():
    """Live interactive REPL supporting all commands and 1-3 letter shortcuts."""
    import engine_bot
    import command_registry

    bot = engine_bot.BotAutomationEngine()

    print(f"""
{Colors.CYAN}{Colors.BOLD}=============================================================================
  🌾 HAY STAR — LIVE COMMAND TERMINAL & REPL
  Type any command or shortcut (e.g. hv, pl, j shop, ss, s bread, af, h)
  Type 'exit' or 'q' to return to main menu
============================================================================={Colors.RESET}
""")
    while True:
        try:
            line = input(f"{Colors.GREEN}hay-star > {Colors.RESET}").strip()
            if not line:
                continue
            if line.lower() in ("exit", "quit", "q", "back"):
                break
            bot.execute_command(line)
        except KeyboardInterrupt:
            print("\n[*] Interrupted.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")


def run_emulator_menu():
    """Emulator Manager sub-menu."""
    try:
        import emulator_manager as em
    except ImportError as exc:
        print(f"[!] emulator_manager.py not found: {exc}")
        return

    print(f"""
{Colors.CYAN}{Colors.BOLD}=============================================================================
              EMULATOR MANAGER — LDPlayer 9 Controller
============================================================================={Colors.RESET}
  {Colors.GREEN}[1]{Colors.RESET}  Auto-Setup  — Clone LDPlayer → HayStarBot, launch, start Hay Day
  {Colors.GREEN}[2]{Colors.RESET}  Clone only  — Create HayStarBot copy (do not launch)
  {Colors.GREEN}[3]{Colors.RESET}  Launch      — Start HayStarBot instance
  {Colors.GREEN}[4]{Colors.RESET}  Stop        — Stop HayStarBot instance
  {Colors.GREEN}[5]{Colors.RESET}  Reboot      — Reboot HayStarBot instance
  {Colors.GREEN}[6]{Colors.RESET}  List        — Show all emulator instances
  {Colors.GREEN}[7]{Colors.RESET}  Status      — Show running instances
  {Colors.GREEN}[8]{Colors.RESET}  Run Hay Day — Start game inside HayStarBot
  {Colors.GREEN}[9]{Colors.RESET}  Kill Hay Day— Stop game inside HayStarBot
  {Colors.GREEN}[A]{Colors.RESET}  ADB shell   — Run ADB command in HayStarBot
  {Colors.GREEN}[B]{Colors.RESET}  Backup      — Backup HayStarBot instance
  {Colors.GREEN}[R]{Colors.RESET}  Restore     — Restore latest HayStarBot backup
  {Colors.GREEN}[E]{Colors.RESET}  REPL        — Open full emulator manager REPL
  {Colors.RED}[0]{Colors.RESET}  Back to main menu
=============================================================================""")

    while True:
        ch = input(f"{Colors.BOLD}Emulator> {Colors.RESET}").strip().upper()
        if ch == "0" or ch in ("BACK", "B"):
            break
        elif ch == "1":
            em.auto_setup_and_launch()
        elif ch == "2":
            em.clone_instance()
        elif ch == "3":
            em.launch_instance()
        elif ch == "4":
            em.quit_instance()
        elif ch == "5":
            em.reboot_instance()
        elif ch == "6":
            em.print_instance_table()
        elif ch == "7":
            em.print_status()
        elif ch == "8":
            em.run_app()
        elif ch == "9":
            em.kill_app()
        elif ch == "A":
            cmd = input("  ADB command: ").strip()
            if cmd:
                em.run_adb(cmd)
        elif ch == "B" and ch != "BACK":
            em.backup_instance()
        elif ch == "R":
            em.restore_instance()
        elif ch == "E":
            em.run_repl()
        else:
            print(f"[!] Unknown option '{ch}'.")


def main_dashboard():
    """Top-level master menu for Hay Star."""
    while True:
        print(f"""
{Colors.CYAN}{Colors.BOLD}=============================================================================
                  HAY STAR - MASTER CONTROL DASHBOARD
                 Ashraf Morningstar | MIT License | 2026
============================================================================={Colors.RESET}
  {Colors.GREEN}[1]{Colors.RESET} Launch Full Supervisor (Mod Staging + Watchdog + Bot Engine)
  {Colors.GREEN}[2]{Colors.RESET} Continuous Auto-Farm Loop (Harvest -> Plant -> Sell -> Collect) [af]
  {Colors.GREEN}[3]{Colors.RESET} Live Interactive Command REPL (Type any shortcut: hv, pl, j, ss...)
  {Colors.GREEN}[4]{Colors.RESET} Multi-Account Manager & Save State Switcher [as]
  {Colors.GREEN}[5]{Colors.RESET} Farm Configuration & Anti-Ban Pricing [cr]
  {Colors.GREEN}[6]{Colors.RESET} Global ID Catalog & Item Search [s / ids]
  {Colors.GREEN}[7]{Colors.RESET} Run Preflight Diagnostics & Environment Installer
  {Colors.GREEN}[8]{Colors.RESET} Run Full Automated Test Suite (23 Verification Tests)
  {Colors.GREEN}[9]{Colors.RESET} Emulator Manager (LDPlayer — clone, launch, ADB, backup) [emu]
  {Colors.CYAN}[10]{Colors.RESET} Master 11-Step Farm Loop (All Crops, Animals, Pets, Fish, Snipe) [mc]
  {Colors.CYAN}[11]{Colors.RESET} Master Multi-Account Auto-Rotation Loop [mr]
  {Colors.YELLOW}[12]{Colors.RESET} Auto-Heal & Reconnect Diagnostics [rc]
  {Colors.RED}[0]{Colors.RESET} Exit
=============================================================================
""")
        choice = input(f"{Colors.BOLD}Select an option [0-12]: {Colors.RESET}").strip()

        if choice == "1":
            run_mod_menu()
            supervisor_script = WORKSPACE_ROOT / "supervisor.py"
            print(f"{Colors.CYAN}[*] Handing off control to Hay Star Autonomous Supervisor...{Colors.RESET}\n")
            try:
                subprocess.run([sys.executable, str(supervisor_script)])
            except KeyboardInterrupt:
                print("\n[*] Supervisor stopped.")

        elif choice == "2":
            try:
                import auto_farm_loop
                loop = auto_farm_loop.AutoFarmLoop()
                loop.run()
            except KeyboardInterrupt:
                print("\n[*] Auto-farm stopped.")

        elif choice == "3":
            run_interactive_repl()

        elif choice == "4":
            try:
                import account_manager
                account_manager.interactive_cli()
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == "5":
            try:
                import config_automation
                config_automation.interactive_menu()
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == "6":
            try:
                import game_ids
                q = input("Enter item name or ID to search (or press Enter for summary): ").strip()
                if q:
                    game_ids.print_search(q)
                else:
                    game_ids.print_category_summary()
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == "7":
            try:
                import install
                installer = install.Installer()
                installer.run_all()
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == "8":
            try:
                import tests.test_all
                tests.test_all.run_tests()
            except Exception as e:
                print(f"[!] Error: {e}")

        elif choice == "9":
            run_emulator_menu()

        elif choice == "10":
            try:
                import master_bot_engine
                bot = master_bot_engine.MasterBotEngine()
                bot.run_continuous_master_loop()
            except KeyboardInterrupt:
                print("\n[*] Master loop stopped.")

        elif choice == "11":
            try:
                import master_bot_engine
                bot = master_bot_engine.MasterBotEngine()
                bot.run_multi_account_rotation_loop()
            except KeyboardInterrupt:
                print("\n[*] Multi-account rotation stopped.")

        elif choice == "12":
            try:
                import recovery_manager
                mgr = recovery_manager.RecoveryManager()
                mgr.check_and_heal()
            except Exception as e:
                print(f"[!] Recovery error: {e}")

        elif choice in ("0", "q", "exit"):
            print("\n[*] Exiting Hay Star. Happy farming!\n")
            break
        else:
            print(f"[!] Invalid option '{choice}'.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ("mod", "mods", "stage"):
            run_mod_menu()
        elif arg in ("repl", "cli", "shell"):
            run_interactive_repl()
        elif arg in ("af", "autofarm", "auto_farm"):
            import auto_farm_loop
            loop = auto_farm_loop.AutoFarmLoop()
            loop.run()
        elif arg in ("mc", "master", "master_cycle"):
            import master_bot_engine
            bot = master_bot_engine.MasterBotEngine()
            bot.run_continuous_master_loop()
        elif arg in ("mr", "rotate", "master_rotate"):
            import master_bot_engine
            bot = master_bot_engine.MasterBotEngine()
            bot.run_multi_account_rotation_loop()
        elif arg in ("rc", "heal", "reconnect", "auto_heal"):
            import recovery_manager
            mgr = recovery_manager.RecoveryManager()
            mgr.check_and_heal()
        elif arg in ("emu", "emulator", "em"):
            # Emulator manager: pass remaining args through
            import emulator_manager
            # Rebuild argv so emulator_manager.main() parses correctly
            sys.argv = ["emulator_manager"] + sys.argv[2:]
            emulator_manager.main()
        elif arg in ("clone",):
            import emulator_manager
            src  = sys.argv[2] if len(sys.argv) > 2 else emulator_manager.DEFAULT_SOURCE_INSTANCE
            dest = sys.argv[3] if len(sys.argv) > 3 else emulator_manager.DEFAULT_BOT_INSTANCE
            emulator_manager.clone_instance(source=src, dest=dest)
        elif arg in ("launch-emu", "launchemu"):
            import emulator_manager
            name = sys.argv[2] if len(sys.argv) > 2 else emulator_manager.DEFAULT_BOT_INSTANCE
            emulator_manager.launch_instance(name)
        else:
            # Dispatch command directly to engine_bot
            import engine_bot
            bot = engine_bot.BotAutomationEngine()
            bot.execute_command(" ".join(sys.argv[1:]))
    else:
        main_dashboard()
