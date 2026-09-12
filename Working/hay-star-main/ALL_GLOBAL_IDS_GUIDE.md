# 🌟 Super Easy Hay Day Global ID & Command Guide 🌟
### *Written so simply that even a 7-year-old child can understand and use it!* 🎈

---

## 🐣 Welcome! What is this guide?

In Hay Day, every single thing on your farm — every plant, animal, tool, cake, and pie — has a secret **Magic Number** called a **Global ID**.

When our bot talks to the game, it uses these magic numbers so it never makes a mistake! 

This guide teaches you:
1. 🧁 **The Magic Formula** (how the numbers are made).
2. 🔍 **How to find any item in 1 second** by typing a simple command.
3. 📋 **The Complete List of Magic Numbers** for every item in the game!
4. 🎮 **The Short 2-Letter Commands** so you don't have to type long words!

---

## 🪄 1. The Magic Formula (Super Easy Math!)

Every item belongs to a **Family** (we call it a `Class ID`).

Each Family has its own starting number:
- 🌱 **Family 4** = Crops (Things you plant in dirt)
- 🌾 **Family 6** = Animal Feed (Food you feed your pets & animals)
- 🍞 **Family 11** = Made in Machines (Bread, butter, sugar, cakes, pies)
- 🏭 **Family 13** = Buildings & Machines (Bakery, Dairy, Barn, Silo)
- 🔨 **Family 18** = Tools (Saws, axes, bolts, planks, deeds)
- 🐔 **Family 23** = Animals (Chickens, cows, pigs, sheep, goats)

### 🎈 How the Magic Number is Calculated:
Take the **Family Number**, multiply by **1,000,000**, and add the **Item Number**!

> **Example:**
> - Wheat is Crop #1 in Family 4: `(4 × 1,000,000) + 1 = 400001`!
> - Corn is Crop #2 in Family 4: `(4 × 1,000,000) + 2 = 400002`!
> - Carrot is Crop #3 in Family 4: `(4 × 1,000,000) + 3 = 400003`!
> - Bread is Product #1 in Family 11: `(11 × 1,000,000) + 1 = 11000001`!

That's it! Easy peasy lemon squeezy! 🍋

---

## ⚡ 2. How to Search Any Item in 1 Second!

You don't need to memorize any numbers. You can just ask Hay Star!

Just open your console or terminal and type:
```powershell
python launcher.py s wheat
```
*(Or inside `hay-star.exe`, just type `s wheat`)*

Hay Star will instantly reply:
```text
  [+] Found 1 match for 'wheat':
      Wheat (Crop) -> Global ID: 400001 | Max Price (10x): 36 coins
```

You can search for anything:
- `s bread` 🥖
- `s cheese` 🧀
- `s bolt` 🔩
- `s saw` 🪚
- `s diamond ring` 💍

---

## 📋 3. Complete Magic Number List

### 🌱 Crops & Plants (Family 4)
| Item Name | Magic Number (ID) | Max Price (10 items) | What it is |
|---|---|---|---|
| **Wheat** | `400001` | 36 coins | Grows in 2 minutes! |
| **Corn** | `400002` | 72 coins | Yellow sweet corn |
| **Carrot** | `400003` | 72 coins | Orange bunny treat |
| **Soybean** | `400004` | 108 coins | Green beans for cow feed |
| **Sugarcane** | `400005` | 144 coins | Sweet stalks for sugar |
| **Pumpkin** | `400006` | 396 coins | Big orange pumpkin |
| **Indigo** | `400007` | 252 coins | Blue flower for dyes |
| **Cotton** | `400008` | 288 coins | White fluff for clothes |
| **Chili Pepper**| `400009` | 360 coins | Spicy red pepper |
| **Tomato** | `400010` | 432 coins | Juicy red tomatoes |
| **Strawberry** | `400011` | 504 coins | Sweet red berry |
| **Potato** | `400012` | 360 coins | Brown potatoes |
| **Rice** | `400013` | 400 coins | White rice |
| **Lettuce** | `400014` | 324 coins | Crispy green salad leaves |

