# 🌾 Hay Day Bot Suite (v8.0.0 Milestone)
> The Unified, Autonomous Hay Day Farm Automation & Bot Control Center. Powered by 3 Free AI Engines with Zero API Keys required.

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License MIT" />
  <img src="https://img.shields.io/badge/Python-3.9+-green.svg?style=for-the-badge&logo=python" alt="Python 3.9+" />
  <img src="https://img.shields.io/badge/Node.js-18+-brightgreen.svg?style=for-the-badge&logo=node.js" alt="Node.js 18+" />
  <img src="https://img.shields.io/badge/AI-100%25%20Free%20(Zero%20Keys)-purple.svg?style=for-the-badge" alt="Free AI" />
  <img src="https://img.shields.io/badge/Emulators-LDPlayer%20%7C%20BlueStacks%20%7C%20Nox%20%7C%20MEmu-orange.svg?style=for-the-badge" alt="Emulators" />
</p>

---

## 🌟 Why Hay Day Bot Suite?

Every Hay Day player knows how tedious harvesting wheat, managing roadside shop sales, and feeding farm animals can get after hours of manual tapping. **Hay Day Bot Suite** is a unified, 1-click automated control center built to automate farm loops safely and efficiently:

- 🌾 **Auto-Wheat & Crop Farming Loop**: Automatic harvesting, planting, and roadside shop listing.
- 🤖 **3 Free AI Engines (Zero API Keys)**:
  1. *Vision & OCR Heuristic AI Engine*: Detects crops, field coordinates, roadside shop slots, and full storage.
  2. *Self-Healing Process & ADB AI Engine*: Automatically recovers ADB connections, unlocks ports, and connects emulators.
  3. *Autonomous Diagnostic & Auto-Bug-Fixing AI Engine*: Scans runtime logs and auto-repairs configurations without requiring paid API keys.
- ⚡ **1-Click Automatic Setup**: Double-click `run.bat` or `install.bat` — designed so simply that even a 7-year-old child can run it.
- 🧪 **Terminal Simulation Mode**: Test and run all 13 farm subsystems directly in the terminal without even having an emulator open.
- 🖥️ **Universal Emulator Support**: Auto-connects to **LDPlayer, BlueStacks, Nox, MEmu, and MuMu Player** on default loopback ports (5555, 5554, 62001, 7555, 21503).
- 🛡️ **Pre-Flight Safety Guard**: Checks for sensitive data leaks, zero hardcoded credentials, and respects Supercell trademark guidelines.

---

## 🚀 Quick Start (Under 10 Seconds)

### Option 1: 1-Click Double-Click (Easiest)
1. Double-click **`run.bat`** (or **`install.bat`** for setup).
2. Follow the friendly interactive menu or let it auto-start!

### Option 2: Command Line
```bash
# 1. Automatic 1-click installer and dependency fixer
python installer.py

# 2. Launch Hay Day interactive bot launcher
python start_bot.py

# 3. Test in Terminal Simulation Mode (No emulator required!)
python start_bot.py --test

# 4. Launch Web Studio & Control Center
node bin/cli.js ui
```

---

## 🛠️ The 13 Farm Subsystems

| # | Subsystem | Functionality | Technology |
|:---|:---|:---|:---|
| **1** | **Newspaper Sniper** | Scans daily newspaper and auto-buys rare expansion tools up to 80-item daily cap | Python 3, ADB Input |
| **2** | **Mine Operations** | Deploys dynamite and TNT up to safety diamond conservation limit | Pure-Python-ADB |
| **3** | **Trees & Bushes** | Harvests mature orchards and posts help requests for wilted trees | Heuristic Vision OCR |
| **4** | **Honey & Beehives** | Collects honeycomb and ensures nectar bushes remain replenished | Heuristic Vision OCR |
| **5** | **Production Machines** | Collects completed goods from Bakery, Dairy, Sugar Mill & queues recipes | State Machine Queue |
| **6** | **Animals & Feed Mills** | Collects eggs/milk, feeds animal pens, and queues feed mill production | Multi-Slot Dispatcher |
| **7** | **Crop Fields (Wheat Loop)** | High-speed 120s wheat harvest & replanting cycle | Touch Macro Dispatcher |
| **8** | **Scheduled Maintenance** | Collects daily Postman mail, wheel of fortune, and mystery packages | Event Scheduler |
| **9** | **Farm Pass** | Collects free daily milestones and season pass reward targets | Milestone Parser |
| **10** | **Storage Upgrade Check** | Analyzes Silo & Barn inventory thresholds and auto-expands when ready | Inventory Ledger |
| **11** | **Fishing Lake** | Casts red lures, clears lobster pools, and resets fishing nets | Map Coordinates Jump |
| **12** | **Roadside Shop Auto-Sell** | Claims coins and lists 10 crates of 10x wheat for 1 coin with newspaper ads | RSS Automation API |
| **13** | **Truck & Visitor Orders** | Filters high-value delivery orders and dismisses low-coin visitors | Order Evaluator |

---

## 📦 Version History & Release Downloads

For full humanly-written changelogs and standalone release downloads spanning **v1.0.0 (2016)** to **v8.0.0 (2026)**, view the [**Release Chronicle (RELEASES.md)**](RELEASES.md).

---

## ⚖️ Copyright & Legal Protection System

- **Copyright (c) 2016–2026 Ashraf Morningstar**. All Rights Reserved.
- **Trademark Notice**: *Hay Day* and *Supercell* are registered trademarks of Supercell Oy. This project is an independent open-source educational automation and accessibility tool and is NOT affiliated with, endorsed by, or supported by Supercell.
- **Fair Use & Accessibility**: Distributed under the MIT License and U.S. Copyright Act Fair Use provisions (17 U.S.C. § 107).
- **DMCA Protection**: Operates exclusively in user-space via standard ADB input protocols with zero digital rights management (DRM) circumvention (17 U.S.C. § 1201).