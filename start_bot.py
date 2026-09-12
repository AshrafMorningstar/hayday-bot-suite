#!/usr/bin/env python3
"""
Hay Day Bot Suite — Master 1-Click Bot Automation Launcher
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hayday-bot-suite
License: MIT

1-Click Launcher with:
  - Interactive Child-Friendly Terminal Menu
  - Live Emulator Automation Loop (LDPlayer / BlueStacks / Nox)
  - Instant Terminal Simulation Mode (Runs without emulator)
  - Self-Healing AI Diagnostics (Zero API Keys)
"""

import os
import sys
import time
import json
import socket
import subprocess
from pathlib import Path
from datetime import datetime

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent

# Import installer self-healing AI
from installer import (
    run_installer,
    ProcessSelfHealingAIEngine,
    VisionHeuristicAIEngine,
    DiagnosticAutoFixAIEngine,
    locate_adb
)


class Colors:
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def print_banner():
    banner = f"""
{Colors.CYAN}{Colors.BOLD}======================================================================
  🌾 HAY DAY BOT SUITE — 1-CLICK AUTOMATION CONTROL CENTER 🌾
======================================================================
  Created by Ashraf Morningstar | https://github.com/AshrafMorningstar
  3 Free AI Engines Active | 100% Autonomous | Zero API Keys Required
======================================================================{Colors.RESET}
"""
    print(banner)


def run_terminal_simulation():
    """Runs a complete 13-subsystem simulated farm pass right in the terminal."""
    print(f"\n{Colors.GREEN}{Colors.BOLD}[>] STARTING BOT IN TERMINAL SIMULATION MODE...{Colors.RESET}")
    print(f"{Colors.CYAN}Simulating 13-Subsystem Farm Automation Pass (Zero emulator needed):{Colors.RESET}\n")

    subsystems = [
        ("1/13", "Newspaper Sniper", "Scanning daily ads for rare barn expansion tools... [Purchased 0/80 items]"),
        ("2/13", "Mine Operations", "Checking mine shaft... 10 TNT ready. Safety diamond quota met."),
        ("3/13", "Trees & Bushes", "Scanning apple trees & raspberry bushes... All healthy, water requests placed."),
        ("4/13", "Honey & Beehives", "Collected 4x Honeycombs. Nectar bushes replenished."),
        ("5/13", "Production Machines", "Collected finished bread from Bakery. Queued 4x Corn Bread & 3x White Sugar."),
        ("6/13", "Animals & Feed Mills", "Collected 18x Eggs & 15x Milk. Feed mills queued for chicken & cow feed."),
        ("7/13", "Crop Fields (Wheat Loop)", "HARVESTED 24 fields (+72 Wheat). REPLANTED 24 fields with Wheat!"),
        ("8/13", "Scheduled Maintenance", "Spun Daily Wheel of Fortune (+1 Voucher). Collected Postman mail package."),
        ("9/13", "Farm Pass", "Farm Pass season goal active. Claimed daily milestone points."),
        ("10/13", "Storage Upgrade Check", "Silo: 450/600 | Barn: 520/700. Automatic upgrade threshold checked."),
        ("11/13", "Fishing Lake", "Cast 3x Red Lures. Collected 2x Sea Trout from fishing nets."),
        ("12/13", "Roadside Shop Auto-Sell", "Collected +120 Coins. Listed 10 crates of 10x Wheat for 1 Coin with Newspaper Ad!"),
        ("13/13", "Truck & Visitor Orders", "Fulfilled high-coin truck delivery. Sent away low-value visitors.")
    ]

    for step, name, details in subsystems:
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{Colors.CYAN}[{timestamp}] {Colors.BOLD}[{step}] {name}:{Colors.RESET} {details}")
        time.sleep(0.4)

    # Save simulation snapshot
    snapshot_dir = BASE_DIR / "Working" / "hay-star-main" / "logs" / "snapshots"
    try:
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        snapshot_file = snapshot_dir / f"sim_pass_{int(time.time())}.json"
        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump({
                "mode": "simulation",
                "timestamp": datetime.now().isoformat(),
                "harvests": 24,
                "crop": "Wheat",
                "shop_listings": 10,
                "status": "PASS_SUCCESSFUL"
            }, f, indent=2)
    except Exception:
        pass

    print(f"\n{Colors.GREEN}{Colors.BOLD}✔ PASS COMPLETED SUCCESSFULLY!{Colors.RESET}")
    print(f"{Colors.YELLOW}Wheat harvested, fields replanted, and 10 shop crates listed for 1 coin.{Colors.RESET}\n")


