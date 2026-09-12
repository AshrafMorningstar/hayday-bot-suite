# 01 Product Requirements Document (PRD) — Hay Day Bot Suite

## 1. Problem Statement
Hay Day is a beloved farming simulation game, but manual crop harvesting, repetitive replanting, livestock feeding, and clearing full silo storage through the roadside shop require hundreds of repetitive screen taps every hour. Players face gameplay fatigue and time constraints. Existing open-source scripts are fragmented across disconnected repositories, lack self-healing capabilities, break on Android ADB reconnects, or require complex manual terminal setups that casual users cannot operate.

## 2. Target Users
- **Primary Users**: Hay Day enthusiasts, farm management players, and casual gamers seeking automation for routine repetitive farming tasks.
- **Accessibility & Educational Users**: Software engineers, accessibility testers, and students exploring Android ADB input automation, computer vision OCR, and reverse-engineering research.
- **Technical Comfort**: Low to Moderate. Designed so that even a 7-year-old child can double-click `run.bat` or run a single command without needing complex configurations.

## 3. Product Vision
The unified, autonomous, 1-click Hay Day farm automation control center and self-healing engine. Powered by 3 free, zero-API-key AI engines to provide effortless farming, roadside shop monetization, and anti-crash resilience.

## 4. Core Features
- **Auto-Wheat Loop (`must-have`)**: Continuous 120s wheat harvest and replanting cycle across all farm plots.
- **Roadside Shop Auto-Seller (`must-have`)**: Auto-claims sold coins and lists 10 crates of 10x wheat at 1 coin with newspaper ads to prevent Silo bottlenecks.
- **3 Free Zero-API-Key AI Engines (`must-have`)**:
  1. *Vision & OCR Heuristic Engine*: Screen state, crop maturity, and popup dismissal.
  2. *Self-Healing Process & ADB Engine*: Port auto-scanning (5555, 5554, 62001, 7555, 21503), ADB daemon cycling, and auto-reconnect.
  3. *Autonomous Diagnostic & Auto-Fixing AI Engine*: Scans runtime logs and auto-patches configuration anomalies.
- **Dual Execution Modes (`must-have`)**: Live Android Emulator Bot (LDPlayer/BlueStacks) and Instant Terminal Simulation Mode (`start_bot.py --test`).
- **Interactive Web Control Center (`should-have`)**: Real-time browser dashboard (`http://localhost:3000`) with live logs, status badges, and 1-click controls.
- **Pre-Flight Privacy Guard (`must-have`)**: Zero hardcoded secrets, private keys, or credentials.
- **Authentic Release Manager (`should-have`)**: Multi-version tagged releases with humanly-written changelogs and standalone download assets.

## 5. App Flow Summary
1. User launches `run.bat` or runs `python start_bot.py`.
2. Self-healing pre-check detects ADB, opens ports, and checks emulator status.
3. User selects action: [1] Live Bot, [2] Terminal Simulation Mode, [3] Auto-Fix Setup, [4] Web UI, [5] Releases, [6] Exit.
4. Bot executes autonomous farm loops with randomized humanized touch jitter (±4s) and watchdog recovery.

## 6. Success Metrics
- **Zero-Crash Rate**: 100% resilience against closed buffer I/O and ADB socket timeouts.
- **Setup Speed**: Under 10 seconds for initial dependency verification.
- **Farming Efficiency**: Continuous wheat harvesting cycle every 120 seconds.
- **Test Coverage**: 8/8 automated test suites passing with 0 failures.

## 7. Out of Scope (V1)
- Paid commercial cloud bot hosting.
- Server-side game packet injection or DRM circumvention (strictly client-side ADB input only).
