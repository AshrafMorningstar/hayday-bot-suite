/* ==========================================================================
   INXERNAL / HDX UI - Frontend Application Logic
   ========================================================================== */

let currentDevice = "emulator-5554";
let entityDatabase = {};
let logIndex = 0;
let autoFarmActive = false;

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initSubTabs();
  fetchEntities();
  startStatusPolling();
  startLogPolling();
  refreshAssetStatus();

  document.getElementById("btnStartEngine").addEventListener("click", startEngine);
  document.getElementById("btnStopEngine").addEventListener("click", stopEngine);
  document.getElementById("deviceSelect").addEventListener("change", (e) => {
    currentDevice = e.target.value;
    log(`Selected device ${currentDevice}`);
  });

  // Setup auto-complete search for crop and market inputs
  setupSearchAutocomplete("farmCropSearch");
  setupSearchAutocomplete("marketItemSearch");
});

// ---------------------------------------------------------------- Main Tabs ----
function initTabs() {
  const tabs = document.querySelectorAll(".main-tab-btn");
  tabs.forEach(btn => {
    btn.addEventListener("click", () => {
      tabs.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach(p => p.classList.remove("active"));
      const activePanel = document.getElementById(`tab-${target}`);
      if (activePanel) activePanel.classList.add("active");
    });
  });
}

// -------------------------------------------------------------- Sub Tabs -------
function initSubTabs() {
  const subtabs = document.querySelectorAll(".subtab-btn");
  subtabs.forEach(btn => {
    btn.addEventListener("click", () => {
      subtabs.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      const target = btn.getAttribute("data-subtab");
      document.querySelectorAll(".manual-panel").forEach(p => p.classList.remove("active"));
      const activeSubPanel = document.getElementById(`panel-${target}`);
      if (activeSubPanel) activeSubPanel.classList.add("active");
    });
  });
}

// ------------------------------------------------------------- Farm Config -----
function switchConfigPanel(cat) {
  document.querySelectorAll(".config-cat-item").forEach(i => i.classList.remove("active"));
  event.currentTarget.classList.add("active");
  log(`Selected config inspector category: ${cat}`);
}

// -------------------------------------------------------------- API & Engine ---
async function sendCommand(cmd) {
  try {
    const res = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ command: cmd })
    });
    const data = await res.json();
    return data.reply || "";
  } catch (e) {
    log(`Command error: ${e}`, "error");
    return `ERR ${e}`;
  }
}

async function sendAdbAction(action, extra = {}) {
  try {
    const res = await fetch("/api/adb_action", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action, device: currentDevice, ...extra })
    });
    return await res.json();
  } catch (e) {
    log(`ADB action error: ${e}`, "error");
  }
}

async function startEngine() {
  log("Starting engine on " + currentDevice + "...");
  const reply = await sendCommand("loadnative");
  log(reply, reply.startsWith("OK") ? "success" : "error");
}

async function stopEngine() {
  log("Stopping engine on " + currentDevice + "...");
  const reply = await sendCommand("farm stop");
  log("Engine stopped: " + reply, "info");
}

// ----------------------------------------------------- Game & Asset Control ----
async function launchGame() {
  const modeSelect = document.getElementById("launchModeSelect");
  const mode = modeSelect ? modeSelect.value : "upload";
  log(`Launching Hay Day (Mode: ${mode})...`);
  const res = await sendAdbAction("launch_game", { mode });
  if (res && res.ok) {
    log(`Hay Day launch command dispatched (mode: ${mode})`, "success");
    setTimeout(refreshAssetStatus, 2500);
  } else {
    log(`Failed to launch Hay Day: ${res ? res.error : "Unknown error"}`, "error");
  }
}

async function stopGame() {
  log("Stopping Hay Day app...");
  const res = await sendAdbAction("stop_game");
  if (res && res.ok) {
    log("Hay Day stopped successfully", "info");
  }
}

async function clearGameData() {
  if (!confirm("Are you sure you want to clear all app data for Hay Day?")) return;
  log("Clearing Hay Day app data via ADB...");
  const res = await sendAdbAction("clear_data");
  if (res && res.ok) {
    log("Hay Day app data cleared", "success");
  }
}

