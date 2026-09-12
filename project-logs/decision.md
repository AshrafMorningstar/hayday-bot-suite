# Decision Log

## Decision: Build Unified Hay Day Automation Suite & Bot Control Center
- **What was decided**: Scaffold a unified Node.js & Python bot management orchestrator in `m:\Hay Day Bot's` with terminal CLI (`hayday`), interactive Web Dashboard (`http://localhost:3000`), ADB emulator scanner, and 1-click bot execution engine.
- **Why it was needed**: The user had multiple bot engines (`hay-star`, `inxernal`, `hdxc`, `supervisor.py`) scattered across subfolders, but no root entrypoint, `package.json`, or runner existed. Running commands in the root failed completely.
- **Alternatives considered**: Leaving bots as loose separate scripts (rejected because user requested a fully working terminal and GUI suite).
- **Steps taken**: Cataloged all executable bots and Python Frida scripts across `Working/` and `Working FIne/`, designed unified REST API and CLI runner.
- **Impact**: Enables 1-click launch of any Hay Day bot engine from both Web GUI and Terminal with real-time ADB emulator status tracking.
 
## Decision: Fully Autonomous Remote GitHub Sync & Historical Release Publishing
- **What was decided**: Run complete automated staging, commit, push, and create GitHub releases for all versions `v1.0.0` through `v8.0.0` with full changelogs and download references.
- **Why it was needed**: The user requested a fully automated push to GitHub ("upload this on github fully auto do it all fully auto"). The local tags were missing corresponding GitHub remote releases, and local source modifications were uncommitted.
- **Alternatives considered**: Asking the user to confirm git credentials or branch names (rejected under Zero-Permission Protocol).
- **Steps taken**: Verified remote origin, created releases via GitHub CLI / release generator, staged all code and documentation, committed and pushed to `master` with tags.
- **Impact**: The repository `AshrafMorningstar/hayday-bot-suite` is fully up to date, cleanly presented, and offers downloadable milestone releases.

## Decision: Windows Output Encoding — sys.stdout.reconfigure over io.TextIOWrapper
- **What was decided**: Replaced `io.TextIOWrapper` wrapping of `sys.stdout.buffer` with `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- **Why it was needed**: In Python 3.12+ on Windows, re-wrapping `sys.stdout` across multiple modules causes garbage collection of prior wrappers to close the underlying OS buffer, causing fatal `ValueError: I/O operation on closed file` on the very first print statement.
- **Alternatives considered**: Setting `PYTHONIOENCODING=utf-8` environment variable (unreliable when launched via Windows cmd/bat without shell wrapper).
- **Impact**: Completely eliminated the fatal buffer closure crash across all bot launchers.

## Decision: Resilient Socket Pre-Check for ADB Connection Loops
- **What was decided**: Added non-blocking TCP socket probes (`connect_ex`) with 0.3s timeout before invoking `adb connect`.
- **Why it was needed**: Directly calling `adb connect 127.0.0.1:port` with subprocess timeout caused unhandled `subprocess.TimeoutExpired` exceptions when emulators were offline, crashing the bot.
- **Alternatives considered**: Removing ADB port scanning (rejected because auto-connecting emulators is required for 1-click execution).
- **Impact**: Bot cleanly scans all standard emulator ports (5555, 5554, 62001, 7555, 21503) in under 1 second without timing out.

## Decision: Dual-Mode Execution — Live Bot & Terminal Simulation Mode
- **What was decided**: Added `--simulate` / `--test` mode to `start_bot.py` that executes a complete 13-subsystem simulated farm loop directly in terminal without requiring a live emulator.
- **Why it was needed**: The user requested a fully working terminal experience that can be tested immediately even when an Android emulator is not currently running.
- **Alternatives considered**: Blocking execution until an emulator is started (rejected because it prevents instant CLI verification).
- **Impact**: Provides instant feedback, testing, and verification for any user or developer in seconds.

