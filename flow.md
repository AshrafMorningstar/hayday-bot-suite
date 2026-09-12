# App Flow & User Journey — Hay Day Bot Suite

```mermaid
flowchart TD
    A[User Launches Suite] --> B{Entry Method}
    B -->|Double-Click| C[run.bat / install.bat]
    B -->|Terminal| D[python start_bot.py]
    B -->|Web CLI| E[node bin/cli.js ui]

    C --> F[Pre-Flight AI Diagnostic]
    D --> F
    
    F --> G[Check Dependencies & Port Probes]
    G --> H{Interactive Menu}
    
    H -->|Option 1| I[🌾 Live Farm Bot]
    H -->|Option 2| J[🧪 Terminal Simulation Mode]
    H -->|Option 3| K[🛠️ Auto-Fix & Setup]
    H -->|Option 4| L[🌐 Web Dashboard]
    H -->|Option 5| M[📦 GitHub Releases]
    H -->|Option 6| N[Exit]

    I --> O{Emulator Active?}
    O -->|Yes| P[Attach Native Loader & Execute 13 Subsystems Loop]
    O -->|No| Q[Alert User: Open LDPlayer or Run Option 2]

    J --> R[Simulate 13 Subsystems in Terminal & Save JSON Snapshot]
    K --> S[Install Packages, Cycle ADB, Stage 10 Mods, Heal Config]
    L --> T[Serve Web UI at http://localhost:3000]
    M --> U[Generate RELEASES.md & Tag Releases]
```

## User Journey Stages
1. **Entry**: Single click on `run.bat` starts the engine immediately.
2. **Detection**: Port probes identify if LDPlayer 9 / BlueStacks is open on loopback.
3. **Execution**: If emulator is active, wheat loop runs autonomously every 120s; if not, user can immediately test with option 2.
4. **Monitoring**: User views real-time harvest counters and coin logs in the terminal or web dashboard.
5. **Self-Healing**: If a game crash or ADB drop occurs, the watchdog cycles the connection and re-attaches automatically.
