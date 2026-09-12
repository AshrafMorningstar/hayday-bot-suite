"""
continuous_monitor.py — Hay★Star Continuous Auto-Test & Watchdog
=================================================================
Runs forever until Ctrl+C. Every cycle (default 5 min) it:

1.  Runs the full 23-test suite
2.  Checks emulator is alive (auto-relaunches if crashed)
3.  Checks supervisor process is alive (auto-restarts if crashed)
4.  Logs every result to logs/monitor_YYYYMMDD.log
5.  Prints a live status dashboard to the console

Usage:
    python continuous_monitor.py           # default 5-min cycles
    python continuous_monitor.py --fast    # 60-second cycles (debug)
    python continuous_monitor.py --once    # single pass, then exit
"""

import sys
import os
import subprocess
import time
import signal
import argparse
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ── Configuration ────────────────────────────────────────────────────────────
ROOT          = Path(__file__).resolve().parent
LOG_DIR       = ROOT / "logs"
CYCLE_SECONDS = 300          # 5 minutes default
FAST_SECONDS  = 60           # --fast flag

LDCONSOLE     = Path(r"C:\LDPlayer\LDPlayer9\ldconsole.exe")
BOT_INSTANCE  = "HayStarBot"

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ── Globals ───────────────────────────────────────────────────────────────────
_supervisor_proc = None
_cycle           = 0
_total_tests     = 0
_total_failures  = 0
_start_time      = datetime.now()

# ── Helpers ───────────────────────────────────────────────────────────────────

def log_path() -> Path:
    return LOG_DIR / f"monitor_{datetime.now():%Y%m%d}.log"


def stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def write_log(line: str):
    with open(log_path(), "a", encoding="utf-8") as f:
        f.write(f"[{stamp()}] {line}\n")


def banner(msg: str, char: str = "=", width: int = 66):
    print(f"\n  {char * width}")
    print(f"  {msg}")
    print(f"  {char * width}")


def elapsed() -> str:
    delta = datetime.now() - _start_time
    h, r  = divmod(int(delta.total_seconds()), 3600)
    m, s  = divmod(r, 60)
    return f"{h:02d}h {m:02d}m {s:02d}s"


# ── Test Runner ───────────────────────────────────────────────────────────────