async function uploadModdedAssets() {
  log("Starting full auto upload of modded assets from com.supercell.hayday...");
  try {
    const res = await fetch("/api/assets/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device: currentDevice })
    });
    const data = await res.json();
    if (data.ok) {
      log("Assets uploaded successfully: " + (data.reply || "Done"), "success");
      updateAssetBadge("Assets: Modded (Loaded)", true);
    } else {
      log("Asset upload failed: " + (data.error || data.reply), "error");
    }
  } catch (e) {
    log(`Error uploading assets: ${e}`, "error");
  }
}

async function cleanGameAssets() {
  log("Cleaning modded assets (preparing clean vanilla launch)...");
  try {
    const res = await fetch("/api/assets/clean", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device: currentDevice })
    });
    const data = await res.json();
    if (data.ok) {
      log("Clean launch state ready: " + (data.reply || "Done"), "success");
      updateAssetBadge("Assets: Clean (Vanilla)", false);
    } else {
      log("Clean failed: " + (data.error || data.reply), "error");
    }
  } catch (e) {
    log(`Error cleaning assets: ${e}`, "error");
  }
}

async function refreshAssetStatus() {
  try {
    const res = await fetch("/api/assets");
    const data = await res.json();
    if (data.ok && data.remote) {
      const isModded = data.remote.is_modded;
      const count = data.remote.files ? data.remote.files.length : 0;
      updateAssetBadge(
        isModded ? `Assets: Modded (${count} items)` : "Assets: Clean (Vanilla)",
        isModded
      );
    }
  } catch (_) {}
}

function updateAssetBadge(text, isModded) {
  const badge = document.getElementById("assetStatusBadge");
  if (!badge) return;
  badge.textContent = text;
  badge.style.color = isModded ? "var(--accent-green)" : "#ffc107";
  badge.style.background = isModded ? "rgba(76,175,80,0.15)" : "rgba(255,193,7,0.15)";
}

// ---------------------------------------------------------- Live Actions -------
async function harvestFields() {
  log("Triggering live field harvest...");
  const reply = await sendCommand("harvest");
  log(reply, reply.startsWith("OK") ? "success" : "error");
  inspectFields();
}

async function plantFields() {
  const cropInput = document.getElementById("farmCropSearch").value.trim();
  const count = document.getElementById("farmFieldsToSow").value || "68";
  log(`Planting ${cropInput} on ${count} fields...`);
  const reply = await sendCommand(`plant ${cropInput}`);
  log(reply, reply.startsWith("OK") ? "success" : "error");
  inspectFields();
}

async function inspectFields() {
  const reply = await sendCommand("fields");
  if (reply.startsWith("OK")) {
    const match = reply.match(/OK\s+(\d+)\s+\[(.*)\]/);
    if (match) {
      const ids = match[2].split(",").map(s => s.trim()).filter(Boolean);
      const tbody = document.getElementById("fieldsTableBody");
      tbody.innerHTML = "";
      ids.slice(0, 100).forEach((fid, idx) => {
        const tr = document.createElement("tr");
        tr.innerHTML = `<td>${fid}</td><td>Wheat</td><td>400001</td><td>Ready</td><td>0s</td>`;
        tbody.appendChild(tr);
      });
      log(`Discovered ${ids.length} field entities in memory`);
    }
  }
}

async function toggleAutoFarm() {
  autoFarmActive = !autoFarmActive;
  const btn = document.getElementById("btnAutoFarm");
  if (autoFarmActive) {
    btn.textContent = "Auto Farm Loop (Active)";
    btn.classList.remove("btn-neutral");
    btn.classList.add("btn-green");
    const crop = document.getElementById("farmCropSearch").value.trim() || "wheat";
    log(`Starting background farm loop (crop=${crop})...`);
    sendCommand(`farm start 120 ${crop}`);
  } else {
    btn.textContent = "Auto Farm Loop (Off)";
    btn.classList.remove("btn-green");
    btn.classList.add("btn-neutral");
    log("Stopping auto farm loop...");
    sendCommand("farm stop");
  }
}

async function sellItem() {
  const slot = document.getElementById("marketSlot").value;
  const item = document.getElementById("marketItemSearch").value.trim() || "wheat";
  const count = document.getElementById("marketCount").value || "10";
  const price = document.getElementById("marketPrice").value || "1";
  const ad = document.getElementById("marketAd").checked ? "1" : "0";

  log(`Listing item in shop: Slot ${slot}, ${item} x${count} @ ${price} coin (ad=${ad})...`);
  const reply = await sendCommand(`sell ${slot} ${count} ${price} ${ad} ${item}`);
  log(reply, reply.startsWith("OK") ? "success" : "error");
}

