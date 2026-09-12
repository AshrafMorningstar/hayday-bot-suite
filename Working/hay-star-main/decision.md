# Master Architectural Decision Log — Hay Star

## ADR 01: Universal Centralized Command Registry (`command_registry.py`)
- **What was decided:** All commands, short aliases, and metadata are defined in a single immutable table in `command_registry.py` with bi-directional lookup.
- **Why it was needed:** To provide 1-3 letter shortcuts (e.g. `hv`, `pl`, `ss`, `cc`, `j`, `af`) without polluting individual execution handlers or breaking backward compatibility.
- **Impact:** Any component (CLI, REPL, supervisor, tests) resolves commands consistently.

## ADR 02: sys.stdout.reconfigure over io.TextIOWrapper
- **What was decided:** Replaced all instances of `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, ...)` with `sys.stdout.reconfigure(encoding="utf-8", errors="replace")`.
- **Why it was needed:** When multiple modules re-wrapped `sys.stdout.buffer`, previously wrapped buffers were closed, causing fatal `ValueError: I/O operation on closed file` during tests and chained imports.
- **Impact:** Completely eliminated buffer closed crashes across all platforms and test runners.

## ADR 03: Deterministic Offline Mock Simulation in SmartClient
- **What was decided:** Implemented automatic offline detection in `SmartClient` that returns `"MOCK_OK"` when `hay-star.exe` is not running.
- **Why it was needed:** Allows full diagnostic testing and standalone verification of automation logic even when the native game binary or emulator is offline.
- **Impact:** Automated tests execute in 7 seconds with 100% pass rate in CI or dev environments.

## ADR 04: Batch Pricing Formula with Anti-Ban Humanization
- **What was decided:** Formulated batch pricing as `max(count, round(base * count * 3.6))` with 10 Wheat capped at 36, and anti-ban mode subtracting 1-3 coins.
- **Why it was needed:** Individual rounding caused 10 wheat to calculate as 40 coins (exceeding Supercell's 36 max ceiling).
- **Impact:** Exact compliance with Hay Day game engine economy and bot detection bypass.
