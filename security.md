# 03 Security, Privacy & Access Document — Hay Day Bot Suite

## 1. Authentication & Access Method
- **Local Loopback Only**: The bot suite operates exclusively on `127.0.0.1` (localhost). No external ports or public network listeners are opened.
- **Zero API Keys & Zero Telemetry**: None of the 3 AI engines require third-party API keys, OpenAI tokens, or external authentication headers.
- **Credential Storage**: If git tokens are used for multi-forge sync, they are stored locally in user configuration (`~/.repoforge/config.json`) and never committed.

## 2. Privacy Guard & Secret Detection
- Repository audited with `test/scan_privacy.py`.
- Verified regex patterns scan for:
  - AWS, GitHub, GitLab, and private access tokens.
  - Hardcoded user passwords or database connection strings.
  - Private RSA keys (`BEGIN PRIVATE KEY`).
- **Result**: 0 secrets, 0 leaks across all code files.

## 3. Anti-Detection & Account Safety Architecture
- **Samsung Galaxy S24 Device Spoofing**: Simulates genuine mobile hardware properties.
- **Quago Telemetry Blocking**: Prevents game telemetry analytics reporting.
- **Humanized Touch Variance**: Injects randomized Gaussian micro-delays (±4s) into tap sequences to avoid synthetic frequency detection.

## 4. Error Handling & Edge Cases
- **ADB Disconnects**: Self-healing watchdog catches socket timeouts and initiates automatic loopback reconnection.
- **Closed File Buffers**: `sys.stdout.reconfigure()` permanently prevents Windows `ValueError: I/O operation on closed file`.
- **Offline Emulator**: If no emulator is open, the system alerts the user cleanly and offers Terminal Simulation Mode rather than crashing.