---

### 🔨 Expansion & Clearing Tools (Family 18)
*🚨 IMPORTANT: The bot NEVER sells these tools! It keeps them safe for you!* 🛡️

| Item Name | Magic Number (ID) | Max Price | What it does |
|---|---|---|---|
| **Bolt** | `18000001` | 270 coins | Upgrades your Barn! |
| **Plank** | `18000002` | 270 coins | Upgrades your Barn! |
| **Duct Tape** | `18000003` | 270 coins | Upgrades your Barn! |
| **Box of Nails**| `18000004` | 270 coins | Upgrades your Silo! |
| **Wood Panel** | `18000005` | 270 coins | Upgrades your Silo! |
| **Screw** | `18000006` | 270 coins | Upgrades your Silo! |
| **Land Deed** | `18000007` | 403 coins | Expands farm land! |
| **Mallet** | `18000008` | 403 coins | Expands farm land! |
| **Marker Stake**| `18000009` | 403 coins | Expands farm land! |
| **Saw** | `18000010` | 54 coins | Cuts down dead trees! |
| **Axe** | `18000011` | 43 coins | Cuts down dead bushes! |
| **Shovel** | `18000012` | 108 coins | Digs in the mine! |
| **Pickaxe** | `18000013` | 126 coins | Mines silver and gold! |
| **Dynamite** | `18000014` | 25 coins | Blows up mine rocks! |
| **TNT Barrel** | `18000015` | 72 coins | Big explosion in mine! |

---

### 🌾 Animal Feeds (Family 6)
| Feed Name | Magic Number (ID) | Made For | Ingredients |
|---|---|---|---|
| **Chicken Feed** | `600001` | 🐔 Chickens | Wheat + Corn |
| **Cow Feed** | `600002` | 🐮 Cows | Corn + Soybean |
| **Pig Feed** | `600003` | 🐷 Pigs | Carrot + Soybean |
| **Sheep Feed** | `600004` | 🐑 Sheep | Wheat + Soybean |
| **Goat Feed** | `600005` | 🐐 Goats | Wheat + Corn + Carrot |

---

### 🍞 Food & Products (Family 11)
| Product Name | Magic Number (ID) | Building Made In | Max Price (10x) |
|---|---|---|---|
| **Bread** | `11000001` | Bakery | 216 coins |
| **Cornbread** | `11000002` | Bakery | 720 coins |
| **Cookie** | `11000003` | Bakery | 1,044 coins |
| **Cream** | `11000004` | Dairy | 504 coins |
| **Butter** | `11000005` | Dairy | 828 coins |
| **Cheese** | `11000006` | Dairy | 1,224 coins |
| **Brown Sugar** | `11000007` | Sugar Mill | 324 coins |
| **White Sugar** | `11000008` | Sugar Mill | 504 coins |
| **Syrup** | `11000009` | Sugar Mill | 900 coins |
| **Popcorn** | `11000010` | Popcorn Pot | 324 coins |
| **Butter Popcorn**| `11000011` | Popcorn Pot | 1,260 coins |
| **Pancake** | `11000012` | BBQ Grill | 1,080 coins |
| **Bacon and Eggs**| `11000013` | BBQ Grill | 2,016 coins |
| **Carrot Pie** | `11000014` | Pie Oven | 828 coins |
| **Pumpkin Pie** | `11000015` | Pie Oven | 1,584 coins |
| **Bacon Pie** | `11000016` | Pie Oven | 2,196 coins |
| **Apple Pie** | `11000017` | Pie Oven | 2,700 coins |
| **Fish Pie** | `11000018` | Pie Oven | 2,268 coins |
| **Cotton Fabric**| `11000019` | Loom | 468 coins |
| **Blue Sweater** | `11000020` | Loom | 2,088 coins |

