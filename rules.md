# Project Rules & AI Guardrails — Hay Day Bot Suite

## 1. Architectural Invariants
1. **Zero Hardcoded Credentials**: Never store private passwords, API keys, or personal tokens in code or configs.
2. **Local Loopback Boundary**: All communication is restricted to `127.0.0.1`. No arbitrary remote ports are opened.
3. **Encoding Integrity on Windows**: Always configure `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` instead of wrapping with `io.TextIOWrapper` to prevent closed buffer errors on Windows.
4. **Resilient Port Probes**: Always perform non-blocking socket checks with short timeouts (0.3s) before calling `adb connect` to prevent process hangs.
5. **Deterministic Tools Layer**: Bundled ADB (`tools/adb.exe`) ensures the bot functions out of the box regardless of system PATH.

## 2. Child-Friendly Simplicity
- CLI commands must be straightforward: numbered options [1] to [6].
- Double-clicking `run.bat` or `install.bat` must never fail silently or close unexpectedly without a helpful message.
- Provide Terminal Simulation Mode so users can see the bot work immediately without needing an open emulator.

## 3. Legal & Safe Harbor Compliance
- Strictly client-side ADB input automation. Zero game binary patching of DRM or anti-cheat bypasses.
- MIT License with DMCA Safe Harbor (§ 1201) and Fair Use (§ 107) provisions.
