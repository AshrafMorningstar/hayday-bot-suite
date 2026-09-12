# Extras & Change Notes

## Extra Implementation Steps & Gotchas
1. **Multi-Engine Support**: The suite automatically detects binary executables (`hay-star.exe`, `hdxc.exe`), Python supervisor scripts (`supervisor.py`), Frida hooks (`frida_bridge.py`), and TypeScript/C++ engines.
2. **ADB Emulator Auto-Detection**: Integrates automatic scanning for Android emulators (LDPlayer, BlueStacks, Nox, MEMu) on ports 5555, 5554, 62001, 7555.
3. **Double-Click Launchers**: Includes `run.bat` and `start.bat` to bypass Windows PowerShell script execution policy restrictions.
5. **Windows stdout Closure Gotcha**: On Windows Python 3.12+, wrapping `sys.stdout` multiple times with `io.TextIOWrapper` causes the prior wrappers to close the underlying C stdio buffer when GC runs. The permanent fix is calling `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` instead of constructing new wrapper objects.
6. **ADB Socket Pre-Check Gotcha**: Directly executing `adb connect` against closed loopback ports causes long timeouts (2-10s) and raises unhandled `subprocess.TimeoutExpired`. Pre-probing with a fast Python `socket.connect_ex` with 0.3s timeout guarantees 0 hangs.
7. **13-Subsystem Simulation Engine**: Implemented simulation pass in `start_bot.py --test` which simulates all 13 farm operations with timestamps and persists real JSON snapshots to `Working/hay-star-main/logs/snapshots/` for offline testing.
8. **Legal Safe Harbor & Fair Use**: Added extensive non-infringement clauses, trademark disclaimers, and DMCA § 1201 anti-circumvention defenses to `LICENSE` to protect open-source educational research.