def run_tests() -> tuple[int, int]:
    """Run full test suite. Returns (passed, failed)."""
    try:
        result = subprocess.run(
            [sys.executable, "tests/test_all.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        output = result.stdout + result.stderr
        passed = output.count(" ok")
        failed = output.count(" FAIL") + output.count(" ERROR")
        # Parse "Ran N tests"
        for line in output.splitlines():
            if line.startswith("Ran "):
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        total = int(parts[1])
                        if failed == 0:
                            passed = total
                    except ValueError:
                        pass
        return passed, failed
    except subprocess.TimeoutExpired:
        write_log("[TEST] TIMEOUT — test suite took >120 s")
        return 0, 1
    except Exception as exc:
        write_log(f"[TEST] ERROR — {exc}")
        return 0, 1


# ── Emulator Monitor ──────────────────────────────────────────────────────────

def check_emulator() -> bool:
    """Check if HayStarBot is running; auto-launch if stopped."""
    if not LDCONSOLE.exists():
        return True  # can't check — skip

    try:
        r = subprocess.run(
            [str(LDCONSOLE), "isrunning", "--name", BOT_INSTANCE],
            capture_output=True, text=True, timeout=10,
        )
        if r.stdout.strip() == "running":
            return True

        # Not running — try to relaunch
        write_log(f"[EMU] '{BOT_INSTANCE}' not running. Relaunching...")
        subprocess.run(
            [str(LDCONSOLE), "launch", "--name", BOT_INSTANCE],
            capture_output=True, timeout=10,
        )
        time.sleep(5)

        # Check again
        r2 = subprocess.run(
            [str(LDCONSOLE), "isrunning", "--name", BOT_INSTANCE],
            capture_output=True, text=True, timeout=10,
        )
        ok = r2.stdout.strip() == "running"
        write_log(f"[EMU] Relaunch {'succeeded' if ok else 'FAILED'}.")
        return ok
    except Exception as exc:
        write_log(f"[EMU] Check error: {exc}")
        return False


# ── Supervisor Process Monitor ────────────────────────────────────────────────

def ensure_supervisor():
    """Keep the supervisor process alive."""
    global _supervisor_proc
    if _supervisor_proc is not None:
        ret = _supervisor_proc.poll()
        if ret is None:
            return  # still running
        write_log(f"[SUP] Supervisor exited with code {ret}. Restarting...")

    try:
        log_file = open(ROOT / "logs" / "supervisor_live.log", "a",
                        encoding="utf-8", errors="replace")
        _supervisor_proc = subprocess.Popen(
            [sys.executable, str(ROOT / "supervisor.py")],
            cwd=str(ROOT),
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )
        write_log(f"[SUP] Supervisor started (PID {_supervisor_proc.pid}).")
    except Exception as exc:
        write_log(f"[SUP] Could not start supervisor: {exc}")


# ── ADB Live Check ────────────────────────────────────────────────────────────

def check_adb() -> str:
    """Return ADB device status string."""
    adb_paths = [
        r"C:\LDPlayer\LDPlayer9\adb.exe",
        "adb",
    ]
    for adb in adb_paths:
        try:
            r = subprocess.run(
                [adb, "devices"],
                capture_output=True, text=True, timeout=8,
            )
            lines = [l for l in r.stdout.splitlines() if "\t" in l]
            if lines:
                devs = [l.split("\t")[0] for l in lines]
                return f"Online: {', '.join(devs)}"
            return "No devices"
        except Exception:
            continue
    return "ADB not found"


# ── Status Dashboard ──────────────────────────────────────────────────────────

def print_dashboard(test_passed: int, test_failed: int, emu_ok: bool, adb_status: str):
    global _cycle
    banner(f"HAY STAR CONTINUOUS MONITOR — Cycle #{_cycle}  |  Up: {elapsed()}")
    print(f"  Time:          {stamp()}")
    print(f"  Tests Run:     {_total_tests} total  |  Passed: {_total_tests - _total_failures}  |  Failed: {_total_failures}")
    print(f"  This Cycle:    {test_passed} passed, {test_failed} failed  ({'OK' if test_failed == 0 else 'FAILURES DETECTED'})")
    print(f"  Emulator:      {'Running' if emu_ok else 'DOWN (relaunch attempted)'}")
    print(f"  ADB:           {adb_status}")
    sup_status = "Running" if (_supervisor_proc and _supervisor_proc.poll() is None) else "Stopped"
    print(f"  Supervisor:    {sup_status}")
    print(f"  Log file:      {log_path()}")
    print(f"  Press Ctrl+C to stop the monitor at any time.")
    print()


# ── Graceful Shutdown ─────────────────────────────────────────────────────────

def shutdown(signum=None, frame=None):
    print("\n\n  Stopping monitor gracefully...")
    write_log(f"[MONITOR] Stopped by user after {elapsed()} and {_cycle} cycles.")
    if _supervisor_proc and _supervisor_proc.poll() is None:
        _supervisor_proc.terminate()
        write_log("[SUP] Supervisor terminated.")
    banner(f"MONITOR STOPPED  |  Total cycles: {_cycle}  |  Total tests run: {_total_tests}  |  Failures: {_total_failures}", char="-")
    sys.exit(0)

signal.signal(signal.SIGINT,  shutdown)
signal.signal(signal.SIGTERM, shutdown)


# ── Main Loop ─────────────────────────────────────────────────────────────────

def main():
    global _cycle, _total_tests, _total_failures

    parser = argparse.ArgumentParser(description="Hay-Star Continuous Monitor")
    parser.add_argument("--fast", action="store_true", help="60-second cycles")
    parser.add_argument("--once", action="store_true", help="Single pass then exit")
    parser.add_argument("--no-supervisor", action="store_true", help="Don't manage supervisor process")
    args = parser.parse_args()

    cycle_secs = FAST_SECONDS if args.fast else CYCLE_SECONDS

    write_log("=" * 60)
    write_log(f"[MONITOR] Hay-Star Continuous Monitor started.")
    write_log(f"[MONITOR] Cycle interval: {cycle_secs}s | Fast: {args.fast} | Once: {args.once}")
    write_log("=" * 60)

    banner("HAY STAR CONTINUOUS AUTO-TEST & WATCHDOG STARTED")
    print(f"  Cycle interval: {cycle_secs}s")
    print(f"  Log: {log_path()}")
    print(f"  Press Ctrl+C to stop.\n")

    while True:
        _cycle += 1
        write_log(f"[CYCLE {_cycle}] Starting...")

        # 1 — Run tests
        print(f"  [{stamp()}] Running test suite (cycle #{_cycle})...")
        passed, failed = run_tests()
        _total_tests    += passed + failed
        _total_failures += failed
        write_log(f"[CYCLE {_cycle}] Tests: {passed} passed, {failed} failed.")

        if failed > 0:
            write_log(f"[CYCLE {_cycle}] *** FAILURES DETECTED — check logs ***")

        # 2 — Check emulator
        emu_ok = check_emulator()
        write_log(f"[CYCLE {_cycle}] Emulator '{BOT_INSTANCE}': {'running' if emu_ok else 'NOT running'}.")

        # 3 — Keep supervisor alive
        if not args.no_supervisor:
            ensure_supervisor()

        # 4 — ADB status
        adb_status = check_adb()
        write_log(f"[CYCLE {_cycle}] ADB: {adb_status}")

        # 5 — Print dashboard
        print_dashboard(passed, failed, emu_ok, adb_status)
        write_log(f"[CYCLE {_cycle}] Complete.")

        if args.once:
            shutdown()
            return

        # Wait for next cycle
        print(f"  Next check in {cycle_secs}s...  (Ctrl+C to stop)\n")
        time.sleep(cycle_secs)


if __name__ == "__main__":
    main()
