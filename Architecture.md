# 02 Technical Architecture Document — Hay Day Bot Suite

## 1. Technology Stack
- **Frontend / Dashboard**: HTML5, Vanilla CSS (Ultra-Premium Dark Theme), JavaScript ES6+ (Zero external styling dependencies).
- **Backend / Web API**: Node.js 18+, Express.js 4.21.2, CORS, child_process native IPC.
- **Bot Automation Engine**: Python 3.9+ (tested up to 3.14 on Windows), OpenCV-Python (`cv2`), Pillow (`PIL`), Psutil, PyYAML, Requests.
- **Device Bridge & Control**: Android Debug Bridge (ADB version 1.0.41) over TCP loopback (ports 5555, 5554, 62001, 7555, 21503).
- **AI Engines (Zero API Keys)**:
  - *Layer 1 (Vision)*: Pixel heuristics & OpenCV template matcher.
  - *Layer 2 (Self-Healing)*: Python socket & subprocess watchdog manager.
  - *Layer 3 (NLP Diagnostics)*: Offline log classifier & config auto-repairer.

## 2. File & Directory Structure
```
m:\Hay Day Bot's\
├── bin\
│   └── cli.js                     # Unified Node CLI entrypoint (`hayday`)
├── src\
│   ├── ai\                        # AI Services & Offline Prompt Templates
│   ├── core\                      # Core scanning, organizing, privacy guard
│   ├── platforms\                 # Forge managers (GitHub, GitLab, Codeberg)
│   ├── server\                    # Express REST API server & bot routes
│   └── viral\                     # Showcase & portfolio generators
├── public\                        # Ultra-Premium Web Dashboard (HTML/CSS/JS)
├── tools\                         # Bundled standalone ADB binary & DLLs
├── Working\
│   ├── hay-star-main\             # Core HayStar 13-subsystem automation engine
│   └── inxernal-main\             # Inxernal Frida hooks & asset editor
├── project-logs\                  # Mandatory Project Logs (work, decision, progress, extras)
├── installer.py                   # Master 1-Click Automatic Setup & AI Healer
├── start_bot.py                   # Master 1-Click Bot Launcher & Terminal Simulator
├── create_releases.js             # Authentic GitHub Multi-Version Release Creator
├── run.bat / install.bat          # 1-Click Double-Click Windows batch launchers
├── RELEASES.md                    # Complete milestone chronicle (v1.0 - v8.0)
├── README.md / LICENSE            # Project overview & Legal Protection System
└── PRD.md / Architecture.md ...   # 9 Core Master Project Documents
```

## 3. A.N.T. 3-Layer Build Architecture
- **Layer 1: Architecture (`architecture/` & SOPs)**:
  - Technical operational standards for emulator connection, mod staging, and watchdog recovery.
- **Layer 2: Navigation & Process Routing**:
  - `start_bot.py` and `bin/cli.js` route commands between live emulator mode, terminal simulation mode, web UI, and auto-setup.
- **Layer 3: Tools & Deterministic Execution**:
  - `tools/adb.exe` provides isolated, deterministic ADB input dispatching without relying on external system environment states.

## 4. Environment & Security Boundaries
- Zero hardcoded passwords, tokens, or API keys.
- Strictly localhost TCP loopback communication (ports 3000 for Web UI, 31350 for HayStar engine).
