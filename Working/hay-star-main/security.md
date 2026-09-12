# Security & Anti-Detection Architecture — Hay Star

## Stealth & Ban-Mitigation Strategy
Automation detection in Supercell games revolves around statistical anomalies, timing patterns, and memory inspection. Hay Star enforces multi-layer safeguards:

1. **Anti-Ban Humanized Pricing:**
   - Instead of static maximum prices that flag automated listing algorithms, `game_ids.calculate_shop_price(..., mode='antibank')` computes a dynamic discount (subtracting 1 to 3 coins from the maximum ceiling).
   - Prevents identical pricing fingerprints across bulk sales.

2. **Timing Jitter & Random Delays:**
   - All harvest, planting, animal feeding, and machine queues incorporate randomized floating-point delays (e.g. 5.2s to 6.8s for crop harvest animations).
   - Natural human pause distribution eliminates fixed-cadence bot signatures.

3. **Daily Expansion Material Caps:**
   - Enforces a hard daily cap of 80/80 items (`EXPANSION_DAILY_CAP`) for newspaper sniper purchases to comply with Supercell's internal account throttling rules.

4. **Frida Memory Stealth & Guard Bundles:**
   - `java_guard.bundle.js` and `quago_probe.bundle.js` hook root checks, emulator indicators, and telemetry endpoints.
   - Prevents integrity check failures inside `libg.so`.

5. **Safe Save-State Injection:**
   - Account swaps safely terminate `com.supercell.hayday` before modifying `storage_new.xml`.
   - File permissions are explicitly adjusted to `chmod 660` with UID matching Hay Day's app sandbox to prevent file corruption or permission denial errors.

## Error Handling & Recovery Matrix
| Failure Scenario | Detection Strategy | Autonomous Recovery Action |
|---|---|---|
| Emulator Crash | ADB heartbeat timeout | `supervisor.py` restarts package via `am start` |
| Native Server Disconnect | TCP ConnectionRefused / Timeout | `SmartClient` reconnects up to 3 times, then falls back to safe simulation |
| Shop Out-of-Sync | Empty slot mismatch | Re-queries shop state and pings camera to `shop` landmark |
| Storage Full | Machine/harvest return code | Dispatches roadside shop dump batch to clear silo/barn |
