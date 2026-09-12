# Dynamic Working Memory — Hay Star

## Active System State
- **Workspace:** `c:/Users/Admin/Documents/hay-star-main`
- **Environment:** Windows (Python 3.14.7, ADB at `C:\LDPlayer\LDPlayer9\adb.exe`)
- **System Health:** 23/23 tests passing (100% pass rate).
- **Core Components:**
  - `hay-star.exe`: Compiled native control engine (port 31350)
  - `launcher.py`: Master dashboard & live REPL shell
  - `engine_bot.py`: 13-subsystem automation engine & command dispatcher
  - `auto_farm_loop.py`: Continuous loop engine
  - `command_registry.py`: Universal 1-3 letter shortcuts
  - `game_ids.py`: Master Global ID database & anti-ban pricing
  - `config_automation.py`: JSON config tuner & hot-reloader
  - `account_manager.py`: Multi-account manager & save switcher
  - `tools/id_extractor.py`: Auto-scanner for 375+ asset CSVs
  - `install.py`: Preflight installer & diagnostic check
  - `tests/test_all.py`: Full verification test suite

## Graphify Conceptual Map
```
[User / start.bat]
        │
        ▼
   [launcher.py]
   ├── Mod Menu [mod_manager.py]
   ├── REPL Shell ──► [command_registry.py] ──► [engine_bot.py]
   ├── Auto-Farm ──► [auto_farm_loop.py] ──► [game_ids.py]
   ├── Accounts ──► [account_manager.py] ──► [ADB / storage_new.xml]
   ├── Config Engine ──► [config_automation.py] ──► [loll.json]
   └── Diagnostics ──► [install.py] & [tests/test_all.py]
                              │
                              ▼
                       [hay-star.exe:31350]
```
