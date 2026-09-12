# Architectural Decisions Log — Hay Day Bot Suite

## ADR 01: Unified 1-Click Control Center & Dual-Mode Execution
- **What was decided**: Build a unified master runner (`start_bot.py`), 1-click batch files (`run.bat`, `install.bat`), and Web Dashboard (`public/`). Provide both Live Android Emulator mode and instant Terminal Simulation Mode (`--test`).
- **Why it was needed**: Users were confused by fragmented scripts across folders that crashed or required manual terminal commands.
- **Alternatives considered**: Separate loose scripts (rejected because casual users cannot configure them).
- **Impact**: Anyone, including a 7-year-old child, can double-click and see the bot working immediately.

## ADR 02: Windows stdout Reconfiguration over io.TextIOWrapper
- **What was decided**: Replaced all `io.TextIOWrapper` wrapping of `sys.stdout.buffer` with `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- **Why it was needed**: Python 3.12+ garbage collection of previous text wrappers closes the underlying C stdio buffer, throwing fatal `ValueError: I/O operation on closed file`.
- **Alternatives considered**: Environment variables (unreliable in Windows cmd/bat).
- **Impact**: Permanent zero-crash fix for terminal printing across all Python modules.

## ADR 03: Pre-Flight Socket Probing for ADB Emulators
- **What was decided**: Probe loopback ports (5555, 5554, 62001, 7555, 21503) using non-blocking Python sockets (0.3s timeout) before triggering `adb connect`.
- **Why it was needed**: Unconditional `adb connect` commands hang and trigger unhandled `subprocess.TimeoutExpired` when emulators are offline.
- **Alternatives considered**: Catching `TimeoutExpired` only (slower, takes 2-10s per port).
- **Impact**: Instant, sub-second emulator port resolution with zero hangs.

## ADR 04: 3 Free Zero-API-Key AI Engines
- **What was decided**: Integrate Vision OCR, Self-Healing ADB, and Auto-Fixing Diagnostic AI engines without requiring paid API keys or tokens.
- **Why it was needed**: Users must not be required to configure OpenAI or cloud keys for bot automation or self-healing.
- **Impact**: 100% free, autonomous, and private offline operation.
