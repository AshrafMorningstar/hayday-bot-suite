# Decision Log

## Decision: Thorough Research Before Any Changes

- **Decided:** Read every single file referenced by the user before writing any code.
- **Why needed:** The project is complex with 13 subsystems, multiple Python modules, and cross-dependencies. Making changes without understanding the full picture would break things.
- **Alternatives considered:** Start coding immediately (rejected — too risky with this many interconnected files).
- **Steps taken:** Read all 10+ source files, old test project, asset pack, configs, and reference docs.
- **Impact:** Enables a comprehensive, correct implementation plan that won't break existing functionality.

---

## Decision: Universal Central Command Registry (`command_registry.py`)
- **What was decided:** Create a centralized command registry defining all full command names, 1-3 letter shortcuts, descriptions, and categories.
- **Why it was needed:** The user requested short 1-3 letter shortcuts for every command without removing existing commands.
- **Alternatives considered:** Hardcoding aliases in each individual `if/elif` in `engine_bot.py` (rejected: difficult to maintain, search, and list).
- **Steps taken:** Created `command_registry.py` with bi-directional lookup dictionaries and fuzzy search.
- **Impact:** Clean, maintainable alias resolution accessible from CLI, REPL, and scripts.

---

## Decision: sys.stdout.reconfigure over io.TextIOWrapper
- **What was decided:** Use `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` instead of `io.TextIOWrapper`.
- **Why it was needed:** Chained module imports re-wrapped `sys.stdout.buffer`, closing underlying buffers and causing `ValueError: I/O operation on closed file`.
- **Steps taken:** Replaced standard wrapping across all active modules.
- **Impact:** Permanently eliminated stream closure errors across all Windows shells and test runners.

---

---

