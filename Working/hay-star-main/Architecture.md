# Technical Architecture Document — Hay Star

## Tech Stack
- **Native Core Engine:** Rust (`loader/src/`, compiled to `hay-star.exe`) listening on TCP port 31350 for low-level memory commands.
- **Hooking & Instrumentation:** Frida (`hook.js`, `java_guard.bundle.js`, `quago_probe.bundle.js`) for anti-detection and runtime interception.
- **High-Level Automation Layer:** Python 3.9+ (`engine_bot.py`, `auto_farm_loop.py`, `config_automation.py`, `account_manager.py`).
- **Bridge & Device Interface:** Android Debug Bridge (ADB) via subprocess for device touch gestures, APK detection, and save-state swapping.
- **Data & Configuration:** JSON (`Assest/configs/farm/loll.json`, `tools/extracted_ids/all_global_ids.json`), CSV databases (`install_time_asset_pack/`).

## Workspace Structural Map
```
hay-star-main/
├── hay-star.exe                  # Compiled native Rust TCP control engine (port 31350)
├── launcher.py                   # Master control dashboard & interactive REPL shell
├── start.bat                     # Quick launcher with shortcut cheat-sheet
├── engine_bot.py                 # Full 13-subsystem automation engine & command dispatcher
├── auto_farm_loop.py             # Continuous harvest→plant→sell→collect automation loop
├── command_registry.py           # Universal registry mapping 1-3 letter shortcuts to full commands
├── game_ids.py                   # Complete Supercell Titan Global ID catalog & landmark coordinates
├── config_automation.py          # Interactive JSON config tuner & hot-reloader
├── account_manager.py            # Multi-account save-state switcher & rotation scheduler
├── mod_manager.py                # Asset staging engine for mods 1-10
├── supervisor.py                 # Watchdog supervisor monitoring emulator and bot health
├── install.py / install.bat      # Environment diagnostic suite and dependency installer
├── tools/
│   ├── id_extractor.py           # Auto-scanner parsing 375+ CSV game database files
│   └── extracted_ids/            # Extracted machine-readable Global IDs JSON and text logs
├── tests/
│   ├── test_all.py               # Comprehensive 23-test verification suite
│   └── run_tests.bat             # 1-click test runner
├── Assest/
│   ├── accounts/                 # Account profile directories containing storage_new.xml
│   └── configs/farm/loll.json    # Master farm configuration file
├── _backup_2026-09-11/           # Timestamped project backup
├── _reference_docs/              # Reference documentation library
└── project-logs/                 # Continuous work, decision, progress, and extras logs
```

## Communication Architecture (A.N.T. 3-Layer Build)
- **Layer 1: Architecture (`architecture/` & Core Docs):** Specifications defining Titan Global ID math, anti-ban pricing equations, and TCP packet formats.
- **Layer 2: Navigation & Routing:** `command_registry.py` and `engine_bot.py` route high-level commands, resolve shortcuts, and manage flow control.
- **Layer 3: Tools & Execution:** Deterministic scripts (`auto_farm_loop.py`, `account_manager.py`, `tools/id_extractor.py`) executing specific atomic farm actions.

## Inter-Process Communication (IPC)
- Python components connect via TCP sockets to `127.0.0.1:31350` to issue newline-delimited command strings (e.g. `nharvest\n`, `nplant 400001\n`, `rss_claim_all\n`).
- If `hay-star.exe` is offline, `SmartClient` gracefully falls back to mock simulation mode (`MOCK_OK`) to ensure non-blocking operation during tests and standalone runs.