---

### 💍 Jewelry & Smelter Bars (Family 11)
*🚨 Bot protects these and sells only when you have surplus!*

| Item Name | Magic Number (ID) | Max Price (10x) |
|---|---|---|
| **Silver Bar** | `11000040` | 1,476 coins |
| **Gold Bar** | `11000041` | 1,800 coins |
| **Platinum Bar** | `11000042` | 2,052 coins |
| **Refined Coal** | `11000043` | 1,080 coins |
| **Iron Bar** | `11000044` | 1,296 coins |
| **Diamond Ring** | `11000045` | 8,244 coins |
| **Bracelet** | `11000046` | 5,148 coins |
| **Necklace** | `11000047` | 7,272 coins |

---

### 🎣 Fishing Lake Items (Family 11)
| Fishing Item | Magic Number (ID) | How it's made | Cost |
|---|---|---|---|
| **Red Lure** | `11000030` | Lure Workbench | **0 Diamonds (FREE!)** |
| **Green Lure** | `11000031` | Lure Workbench | Voucher |
| **Blue Lure** | `11000032` | Lure Workbench | Voucher |
| **Fishing Net** | `11000035` | Netmaker | Free |
| **Lobster Trap**| `11000036` | Netmaker | Free |
| **Duck Trap** | `11000037` | Netmaker | Free |

---

## 🎮 4. Command Quick Reference (Long vs Short)

You can type either the **Full Word** or the **2-Letter Shortcut**! Both work identically!

| What you want to do | Full Command | Easy 2-Letter Shortcut | Example to Type |
|---|---|---|---|
| **Single Farm Auto Loop** | `master_cycle` | `mc` | `mc` |
| **Multi-Account Auto Loop** | `master_rotate`| `mr` | `mr` |
| **Fix Stuck Screen / Reconnect**| `auto_heal` | `rc` | `rc` |
| **Open Menu Dashboard** | `dashboard` | `db` (or `dash`) | `db` |
| **Run All Automations** | `auto` | `all` | `all` |
| **Load Bot Engine** | `loadnative` | `ln` | `ln` |
| **Find Farm Fields** | `nfields` | `nf` | `nf` |
| **Plant Any Crop** | `nplant` | `np` | `np 400001` (plants wheat) |
| **Harvest All Crops** | `nharvest` | `nh` | `nh` |
| **Sell Item in Shop** | `nsell` | `ns` | `ns 0 10 36 1 400001` |
| **Teleport Camera** | `jump` | `j` | `j shop` or `j farm` |
| **Search Magic ID Number** | `search` | `s` | `s wheat` or `s 400001` |
| **Show ID Family Summary**| `ids` | `ids` | `ids` |
| **Run All 28 Tests** | `test` | `tst` | `tst` |
| **Show Help Menu** | `help` | `h` | `h` |
| **Exit Bot** | `quit` | `q` | `q` |

---

## 🧸 5. How Even a 7-Year-Old Can Test It in 1 Minute!

Here are 3 super fun tests you can do right now:

### Test 1: Search for Chocolate or Bread 🍫
1. Open your terminal or console.
2. Type:
   ```powershell
   python launcher.py s bread
   ```
3. Look at that! It shows you Bread's ID and price in 0.1 seconds!

### Test 2: Fix any connection popup with 2 letters! 🔄
1. Type:
   ```powershell
   python launcher.py rc
   ```
2. The bot instantly checks LDPlayer, taps through any "Reload game" or "Another device connected" popup, and brings Hay Day right back!

### Test 3: Run the 28-Test Certificate! 🏆
1. Type:
   ```powershell
   python tests/test_all.py
   ```
2. Watch all 28 green checkmarks go `ok`! 
3. When you see `ALL TESTS PASSED! FULL SYSTEM VERIFIED`, your bot is 100% healthy and ready to farm!

---

*Made with ❤️ for Hay Day farmers of all ages!* 🚜🌾
