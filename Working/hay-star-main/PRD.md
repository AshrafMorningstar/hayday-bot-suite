# Product Requirements Document (PRD) — Hay Star Overhaul

## Problem Statement
Hay Day players and automation developers require an ultra-reliable, high-performance, and stealthy automation system capable of executing multi-step farm management (harvesting, planting, livestock handling, machine queuing, roadside shop selling, mining, and fishing) without manual intervention or account bans. Previous iterations lacked short command shortcuts, automated CSV ID extraction, anti-ban randomized pricing, seamless account rotation, and integrated diagnostics.

## Target Users
- **Farm Automators & Testers:** Developers and power users seeking hands-free, continuous farm progression.
- **Multi-Account Farm Managers:** Users operating several farms (e.g. main level 86, feeder farms level 55) requiring automated save-state switching.
- **Game Reverse Engineers:** Analysts needing structured Supercell Titan Global IDs and packet/memory injection hooks.

## Product Vision
Hay Star is the definitive, all-in-one Supercell Hay Day automation suite combining compiled Rust high-speed memory control, stealth Frida hooking, an extensive Titan Global ID catalog, anti-ban randomized pricing, 1-3 letter shortcuts, and autonomous recovery loops.

## Core Features
1. **Timestamped Project Backup & Reference Organization** (`must-have`): Full codebase preservation and reference document categorization.
2. **Master Titan Global ID Catalog (`game_ids.py`)** (`must-have`): Complete database of crops, feeds, recipes, buildings, tools, and screen landmarks with fuzzy lookup.
3. **Global ID Auto-Extractor (`tools/id_extractor.py`)** (`must-have`): Dynamic CSV parser scanning game asset archives (375+ CSVs) into machine-readable JSON.
4. **1-3 Letter Shortcut System (`command_registry.py`)** (`must-have`): Universal alias system (e.g., `hv`, `pl`, `ss`, `cc`, `j`, `af`, `x`) preserving all legacy commands.
5. **Continuous Auto-Farm Loop (`auto_farm_loop.py`)** (`must-have`): Complete harvest → plant → sell → collect cycle with coin counters and uptime stats.
6. **Camera Teleport & Landmark Navigation** (`must-have`): Instant camera panning to shop, farm, livestock, machines, mine, boat, and town via ADB gestures and TCP packets.
7. **Multi-Account Switcher & Auto-Rotation (`account_manager.py`)** (`must-have`): Seamless save swapping (`storage_new.xml`) with Linux permission fixes and rotation scheduling.
8. **Config-Driven Automation Engine (`config_automation.py`)** (`must-have`): Interactive parameter tuning, section toggles, and TCP hot-reloading (`cr`).
9. **Environment Preflight Diagnostics & Installer (`install.py`, `install.bat`)** (`must-have`): One-click verification of Python, ADB, emulator, root, and bundles.
10. **Automated Diagnostic Test Suite (`tests/test_all.py`, `tests/run_tests.bat`)** (`must-have`): Comprehensive 23-test verification suite covering every subsystem.
11. **Master Control Dashboard (`launcher.py`, `start.bat`)** (`must-have`): Unified interactive launcher with mod staging, live REPL shell, and bot execution.

## App Flow Summary
1. User starts `start.bat` or `python launcher.py`.
2. Environment is validated via preflight checks.
3. User selects mod staging or chooses live bot modes:
   - Option 1: Full Supervisor with crash watchdog
   - Option 2: Continuous Auto-Farm Loop (`af`)
   - Option 3: Live Interactive REPL (`hv`, `pl`, `j shop`, `ss`, etc.)
   - Option 4: Account Switcher (`as`)
   - Option 5: Farm Config Engine (`cr`)
4. Execution proceeds autonomously, logging stats and maintaining stealth.

## Success Metrics
- **Pass Rate:** 100% test pass rate across all 23 verification tests.
- **Shortcuts:** Zero collision across 28+ 1-3 letter shortcuts.
- **Safety:** Anti-ban pricing strictly below maximum ceilings.
- **Zero-Failure Fallback:** Offline mock responses when TCP server is offline during testing.

## Out of Scope (Version 1)
- Modification of compiled native binary internal bytecode (`hay-star.exe` operates as a black-box TCP server on port 31350).
- Cloud-hosted remote web dashboard (focus is local emulator and standalone automation).
