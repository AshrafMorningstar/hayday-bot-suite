"""
INXERNAL UI Server
Provides a high-performance HTTP & WebSocket/SSE backend for the bot UI,
bridging the frontend directly to loader.py's TCP control server (127.0.0.1:31350)
and ADB on emulator-5554.
"""

import json
import os
import re
import shlex
import socket
import subprocess
import sys
import tarfile
import tempfile
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from asset_editor import AssetEditor

PROJECT_DIR = Path(__file__).resolve().parent
UI_DIR = PROJECT_DIR / "ui"
GLOBAL_IDS_FILE = PROJECT_DIR / "game_global_ids.json"
CONTROL_HOST = "127.0.0.1"
CONTROL_PORT = 31350
UI_PORT = 31360

# Load Global IDs database
GLOBAL_IDS = {}
if GLOBAL_IDS_FILE.is_file():
    try:
        GLOBAL_IDS = json.loads(GLOBAL_IDS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[!] Could not load global IDs: {e}")

# In-memory log buffer for UI streaming
LOG_LINES = []
LOG_LOCK = threading.Lock()


def add_log(text, level="info"):
    with LOG_LOCK:
        timestamp = time.strftime("%H:%M:%S") + f".{int((time.time() % 1) * 1000):03d}"
        entry = {"time": timestamp, "text": text, "level": level}
        LOG_LINES.append(entry)
        if len(LOG_LINES) > 2000:
            LOG_LINES.pop(0)


def send_control_command(cmd_str, timeout=5.0):
    """Send a line command to loader.py's TCP control server and return the reply."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((CONTROL_HOST, CONTROL_PORT))
        s.sendall((cmd_str.strip() + "\n").encode("utf-8"))
        reply = s.recv(4096).decode("utf-8", "replace").strip()
        s.close()
        return reply
    except ConnectionRefusedError:
        return "ERR loader control server not running (start loader first)"
    except socket.timeout:
        return "ERR loader control server timed out"
    except Exception as e:
        return f"ERR socket error: {e}"


def get_connected_emulators():
    """Discover running Android emulators / devices via ADB."""
    devices = []
    adb_paths = [
        r"C:\LDPlayer\LDPlayer9\adb.exe",
        r"C:\Program Files\Nox\bin\nox_adb.exe",
        "adb",
    ]
    adb_bin = "adb"
    for p in adb_paths:
        if os.path.isfile(p):
            adb_bin = p
            break
    try:
        res = subprocess.run([adb_bin, "devices"], capture_output=True, text=True, timeout=3)
        for line in res.stdout.splitlines():
            line = line.strip()
            if line and not line.startswith("List of") and "\tdevice" in line:
                dev_id = line.split("\t")[0].strip()
                devices.append({"id": dev_id, "state": "online", "name": dev_id})
    except Exception as e:
        devices.append({"id": "emulator-5554", "state": "unknown", "name": "emulator-5554"})
    if not devices:
        devices.append({"id": "emulator-5554", "state": "offline", "name": "emulator-5554"})
    return devices


GAME_ASSETS_DIR = PROJECT_DIR / "com.supercell.hayday"
APP_DATA_DIR = "/data/user/0/com.supercell.hayday"
APP_UPDATE_DIR = f"{APP_DATA_DIR}/update"


def get_adb_bin():
    adb_paths = [
        r"C:\LDPlayer\LDPlayer9\adb.exe",
        r"C:\Program Files\Nox\bin\nox_adb.exe",
        "adb",
    ]
    for p in adb_paths:
        if os.path.isfile(p):
            return p
    return "adb"


def get_asset_profiles():
    profiles = []
    if not GAME_ASSETS_DIR.is_dir():
        return profiles
    for child in sorted(GAME_ASSETS_DIR.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        target = None
        if child.name == "update":
            target = child
            name = "Default (update)"
        elif (child / "update").is_dir():
            target = child / "update"
            name = child.name
        elif (child / "data").is_dir() or (child / "fingerprint.json").is_file():
            target = child
            name = child.name
        if target:
            file_count = sum(len(files) for _, _, files in os.walk(target))
            size_bytes = sum(
                sum(os.path.getsize(os.path.join(r, f)) for f in files)
                for r, _, files in os.walk(target)
            )
            profiles.append({
                "name": name,
                "path": str(target),
                "file_count": file_count,
                "size_mb": round(size_bytes / (1024 * 1024), 2),
            })
    return profiles


def get_app_uid(adb_bin, device="emulator-5554"):
    try:
        r = subprocess.run(
            [adb_bin, "-s", device, "shell", f"stat -c %u:%g {APP_DATA_DIR}"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        out = r.stdout.strip()
        if re.match(r"^\d+:\d+$", out):
            return out
    except Exception:
        pass
    return "10061:10061"


def upload_assets_direct(profile_path, adb_bin=None, device="emulator-5554"):
    adb = adb_bin or get_adb_bin()
    profile_p = Path(profile_path).resolve()
    if not profile_p.is_dir():
        return False, f"Directory not found: {profile_p}"
    tar_tmp = None
    try:
        subprocess.run(
            [adb, "-s", device, "shell", "am force-stop com.supercell.hayday"],
            capture_output=True,
            timeout=5,
        )
        time.sleep(0.3)
        items = list(profile_p.iterdir())
        with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tf:
            tar_tmp = tf.name
        with tarfile.open(tar_tmp, "w") as tar:
            for it in items:
                tar.add(str(it), arcname=it.name)

        stage_tar = "/data/local/tmp/.nxrth_update.tar"
        subprocess.run(
            [adb, "-s", device, "push", tar_tmp, stage_tar],
            capture_output=True,
            timeout=60,
        )
        uid_gid = get_app_uid(adb, device)
        extract_cmd = (
            f"mkdir -p {APP_UPDATE_DIR} && "
            f"tar -xf {stage_tar} -C {APP_UPDATE_DIR} && "
            f"rm -f {stage_tar} && "
            f"chown -R {uid_gid} {APP_UPDATE_DIR} && "
            f"chmod -R 777 {APP_UPDATE_DIR}"
        )
        subprocess.run(
            [adb, "-s", device, "shell", f"su 0 {extract_cmd}"],
            capture_output=True,
            timeout=10,
        )
        return True, f"Uploaded {profile_p.name} successfully"
    except Exception as e:
        return False, str(e)
    finally:
        if tar_tmp and os.path.exists(tar_tmp):
            try:
                os.remove(tar_tmp)
            except Exception:
                pass


def clean_assets_direct(adb_bin=None, device="emulator-5554"):
    adb = adb_bin or get_adb_bin()
    try:
        subprocess.run(
            [adb, "-s", device, "shell", "am force-stop com.supercell.hayday"],
            capture_output=True,
            timeout=5,
        )
        clean_cmd = f"rm -rf {APP_UPDATE_DIR}/* {APP_UPDATE_DIR}"
        subprocess.run(
            [adb, "-s", device, "shell", f"su 0 {clean_cmd}"],
            capture_output=True,
            timeout=5,
        )
        return True, "Cleaned custom assets (vanilla game state)"
    except Exception as e:
        return False, str(e)


def get_remote_assets_state(adb_bin=None, device="emulator-5554"):
    adb = adb_bin or get_adb_bin()
    try:
        r = subprocess.run(
            [adb, "-s", device, "shell", f"ls -1 {APP_UPDATE_DIR} 2>/dev/null"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        files = [f.strip() for f in r.stdout.splitlines() if f.strip()]
        is_modded = any(f in ("data", "localization", "sc") for f in files)
        return {
            "exists": bool(files),
            "files": files,
            "is_modded": is_modded,
            "state": "modded" if is_modded else ("clean" if files else "empty"),
        }
    except Exception:
        return {"exists": False, "files": [], "is_modded": False, "state": "unknown"}


class BotUIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/status":
            ctl_status = send_control_command("status", timeout=2.0)
            adb_status = send_control_command("adb", timeout=2.0)
            data = {
                "ok": True,
                "control_status": ctl_status,
                "adb_status": adb_status,
                "attached": "attached=yes" in ctl_status,
                "farm_running": "farm=running" in ctl_status,
                "gate_ready": "gate=ready" in ctl_status,
                "time": time.time(),
            }
            self._send_json(data)
            return

        elif path == "/api/emulators":
            devices = get_connected_emulators()
            self._send_json({"ok": True, "devices": devices})
            return

        elif path == "/api/logs":
            params = parse_qs(parsed.query)
            since_idx = int(params.get("since", ["0"])[0])
            with LOG_LOCK:
                entries = LOG_LINES[since_idx:]
                total = len(LOG_LINES)
            self._send_json({"ok": True, "entries": entries, "total": total})
            return

        elif path == "/api/entities":
            self._send_json({"ok": True, "database": GLOBAL_IDS})
            return

        elif path == "/api/lookup":
            params = parse_qs(parsed.query)
            query = params.get("q", [""])[0].strip().lower()
            results = []
            if query:
                for cat, items in GLOBAL_IDS.items():
                    if isinstance(items, list):
                        for it in items:
                            if isinstance(it, dict):
                                name = it.get("name", "")
                                if query in name.lower() or query == str(it.get("global_id", "")):
                                    results.append({
                                        "category": cat,
                                        "name": name,
                                        "global_id": it.get("global_id", it.get("id")),
                                        "data": it,
                                    })
            self._send_json({"ok": True, "query": query, "results": results})
            return

        elif path == "/api/assets":
            ctl_status = send_control_command("assets_status", timeout=2.0)
            remote = get_remote_assets_state(device="emulator-5554")
            self._send_json({
                "ok": True,
                "profiles": get_asset_profiles(),
                "remote": remote,
                "ctl_status": ctl_status,
            })
            return

        super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            req = json.loads(body)
        except Exception:
            req = {}

        if path == "/api/command":
            cmd = req.get("command", "").strip()
            if not cmd:
                self._send_json({"ok": False, "error": "Empty command"})
                return

            add_log(f"> {cmd}", level="cmd")
            res = send_control_command(cmd, timeout=8.0)
            level = "success" if res.startswith("OK") else "error"
            add_log(res, level=level)
            self._send_json({"ok": res.startswith("OK"), "reply": res})
            return

        elif path == "/api/assets/upload":
            pname = req.get("profile", "")
            device = req.get("device", "emulator-5554")
            profiles = get_asset_profiles()
            target_profile = None
            if pname:
                for p in profiles:
                    if pname.lower() in p["name"].lower():
                        target_profile = p
                        break
            if not target_profile and profiles:
                target_profile = profiles[0]
            if not target_profile:
                self._send_json({"ok": False, "error": "No asset profile found"})
                return

            add_log(
                f"Uploading assets from '{target_profile['name']}' "
                f"({target_profile['file_count']} files, {target_profile['size_mb']} MB)..."
            )
            res = send_control_command(f"assets_upload {target_profile['name']}", timeout=30.0)
            if res.startswith("OK"):
                add_log(res, level="success")
                self._send_json({"ok": True, "reply": res})
            else:
                ok, msg = upload_assets_direct(target_profile["path"], device=device)
                add_log(msg, level="success" if ok else "error")
                self._send_json({"ok": ok, "reply": msg})
            return

        elif path == "/api/assets/clean":
            device = req.get("device", "emulator-5554")
            add_log("Cleaning custom modded assets (preparing clean vanilla state)...")
            res = send_control_command("assets_clean", timeout=10.0)
            if res.startswith("OK"):
                add_log(res, level="success")
                self._send_json({"ok": True, "reply": res})
            else:
                ok, msg = clean_assets_direct(device=device)
                add_log(msg, level="success" if ok else "error")
                self._send_json({"ok": ok, "reply": msg})
            return

        elif path == "/api/assets/restart_game":
            device = req.get("device", "emulator-5554")
            add_log(f"Restarting Hay Day on {device} to test live assets...")
            editor = AssetEditor(device=device)
            ok, msg = editor.test_restart_game()
            add_log(msg, level="success" if ok else "error")
            self._send_json({"ok": ok, "reply": msg})
            return

        elif path == "/api/assets/editor/search":
            q = req.get("query", "")
            editor = AssetEditor()
            results = editor.search_items(q)
            self._send_json({"ok": True, "results": results[:50]})
            return

        elif path == "/api/assets/editor/update":
            table = req.get("table", "")
            item = req.get("item", "")
            param = req.get("param", "Value")
            val = req.get("value", "")
            deploy = req.get("deploy", True)
            device = req.get("device", "emulator-5554")
            editor = AssetEditor(device=device)
            ok, msg = editor.set_item_param(table, item, param, val)
            add_log(msg, level="success" if ok else "error")
            if ok and deploy:
                ok_dep, msg_dep = editor.deploy_to_ldplayer()
                add_log(msg_dep, level="success" if ok_dep else "info")
            self._send_json({"ok": ok, "reply": msg})
            return

        elif path == "/api/assets/editor/batch":
            pattern = req.get("pattern", "fields.csv")
            param = req.get("param", "Value")
            mode = req.get("mode", "multiply")
            mult = float(req.get("multiplier", 5.0))
            exact = req.get("exact", "")
            deploy = req.get("deploy", True)
            device = req.get("device", "emulator-5554")
            editor = AssetEditor(device=device)
            cnt = editor.batch_modify(pattern, param, mode=mode, multiplier=mult, exact_val=exact)
            msg = f"Batch updated {cnt} items ({pattern}: {param})"
            add_log(msg, level="success")
            if cnt > 0 and deploy:
                ok_dep, msg_dep = editor.deploy_to_ldplayer()
                add_log(msg_dep, level="success" if ok_dep else "info")
            self._send_json({"ok": True, "modified_count": cnt, "reply": msg})
            return

        elif path == "/api/adb_action":
            # Touch or navigation action
            action = req.get("action", "")
            adb_bin = r"C:\LDPlayer\LDPlayer9\adb.exe"
            device = req.get("device", "emulator-5554")
            args = []
            if action == "tap":
                x, y = req.get("x", 0), req.get("y", 0)
                args = ["shell", f"input tap {x} {y}"]
                add_log(f"ADB tap at ({x}, {y})")
            elif action == "swipe":
                x1, y1 = req.get("x1", 0), req.get("y1", 0)
                x2, y2 = req.get("x2", 0), req.get("y2", 0)
                ms = req.get("duration", 300)
                args = ["shell", f"input swipe {x1} {y1} {x2} {y2} {ms}"]
                add_log(f"ADB swipe ({x1},{y1}) -> ({x2},{y2})")
            elif action == "back":
                args = ["shell", "input keyevent 4"]
                add_log("ADB BACK pressed")
            elif action == "launch_game":
                mode = req.get("mode", "direct")
                if mode == "upload":
                    pname = req.get("profile", "")
                    profiles = get_asset_profiles()
                    target = profiles[0]["path"] if profiles else None
                    if pname:
                        for p in profiles:
                            if pname.lower() in p["name"].lower():
                                target = p["path"]
                                break
                    if target:
                        add_log(f"Pre-launch: uploading custom assets from {Path(target).name}...")
                        upload_assets_direct(target, adb_bin=adb_bin, device=device)
                elif mode == "clean":
                    add_log("Pre-launch: removing custom assets (clean vanilla launch)...")
                    clean_assets_direct(adb_bin=adb_bin, device=device)
                args = ["shell", "monkey -p com.supercell.hayday -c android.intent.category.LAUNCHER 1"]
                add_log(f"ADB Launch Hay Day (mode: {mode})")
            elif action == "stop_game":
                args = ["shell", "am force-stop com.supercell.hayday"]
                add_log("ADB Stop Hay Day")
            elif action == "clear_data":
                args = ["shell", "pm clear com.supercell.hayday"]
                add_log("ADB Clear Hay Day Data")

            if args:
                try:
                    subprocess.run([adb_bin, "-s", device] + args, capture_output=True, timeout=5)
                    self._send_json({"ok": True, "action": action})
                except Exception as e:
                    self._send_json({"ok": False, "error": str(e)})
            else:
                self._send_json({"ok": False, "error": f"Unknown action {action}"})
            return

        self.send_error(404, "Endpoint not found")

    def _send_json(self, data, code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server():
    server = ThreadingHTTPServer(("127.0.0.1", UI_PORT), BotUIHandler)
    add_log(f"UI Server initialized at http://127.0.0.1:{UI_PORT}")
    print(f"[*] INXERNAL UI Server listening on http://127.0.0.1:{UI_PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    if "--test" in sys.argv:
        print("[*] Testing UI server components...")
        print(f"  -> Global IDs loaded: {len(GLOBAL_IDS)} categories")
        print(f"  -> UI Dir: {UI_DIR} (exists: {UI_DIR.is_dir()})")
        devs = get_connected_emulators()
        print(f"  -> Discovered devices: {devs}")
        sys.exit(0)

    run_server()
