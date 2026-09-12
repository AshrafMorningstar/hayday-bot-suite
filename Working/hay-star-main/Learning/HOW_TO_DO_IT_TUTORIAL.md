# 🎓 Master Tutorial: How Everything Works in Hay★Star
### *The Complete, Ultra-Easy Guide (Even a 7-Year-Old Can Understand!)*

Welcome! In this tutorial, you will learn **exactly** how Hay★Star works under the hood, how we remove Google login screens, how we skip the crow (scarecrow) and startup clouds, how instant teleportation works without touching the screen, and how to operate all the features with 2-letter shortcuts!

---

## 🌟 Table of Contents
1. [How the Android Emulator Works with the Bot](#1-how-the-emulator-works)
2. [How We Remove the Google Login Screen Forever](#2-removing-the-google-login-screen)
3. [How We Remove the Crow (Scarecrow) & Clouds](#3-removing-the-crow-and-clouds)
4. [How Instant Teleportation Works (DeepLinks - Zero Touch!)](#4-instant-teleportation-via-deeplinks)
5. [How 110 Crops are Harvested in 0.1 Seconds (`nh`)](#5-how-crop-harvesting-and-planting-work)
6. [How Crop Planting Works (`np 400001`)](#6-how-crop-planting-works)
7. [The 2-Letter Shortcut Commands Cheat-Sheet](#7-shortcut-commands-cheat-sheet)
8. [Step-by-Step: How to Run the Bot on Your PC](#8-step-by-step-running-the-bot)

---

## 1. How the Android Emulator Works
When you play Hay Day on your computer, you run an emulator called **LDPlayer 9**.
LDPlayer creates a virtual Android phone inside Windows.

Hay★Star connects to this virtual Android phone using two high-speed bridges:
1. **ADB Bridge (`ldconsole.exe adb` / `adb.exe`):**
   Sends high-level OS commands directly into Android (rebooting, launching the game, taking screenshots, and pressing keys).
2. **In-Memory ARM64 Engine (`libmstar.so`):**
   A super-fast native C++ engine loaded directly into Hay Day's game code. When you tell it to harvest 110 crops, it doesn't swipe 110 times on the screen — it directly updates all 110 field objects inside the game's memory in less than 0.1 seconds!

---

## 2. Removing the Google Login Screen Forever

### Why did Google Login appear?
Whenever Android starts up or an app asks to log in to Google Play Games, Google Play Services opens an activity called:
`com.google.android.gms/.auth.uiflows.minutemaid.MinuteMaidActivity`
This popup covers the game and blocks all clicks!

### How Hay★Star removes it automatically:
We remove it at **two levels**:

#### Level 1: In the Game's JavaScript/Frida Hook (`hook.js`)
Inside `hook.js`, we intercept Hay Day's call to Google Play:
```javascript
// Intercept GoogleServiceClient so the game never opens the sign-in modal
Java.perform(function() {
    var GoogleServiceClient = Java.use("com.supercell.hayday.GoogleServiceClient");
    GoogleServiceClient.forNative_signIn.implementation = function() {
        console.log("[JAVA-GUARD] GoogleServiceClient.forNative_signIn() -> suppressed");
        return; // Returns immediately without opening Google Sign-In!
    };
});
```

#### Level 2: At the Android OS Level via ADB (`recovery_manager.py`)
If Android itself tries to show the login window, our `RecoveryManager` executes:
```python
# Force-stops the Google Play sign-in service
run_adb(["shell", "am force-stop com.google.android.gms"])

# Re-focuses Hay Day immediately
run_adb(["shell", "am start -n com.supercell.hayday/com.supercell.hayday.GameApp"])

# Sends Keycode 4 (Back key) to dismiss any remaining dialog
run_adb(["shell", "input keyevent 4"])
```
**Result:** The blue Google Sign-In screen disappears instantly, and the farm is displayed directly!

---

## 3. Removing the Crow (Scarecrow) & Clouds

### What is the "Crow"?
In Hay Day, the crow / scarecrow is **Mr. Wicker** (from `scarecrows.csv` and `tutorials.csv`). When a tutorial or hint triggers, Mr. Wicker pops up on screen with speech bubbles.

### What are the "Clouds"?
When Hay Day loads or changes areas, it plays an animation defined in `game_config.csv` called:
`CloudsExportName: cloud_formation`
These white clouds cover the entire screen while the game loads graphic textures.

### How Hay★Star removes them:
1. **Skipping Crow Dialogs:**
   In `recovery_manager.py`, the bot automatically dispatches tap events on the modal confirmation zone (`x=640, y=480` or `x=320, y=240`), which immediately advances and closes any visitor or Scarecrow speech bubbles.
2. **Clearing Startup Clouds:**
   The bot checks when `cloud_formation` finishes rendering by verifying the focused activity window. Once the game reaches `GameApp` and the surface is stable (checked via `dumpsys window`), the camera is immediately unlocked.

---

## 4. Instant Teleportation via DeepLinks (Zero Touch!)

Instead of dragging or swiping the screen with finger gestures (which can miss, lag, or get stuck), Hay Day has built-in **Supercell DeepLinks** defined in:
`install_time_asset_pack/assets/data/deeplinks.csv`

### Built-in DeepLinks in Hay Day:
| Landmark / Area | DeepLink URL | What it Does |
|---|---|---|
| **Fishing Lake** | `hayday://?action=VisitFishing` | Instantly flies camera to the Fishing Area & Angus |
| **Town Station** | `hayday://?action=VisitTown` | Instantly flies camera to the Town Train Station |
| **Greg's Farm** | `hayday://?action=VisitGregFarm` | Instantly teleports to Greg's farm |
| **Roadside Shop** | `hayday://?action=OpenDiamondShop` | Opens Roadside Shop and Crates |
| **Farm Center / Home** | `Tap Home (38, 442)` or `SelectGameObject` | Returns directly to Farmhouse and Crop Fields |

### How to trigger a DeepLink from Windows command line:
```bash
adb shell am start -p com.supercell.hayday -a android.intent.action.VIEW -d "hayday://?action=VisitFishing"
```
Notice the flag `-p com.supercell.hayday`. This tells Android to send the deep link **only** to Hay Day, preventing Google or a web browser from popping up!

---

## 5. How Crop Harvesting Works (`nh`)
In traditional bots, you have to drag the sickle tool across every field on the screen. If you have 110 fields, this takes 10 to 20 seconds and can miss plots.

In Hay★Star:
1. The Rust loader stages `libmstar.so` into memory via `loadnative` (`ln`).
2. When you send `nharvest` (`nh`), `libmstar.so` queries the field array:
   `Field 400000, 400001, 400002 ... 400109` (110 plots).
3. It sets the crop maturity timer to 0 and writes the harvest packet directly into the game engine's packet queue.
4. **All 110 crops are harvested in under 0.1 seconds!**

---

## 6. How Crop Planting Works (`np 400001`)
When planting wheat or any crop:
1. Global ID `400001` is Wheat (from `game_ids.py`).
2. The command `np 400001` targets all 110 field entities.
3. The native engine iterates through each empty plot and assigns seed ID `400001`.
4. The game UI instantly updates with fresh planted tilled soil!

---

## 7. Shortcut Commands Cheat-Sheet

You don't need to type long commands! Every command has an easy 2-letter shortcut:

| Shortcut | Full Command | What it Does |
|:---:|:---|:---|
| **`ln`** | `loadnative` | Loads the C++ ARM64 engine into Hay Day |
| **`nf`** | `nfields` | Lists all 110 field entity IDs |
| **`nh`** | `nharvest` | Harvests all 110 crop plots in < 0.1s |
| **`np`** | `nplant 400001` | Plants all 110 plots with wheat (or any crop ID) |
| **`ns`** | `nsell` | Sells crops in shop with anti-ban max price (-$1/-$2) |
| **`mc`** | `master_cycle` | Runs the 11-step full farming master loop |
| **`mr`** | `master_rotate`| Rotates between multiple accounts automatically |
| **`rc`** | `auto_heal` | Dismisses Google login, reload popups & reconnects |
| **`j`** | `jump <place>` | Teleports camera to `shop`, `animals`, `fishing`, `farm` |
| **`s`** | `search <item>`| Searches global item catalog (e.g. `s wheat`) |
| **`tst`**| `test_all` | Runs the full 28-test automated diagnostic suite |

---

## 8. Step-by-Step: Running the Bot

### Step 1: Launch the Emulator & Hay Day
Double-click `launch_emulator.bat` or run:
```bash
python launcher.py emu launch
```

### Step 2: Start the Hay★Star Engine
Run the launcher dashboard:
```bash
python launcher.py
```
Or start the interactive REPL:
```bash
python launcher.py repl
```

### Step 3: Run Full Auto-Farming
To let the bot harvest, plant, sell, feed animals, and collect coins continuously:
```bash
python launcher.py mc
```

**Congratulations!** You now know exactly how every piece of Hay★Star works from the ground up!