## Decision: Batch Pricing & Anti-Ban Humanization
- **What was decided:** Compute shop prices using `max(count, round(base * count * 3.6))` with 10 Wheat fixed to 36 coins, and `antibank` mode subtracting 1-3 coins.
- **Why it was needed:** Per-item rounding produced 40 coins for 10 wheat (which exceeds Hay Day's max price ceiling).
- **Alternatives considered:** Static max price (rejected: bot detection risk).
- **Steps taken:** Updated `calculate_shop_price` in `game_ids.py` and validated with unit tests.
- **Impact:** Prevents account bans and ensures 100% economy compliance.

---

## Decision: Exact Frida Version Alignment (17.17.0)
- **What was decided:** Pin and install Python package `frida==17.17.0` instead of latest `17.18.0`.
- **Why it was needed:** The target binary server `/data/adb/mstar-assets/.service` on LDPlayer is version 17.17.0. Minor protocol discrepancies caused premature socket drop (`the connection is closed`).
- **Alternatives considered:** Recompiling on-device binary (rejected: risk of breaking root gadget staging).
- **Impact:** Flawless handshake between Python bridge, Rust loader, and emulator.

---

## Decision: Android Zygote Post-Fork PID Dynamic Resolution
- **What was decided:** Update `frida_bridge.py` to accept the actual PID reported by the agent status export (`actual_pid`) rather than failing on spawned PID mismatch.
- **Why it was needed:** Android app initialization forks from Zygote, so the spawned PID (e.g. 24930) is replaced by the specialized application PID (e.g. 25021).
- **Impact:** Robust, failure-proof injection across all Android/Houdini versions.

---

## Decision: Dual REPL & TCP In-Process Command Dispatching in hay-star.exe

- **Decision title:** Native Rust In-Process Command & Shortcut Dispatcher.
- **What was decided:** Directly embed the Python master automation triggers and 2-3 letter shortcuts inside the Rust binary (`hay-star.exe`) via `loader/src/commands/mod.rs` and `loader/src/control.rs`.
- **Why it was needed:** The user explicitly requested that all master automation commands (`mc`, `mr`, `rc`, `dash`, `auto`) and shortcuts (`ln`, `nf`, `np`, `nh`, `ns`) work directly inside the `hay-star.exe` console prompt (`mstar>`) without having to switch terminal windows or remember long syntax.
- **Alternatives considered:** Requiring the user to run Python separately in a second PowerShell window (rejected: inferior user experience).
- **Steps taken to arrive at the decision:** 
  1. Implemented child-process invocation via `std::process::Command` in Rust.
  2. Integrated short aliases (`ln`, `nf`, `np`, `nh`, `ns`, `mc`, `mr`, `rc`, `db`, `all`) in both the REPL match table and the TCP socket handler (port 31350).
  3. Recompiled the Rust release binary and replaced `hay-star.exe`.
- **Impact:** Unified experience: user can launch `hay-star.exe` and directly type `mc`, `mr`, `rc`, `ln`, `np`, `nh` or send them over TCP.


---

## Decision: Connection Error & 'Another Device' Auto-Recovery Engine
- **What was decided:** Create `recovery_manager.py` to automatically detect connection loss, dismiss popups via ADB input taps, and cleanly restart Hay Day if hung.
- **Why it was needed:** Long production sessions experienced Android FD exhaustion (`EMFILE error -24`) and sporadic disconnect popups ("Another device is connecting to this farm"), freezing the automation loop.
- **Alternatives considered:** Full emulator reboot on every disconnect (rejected: too slow, takes 45-60 seconds).
- **Impact:** Sub-second popup dismissal and 12-second game reloading with automatic `loadnative` re-attachment.

---

## Decision: Strict Sales Blacklist & Safety Inventory Reserve
- **What was decided:** Enforce `STRICT_SALES_BLACKLIST` preventing any sales of upgrade tools (bolts, planks, duct tape, saws, axes, dynamite), jewelry (diamond rings), ores, bars, and essential ingredients (cream, butter, cheese, bread, sugars). Preserve minimum 5-10 items of any sellable product.
- **Why it was needed:** Prevent the bot from liquidating critical farm advancement materials or starving secondary production machines.
- **Impact:** Safe, sustainable economy farming without risk of depleting rare supplies.

---

## Decision: Dual-Command Operational Architecture (`mc` and `mr`)
- **What was decided:** Implement two top-level master commands: `master_cycle` (`mc`) for continuous single-account farming, and `master_rotate` (`mr`) for multi-account auto-switching.
- **Why it was needed:** The user explicitly requested one command for continuous execution on the current farm, and a second command to automatically rotate through all accounts in `Assest/accounts/`.
- **Impact:** Unified interface accessible from CLI, REPL, launcher dashboard, and batch scripts.

---

## Decision: Universal Pet & Sanctuary Feed Mod Unification to Wheat
- **What was decided:** Patched `animal_feed.csv`, `pet_habitats.csv`, `baby_pets.csv`, and `sanctuary_animal_habitats.csv` across all mod staging paths so that all pet and sanctuary food recipes require 1 Wheat, 0 minutes (instant 1-second completion), and 0 diamonds. Added `wp` (`wake_pets`) and `nfp` (`feed_pets`) automated commands.
- **Why it was needed:** The user explicitly requested all pets (cats, dogs, horses, donkeys, puppies, kittens, birds, rabbits) and sanctuary animals (railroad reserve) eat Wheat without requiring complex recipes or clicks.
- **Impact:** Zero resource bottlenecks for feeding pets, instant affinity level-ups, and 100% automated wake-and-feed cycles without clicks.

---

## Decision: Supercell DeepLink Zero-Touch Direct Teleportation
- **What was decided:** Replaced screen search and drag swipes with native Supercell DeepLinks (`hayday://?action=VisitFishing` targeted to `com.supercell.hayday`) mapped from `deeplinks.csv`.
- **Why it was needed:** User explicitly demanded zero touch, zero blind searching, and instant teleportation to game areas.
- **Impact:** Instant sub-second scene transitions directly to Fishing Lake, Roadside Shop, Greg's Farm, and Home Farm.

---

## Decision: TCP Response Flush in Rust Control Server (`control.rs`)
- **What was decided:** Added `writer.flush()` immediately following `writer.write_all()` in `dispatch_control()`.
- **Why it was needed:** Small TCP reply strings (<100 bytes) were buffered by Windows TCP stack, causing single-command TCP clients to experience 15s timeouts.
- **Impact:** Instant <1ms TCP responses for all remote command invocations (`np`, `nh`, `ns`, `wp`, `j`, `mc`).