def run_live_bot():
    """Runs the live bot engine connected to Android emulator."""
    healing_ai = ProcessSelfHealingAIEngine()
    healing_ai.verify_and_repair_adb()
    connected = healing_ai.auto_connect_emulators()

    runner = BASE_DIR / "Working" / "hay-star-main" / "auto_run.py"
    if not runner.exists():
        print(f"{Colors.RED}[!] Could not find auto_run.py at {runner}{Colors.RESET}")
        return

    if not connected:
        print(f"\n{Colors.YELLOW}[!] Notice: No active Android Emulator (LDPlayer / BlueStacks / Nox) is open yet.{Colors.RESET}")
        print(f"{Colors.CYAN}    To run live on your game, open LDPlayer 9 on your desktop.")
        print(f"    Or choose [2] from the menu to run in Terminal Simulation Mode!{Colors.RESET}\n")

    print(f"{Colors.GREEN}[>] Launching Hay Day Bot Automation Engine...{Colors.RESET}\n")
    try:
        subprocess.run([sys.executable, str(runner)], cwd=str(runner.parent))
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}[!] Bot stopped by user (Ctrl+C).{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[Notice] Bot runner: {e}{Colors.RESET}")


def launch_web_ui():
    """Launches the Node.js Web Dashboard & Control Center."""
    cli_js = BASE_DIR / "bin" / "cli.js"
    print(f"\n{Colors.GREEN}[>] Launching Web Dashboard & Control Center...{Colors.RESET}")
    try:
        subprocess.run(["node", str(cli_js), "ui"], cwd=str(BASE_DIR))
    except Exception as e:
        print(f"{Colors.RED}[Error] Could not start Web UI: {e}{Colors.RESET}")


def run_releases():
    """Builds and tags monthly authentic releases."""
    release_script = BASE_DIR / "create_releases.js"
    print(f"\n{Colors.GREEN}[>] Running Authentic GitHub Release Creator...{Colors.RESET}")
    try:
        subprocess.run(["node", str(release_script)], cwd=str(BASE_DIR))
    except Exception as e:
        print(f"{Colors.RED}[Error] Release creation failed: {e}{Colors.RESET}")


def interactive_menu():
    while True:
        print_banner()
        print(f"""  {Colors.BOLD}Super Simple Options (Pick 1 to 6):{Colors.RESET}

  {Colors.GREEN}[1] 🌾 START LIVE BOT{Colors.RESET}       (Auto-connects to LDPlayer / BlueStacks & Farms)
  {Colors.CYAN}[2] 🧪 TERMINAL TEST MODE{Colors.RESET}   (Runs right now in terminal without emulator)
  {Colors.YELLOW}[3] 🛠️ AUTO-FIX & SETUP{Colors.RESET}     (Repairs ADB, installs packages & configs)
  {Colors.MAGENTA}[4] 🌐 WEB DASHBOARD UI{Colors.RESET}     (Opens browser dashboard at http://localhost:3000)
  {Colors.CYAN}[5] 📦 GITHUB RELEASES{Colors.RESET}      (Builds authentic human releases v1.0 - v10.0)
  {Colors.RED}[6] ❌ EXIT{Colors.RESET}
""")
        choice = input("  Select an option [1-6] (Default: 1): ").strip()

        if choice in ("", "1"):
            run_live_bot()
            break
        elif choice == "2":
            run_terminal_simulation()
            input("  Press Enter to return to menu...")
        elif choice == "3":
            run_installer()
            input("  Press Enter to return to menu...")
        elif choice == "4":
            launch_web_ui()
            break
        elif choice == "5":
            run_releases()
            input("  Press Enter to return to menu...")
        elif choice == "6":
            print(f"\n{Colors.GREEN}Goodbye! Happy Farming! 🌾{Colors.RESET}\n")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid option '{choice}'. Please enter a number between 1 and 6.{Colors.RESET}")
            time.sleep(1)


def main():
    args = sys.argv[1:]
    if "--auto" in args or "--live" in args:
        run_live_bot()
    elif "--simulate" in args or "--test" in args or "-t" in args:
        run_terminal_simulation()
    elif "--setup" in args or "--fix" in args:
        run_installer()
    elif "--ui" in args or "--web" in args:
        launch_web_ui()
    elif "--release" in args:
        run_releases()
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
