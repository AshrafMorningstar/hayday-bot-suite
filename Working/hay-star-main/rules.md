# Project Rules & AI Guardrails — Hay Star

## Architectural Invariants
1. **Never Modify Compiled Binaries Directly:** `hay-star.exe` is a pre-compiled native Rust control engine. All interactions must proceed via TCP socket commands on port 31350.
2. **Never Break Legacy Commands:** Existing long-form commands (e.g. `nharvest`, `nplant`, `rss_claim_all`, `production_collect_all`) must continue to work without changes. Shortcuts (`hv`, `pl`, `cc`, `cm`) are additive only.
3. **Graceful Degradation:** Any component communicating over TCP or ADB must safely detect offline conditions and fallback to non-blocking simulation or diagnostic warnings instead of crashing.
4. **Encoding Integrity on Windows:** All Python modules must configure `sys.stdout.reconfigure(encoding="utf-8", errors="replace")` rather than re-wrapping `io.TextIOWrapper` to prevent closed file buffer errors.
5. **Anti-Ban Safety:** Never expose static maximum price listings on high-frequency loops. Always use randomized humanized pricing (`calculate_shop_price(..., mode='antibank')`).
6. **Strict Logging Protocol:** Maintain the 4 core project logs in `project-logs/` (`work.md`, `decision.md`, `progress.md`, `extras.md`) after every operational session.
