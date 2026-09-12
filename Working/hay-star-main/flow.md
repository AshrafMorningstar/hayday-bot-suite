# Application Flow & State Machine — Hay Star

## Master User Flow
```mermaid
graph TD
    A[start.bat / launcher.py] --> B{Choose Action}
    B -->|1| C[Full Supervisor + Watchdog]
    B -->|2| D[Continuous Auto-Farm Loop af]
    B -->|3| E[Live Interactive REPL Shell]
    B -->|4| F[Account Switcher as]
    B -->|5| G[Farm Config Engine cr]
    B -->|6| H[Global ID Catalog Search s]
    B -->|7| I[Preflight Installer & Diagnostics]
    B -->|8| J[Full Test Suite 23 Tests]
    B -->|0| K[Exit]

    D --> D1[Harvest Ready Crops]
    D1 --> D2[Wait 5s Animation Jitter]
    D2 --> D3[Plant Next Crop Batch]
    D3 --> D4[Teleport Camera to Shop]
    D4 --> D5[List Crates with Anti-Ban Pricing]
    D5 --> D6[Sweep & Collect Coins]
    D6 --> D7[Sleep Growth Timer + Periodic Sweep]
    D7 --> D1
```

## State Machine: Continuous Auto-Farm Loop (`auto_farm_loop.py`)
1. **STATE_INIT:** Load configurations, connect TCP client or engage dry-run simulation mode.
2. **STATE_HARVEST:** Dispatch `nharvest`, log increment to `stats.total_harvests`.
3. **STATE_ANIM_WAIT:** Wait 5.0s ± 0.5s for scythe swing and silo collection animations.
4. **STATE_PLANT:** Dispatch `nplant <crop_id>`, verify seeds sown.
5. **STATE_JUMP_SHOP:** Execute `execute_jump('shop')` via ADB swipe and TCP signal.
6. **STATE_SELL:** Scan empty crates, list items using safe humanized prices (`antibank`), set newspaper advertisement on crate 0.
7. **STATE_COLLECT:** Send `rss_claim_all` to sweep accumulated coins from sold crates.
8. **STATE_GROWTH_WAIT:** Calculate crop maturity duration (e.g. 120s for wheat). Loop with interruptible sleep while running 15s periodic coin sweeps.
9. **STATE_LOOP:** Repeat cycle until `stop` signal (`x` or `Ctrl+C`).
