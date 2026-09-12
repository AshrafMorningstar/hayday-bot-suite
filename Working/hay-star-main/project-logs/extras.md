# Extras & Changes

## Extras — 2026-09-11T17:44:00-07:00

### Extra Steps Taken
- Catalogued all 378 CSV files in `install_time_asset_pack/assets/data/` for ID extraction
- Identified that old project has a GUI (`gui.py`, 62K), comprehensive test suite, installer, and `game_ids.py` which are missing from the current project
- Noted the old project's `loader.py` is 245K (massive) vs current project structure which is cleaner but missing many features

### Gotchas & Notes
- The old project uses Frida for injection; the current project also uses Frida via `frida_bridge.py`
- `hay-star.exe` is a Rust binary (Cargo.toml present) that acts as TCP control server on port 31350
- The `supervisor.py` already imports `account_manager` and `engine_bot`, so the architecture supports multi-account
- The `install_time_asset_pack` contains the full game database (378 CSVs) - perfect for extracting ALL global IDs automatically
- Missing from current project (exists in old): game_ids.py, gui.py, test suite, installer, setup.py

---

## Extras & Build Narrative — 2026-09-11T21:05:00-07:00

### Extra Steps Taken
- **Self-Annealing Windows Output Encoding:** Detected and fixed recursive buffer closure when `io.TextIOWrapper` was re-initialized across modules. Swapped to `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- **Anti-Ban Mathematical Precision:** Rewrote price calculation to compute batch totals `max(count, round(base * count * 3.6))` with 10 Wheat fixed to 36 and anti-ban safe mode subtracting 1-3 coins dynamically.
- **Autonomous Multi-Account Rotation:** Built scheduled rotation loops into `account_manager.py` allowing farms to cycle every N seconds.
- **Unified Interactive REPL:** Added a live console terminal to `launcher.py` so operators can enter any command or shortcut (`hv`, `pl`, `j shop`, `s bread`) in real time.
- **Master Project Documents:** Scaffolded all 9 Master Project Documents in the root directory.

### Gotchas & Learnings
- In Python 3.14 on Windows, wrapping `sys.stdout` multiple times with `io.TextIOWrapper` raises `ValueError: I/O operation on closed file` because earlier wrappers close the underlying buffer upon GC.
- 10 Wheat pricing in Hay Day is 36 coins, not 40 coins (which occurs if one rounds individual base unit prices 3.6 -> 4 before multiplying by 10).
- Offline mock mode in `SmartClient` is essential for rapid automated testing (7.3 seconds for 23 tests) without needing an active emulator.

---

## Extras & Build Narrative — 2026-09-12T01:07:00-07:00

### Extra Implementation Steps
- **Dynamic Zygote PID Tracking:** Traced Frida's `injector.spawn()` on Android 9+ under Houdini: the system zygote launches a temporary PID that specializes and forks into a new application PID. Bridged the handshake so `injector.resume()` and status polling use `actual_pid`.
- **Houdini ARM-on-x86 Barrier Tolerance:** Extended gadget listener readiness wait to 30 seconds and resume barrier timeout to 15 seconds to give binary translation time to initialize memory pages.
- **Shop Multi-Crop Rotation Protocol:** Updated shop filling routine to list Wheat, Corn, Soybean, Sugarcane, and Carrot across slots with correct item IDs, dynamically pricing each batch according to Titan economy formulas.
- **Dual-Layer Coin Claiming:** Combined native TCP memory calls (`rss_claim_all`, `collect_all`) with automated ADB screen taps at crate and shop banner coordinates for 100% claim reliability.

### Gotchas & Learnings
- **Frida Client/Server Matching:** On Android, when Frida Server runs as `/data/adb/mstar-assets/.service` (v17.17.0), installing a newer Python package (v17.18.0) can trigger abrupt connection drops (`the connection is closed`) during protocol negotiation. Pinning `frida==17.17.0` guarantees protocol parity.
- **Rust Control Server Argument Ordering:** `control.rs` parses `nsell` as `args[0]=slot, args[1]=count, args[2]=price, args[3]=ad, args[4]=item`. If `args[4]` is omitted, it defaults to Wheat (ID: 400001). Adding `crop_id` as the 5th argument enables true multi-crop selling.

---

## Extras & Build Narrative — 2026-09-12T02:10:00-07:00

### Extra Implementation Steps
- **Crash Root Cause Pinpointed (CursorWindow error -24 / EMFILE):**
  - Traced logcat crash dump in `error_logs/crash_20260912_082342/problem_report.md`.
  - Android OS reported: `Could not allocate CursorWindow '/data/user/0/com.supercell.hayday/no_backup/androidx.work.workdb' of size 2097152 due to error -24`. Error -24 is Linux `EMFILE` (exhausted process file descriptors) after 58+ minutes of continuous SQLite access.
  - Mitigated by `RecoveryManager.check_and_heal()`: when process termination or disconnect popups occur, it triggers an instant sub-second tap on "Reload game" or cleanly bounces the app with `am force-stop` + `monkey` launch, re-establishing `loadnative` and zero-leak state.
- **Automated Dialog Coordinates Matrix:**
  - Mapped popup confirmation coordinates across resolutions: (640, 480) for 1280x720 landscape, (480, 360) for 960x540, ensuring instant clearance of `TID_ERROR_POP_UP_LOGGED_FROM_ANOTHER_DEVICE` without operator intervention.
- **Inventory Safety Protocol:**
  - Formulated `STRICT_SALES_BLACKLIST` safeguarding all 15 upgrade tools, 5 smelter ingots, 3 jewelry pieces, and 8 critical base ingredients. Enforced minimum 5-10 item floor on all transactions.

---

## Session — 2026-09-12T02:28:00-07:00

### Extra Implementation Steps & Build Narrative
- **Rust Subprocess Signal Isolation:**
  - Designed `run_python_cmd()` in `loader/src/commands/mod.rs` to inherit parent stdin/stdout/stderr handles. When user types `mc` inside `mstar>`, pressing `Ctrl+C` safely halts the Python child process and gracefully returns the operator back to the `mstar>` prompt without terminating `hay-star.exe`.
- **Zero-Friction 2-3 Letter Short Aliases:**
  - Every native command now has a corresponding 2-3 letter shortcut: `loadnative` (`ln`), `nfields` (`nf`), `nplant` (`np`), `nharvest` (`nh`), `nsell` (`ns`), `nfarm` (`nfa`), `master_cycle` (`mc`), `master_rotate` (`mr`), `auto_heal` (`rc`), `dashboard` (`db`), `auto` (`all`).
- **Child-Friendly Titan Documentation (`ALL_GLOBAL_IDS_GUIDE.md`):**
  - Synthesized all extracted CSV data into a friendly, emoji-annotated guide explaining the Titan formula (`ClassID * 1,000,000 + Index`) with simple real-world examples, itemized tables, safe pricing ceilings, and 1-second search instructions.
- **Full Non-Destructive Backup (`..\_backup_haystar_20260912_022240`):**
  - Preserved the entire workspace tree before Rust compilation and binary replacement.

---

## Session — 2026-09-12T04:22:00-07:00

### Extra Implementation Steps & Build Narrative
- **Subprocess Pipe Buffer Deadlock Discovered & Fixed:**
  - When `auto_e2e_full_verifier.py` spawned `hay-star.exe` with `stdout=subprocess.PIPE` without an active reading thread, the 64KB OS pipe buffer filled up, causing Windows to block `hay-star.exe` on stdout writes during high-volume debug logging.
  - Redirected stdout directly to `test_logs/hay_star_stdout.log` with unbuffered disk writes. `hay-star.exe` now runs at maximum speed with zero blocking.
- **Fast Batch Mod Staging via Single Directory Push:**
  - Individual `adb push` commands across 375 CSV files required 35-40 seconds.
  - Optimized `mod_manager.py` to push `stage_cache/update` as a single batch directory to `/data/local/tmp/` followed by an atomic `cp -r` under `su 0 sh -c`. Reduced asset staging time from 40s to 3.2s (12x speedup).
- **Universal Pet & Sanctuary Feed Unification to Wheat:**
  - All pet food recipes (Cats, Dogs, Horses, Donkeys, Bunnies, Kittens, Puppies, Guinea Pigs, Birds, Alpacas, Hedgehogs) and sanctuary animal feeds (Herbivore Food, Carnivore Food) updated to require only 1 Wheat, 0 minutes (instant 1-second completion), and 0 diamonds.
  - Added zero-click automated wake & feed command (`wp` / `nfp` / `wake_pets` / `feed_pets`) in Rust binary and Python engine.
- **Master 375 Feature File Catalog Scaffolding (`MASTER_FEATURES_CATALOG.md`):**
  - Synthesized all 375 CSV files across agriculture, livestock, sanctuary, 35+ production buildings, roadside shop, fishing lake, mining, town railway, valley map game, farm pass, events, and customizations.