function openShopScreen() {
  log("Tapping shop button on screen...");
  sendAdbAction("tap", { x: 35, y: 440 });
}

// ------------------------------------------------------------- Navigation ------
function travelTo(dest) {
  log(`Traveling to: ${dest.toUpperCase()}...`);
  if (dest === "home") sendAdbAction("tap", { x: 320, y: 450 });
  else if (dest === "fishing") sendAdbAction("tap", { x: 50, y: 150 });
  else if (dest === "town") sendAdbAction("tap", { x: 600, y: 150 });
  else if (dest === "greg") log("Visiting Greg's farm...");
  else if (dest === "aitown") log("Switching to AI Town...");
}

function visitPlayer() {
  const id = document.getElementById("visitIdInput").value.trim();
  if (id) log(`Visiting player tag #${id}...`);
}

// ---------------------------------------------------------- Trees & Fishing ----
async function collectReadyTrees() {
  log("Collecting all ripe fruit from trees and bushes...");
  sendAdbAction("tap", { x: 300, y: 300 });
}

async function collectReadyNests() {
  log("Collecting ready nests (honey, peanuts)...");
  sendCommand("harvest");
}

async function chopSelectedTree() {
  log("Chop Selected: verifying device connection...");
  sendAdbAction("tap", { x: 300, y: 250 });
}

async function chopAllTrees() {
  if (confirm("Are you sure you want to chop ALL dead trees and bushes?")) {
    log("Chopping all dead trees and bushes with saws and axes...");
  }
}

async function refreshFishing() {
  log("Refreshing fishing spots and live fish state...");
}

async function catchReadyFish() {
  log("Catching ready fish from active spots...");
}

async function blastMine(tool) {
  log(`Blasting mine using ${tool}...`);
}

async function collectOre() {
  log("Collecting extracted ores in adaptive growing batches...");
}

// ------------------------------------------------------ Universal Search -------
async function fetchEntities() {
  try {
    const res = await fetch("/api/entities");
    const data = await res.json();
    if (data.ok) entityDatabase = data.database;
  } catch (_) {}
}

function setupSearchAutocomplete(inputId) {
  const input = document.getElementById(inputId);
  if (!input) return;

  input.addEventListener("input", () => {
    const q = input.value.trim().toLowerCase();
    if (!q || !entityDatabase) return;
    // Substring matching across all categories
    for (const [cat, list] of Object.entries(entityDatabase)) {
      if (Array.isArray(list)) {
        for (const it of list) {
          if (it.name && it.name.toLowerCase().includes(q)) {
            input.setAttribute("title", `Match: ${it.name} (ID: ${it.global_id || it.id})`);
            break;
          }
        }
      }
    }
  });
}

function filterInventory() {
  const q = document.getElementById("invSearchInput").value.toLowerCase();
  const rows = document.querySelectorAll("#invTableBody tr");
  rows.forEach(r => {
    const text = r.textContent.toLowerCase();
    r.style.display = text.includes(q) ? "" : "none";
  });
}

// ------------------------------------------------------------ Table Sorting ----
function sortTable(tableId, colIdx) {
  const table = document.getElementById(tableId);
  if (!table) return;
  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));
  const asc = table.getAttribute(`data-sort-${colIdx}`) !== "asc";

  rows.sort((a, b) => {
    const aText = a.children[colIdx].innerText.trim();
    const bText = b.children[colIdx].innerText.trim();
    const aNum = parseFloat(aText.replace(/[^\d.-]/g, ""));
    const bNum = parseFloat(bText.replace(/[^\d.-]/g, ""));

    if (!isNaN(aNum) && !isNaN(bNum)) {
      return asc ? aNum - bNum : bNum - aNum;
    }
    return asc ? aText.localeCompare(bText) : bText.localeCompare(aText);
  });

  table.setAttribute(`data-sort-${colIdx}`, asc ? "asc" : "desc");
  rows.forEach(r => tbody.appendChild(r));
}

// ---------------------------------------------------------- Logging System -----
function log(msg, level = "info") {
  const box = document.getElementById("logContent");
  const time = new Date().toTimeString().split(" ")[0] + "." + String(Date.now() % 1000).padStart(3, "0");
  const div = document.createElement("div");
  div.className = "log-entry";
  div.innerHTML = `<span class="log-time">${time}</span><span class="log-msg ${level}">${escapeHtml(msg)}</span>`;
  box.appendChild(div);

  if (document.getElementById("logAutoScroll").checked) {
    box.scrollTop = box.scrollHeight;
  }
}

function copyLogs() {
  const text = document.getElementById("logContent").innerText;
  navigator.clipboard.writeText(text);
  log("Copied logs to clipboard", "info");
}

function clearLogs() {
  document.getElementById("logContent").innerHTML = "";
}

function escapeHtml(text) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// -------------------------------------------------------- Status Polling -------
function startStatusPolling() {
  setInterval(async () => {
    try {
      const res = await fetch("/api/status");
      const data = await res.json();
      if (data.ok) {
        const badge = document.getElementById("licenseStatus");
        if (data.attached) {
          badge.textContent = "Engine: Live & Attached | @m0nesy619";
          badge.style.color = "var(--accent-green)";
        }
      }
    } catch (_) {}
  }, 2500);
}

function startLogPolling() {
  setInterval(async () => {
    try {
      const res = await fetch(`/api/logs?since=${logIndex}`);
      const data = await res.json();
      if (data.ok && data.entries && data.entries.length > 0) {
        data.entries.forEach(e => log(e.text, e.level));
        logIndex = data.total;
      }
    } catch (_) {}
  }, 1000);
}

// -------------------------------------------------------- Asset Management -----
async function uploadModdedAssets() {
  const badge = document.getElementById("assetStatusBadge");
  if (badge) {
    badge.textContent = "Assets: Uploading...";
    badge.style.color = "var(--accent-gold)";
  }
  log("Starting fast deployment of modded assets to " + currentDevice + "...");
  try {
    const res = await fetch("/api/assets/upload", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device: currentDevice })
    });
    const data = await res.json();
    if (data.ok) {
      log("Modded assets successfully deployed!", "success");
      if (badge) {
        badge.textContent = "Assets: Modded";
        badge.style.color = "var(--accent-green)";
      }
    } else {
      log("Asset upload failed: " + (data.reply || data.error), "error");
      if (badge) {
        badge.textContent = "Assets: Error";
        badge.style.color = "var(--accent-red)";
      }
    }
  } catch (e) {
    log("Asset upload network error: " + e, "error");
    if (badge) {
      badge.textContent = "Assets: Error";
      badge.style.color = "var(--accent-red)";
    }
  }
}

async function cleanGameAssets() {
  const badge = document.getElementById("assetStatusBadge");
  if (badge) {
    badge.textContent = "Assets: Cleaning...";
    badge.style.color = "var(--accent-gold)";
  }
  log("Wiping custom update assets from " + currentDevice + " (vanilla state)...");
  try {
    const res = await fetch("/api/assets/clean", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device: currentDevice })
    });
    const data = await res.json();
    if (data.ok) {
      log("Assets cleared! Game prepared for clean vanilla launch.", "success");
      if (badge) {
        badge.textContent = "Assets: Vanilla";
        badge.style.color = "var(--text-muted)";
      }
    } else {
      log("Asset clean failed: " + (data.reply || data.error), "error");
    }
  } catch (e) {
    log("Asset clean network error: " + e, "error");
  }
}

async function restartGameTest() {
  log("Restarting Hay Day on " + currentDevice + " to test live assets...");
  try {
    const res = await fetch("/api/assets/restart_game", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ device: currentDevice })
    });
    const data = await res.json();
    log(data.reply || (data.ok ? "Game restarted" : "Restart failed"), data.ok ? "success" : "error");
  } catch (e) {
    log("Restart error: " + e, "error");
  }
}

function openAssetEditor() {
  log("To open the interactive Asset Editor console, double-click run_asset_editor.bat or run: python asset_editor.py", "info");
  alert("Interactive Live Asset Editor:\n\nTo inspect and edit CSV exceed assets interactively, run:\nrun_asset_editor.bat\n\nor run:\npython asset_editor.py in terminal.");
}
