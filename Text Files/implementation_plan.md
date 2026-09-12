# Hay Day Configuration Merge & Customization: HAY_STAR

Merge and customize the Hay Day game data files from the two source folders (`نسخة اقل سعر` and `نسخه اعلى سعر`) into a unified, high-reward configuration with rock-bottom Tom prices, enhanced XP/Coins, and professional `HAY_STAR` branding.

## User Review Required

> [!IMPORTANT]
> - **Source Folders Deletion**: The two original folders (`نسخة اقل سعر` and `نسخه اعلى سعر`) will be safely merged and verified before being deleted, in accordance with your explicit instructions.
> - **Direct Main Folder Deployment**: The merged files will be deployed both into a dedicated `HAY_STAR/update` directory and directly into `com.supercell.hayday/update` for immediate game client loading.
> - **Scale Ranges**:
>   - **Tom Purchase Prices**: Set to lowest (`DumbValue = 1` for all goods), so Tom buys items for less than 10 coins.
>   - **Harvesting & Collecting XP**: Crops (`fields.csv`, `fruits.csv`), animal products (`animal_goods.csv`), and factory items will yield between 1,000 XP (starting tier) and 1,000,000 XP (high tier).
>   - **Truck & Cargo Orders**: Coin rewards scaled between 1,000 and 10,000,000 coins; XP rewards scaled between 1,000 and 1,000,000 XP.
>   - **Farm Visitors (People Orders)**: XP rewards (`ConstantExp`) scaled from 1,000 to 1,000,000; friendship coin rewards scaled up to 10,000,000.
>   - **Branding**: All loading screen and HUD brandings (`s1_v11`, `GAU`, `سجاد هادي`, `Trần Thuận`) updated to `✨ HAY_STAR ✨` (with mention of `Ashraf Morningstar`).

---

## Proposed Changes

### 1. Merged Directory & Base Selection
- Create the merge workspace `HAY_STAR`.
- Use the complete set of 399 files as the base.
- Adopt the low price settings from `نسخة اقل سعر` where all item base prices (`DumbValue`) are set to `1`, ensuring Tom offers items for less than 10 coins.

### 2. High Rewards Configuration (XP & Coins)

#### Item Data Files (64+ goods files including `fields.csv`, `fruits.csv`, `animal_goods.csv`, `bakery_goods.csv`, etc.)
- **`ExpCollect` (Harvesting & Collecting XP)**:
  - Scale proportionally based on item level / tier:
    - Base crops/items (e.g., Wheat, Corn, Egg): **1,000 XP**
    - Mid-tier items: **10,000 – 100,000 XP**
    - High-tier items: up to **1,000,000 XP**
- **`OrderPrice` (Truck, Cargo, and Visitor Coin Rewards)**:
  - Scale from **1,000 coins** minimum up to **10,000,000 coins** maximum based on product tier and unlock level.
- **`OrderExp` (Truck & Cargo XP Rewards)**:
  - Scale from **1,000 XP** minimum up to **1,000,000 XP** maximum.
- **`DumbValue` (Tom Pricing)**:
  - Kept strictly at **1** so Tom's purchase cost remains under 10 coins.

#### Pets & Sanctuary Animals (`pets.csv`, `sanctuary_animals.csv`)
- **`Exp`**: Scale pet feeding / sanctuary animal XP rewards between **1,000** and **1,000,000 XP**.

#### Visitor & People Rewards (`people_spawners_rewards.csv`, `people_friendship.csv`, `reengagement_config.csv`)
- **`people_spawners_rewards.csv`**:
  - Update `ConstantExp` from level 1 to 100+ to scale from **1,000 XP** to **1,000,000 XP**.
- **`people_friendship.csv`**:
  - Update `FreeCash` coin rewards to scale from **1,000** up to **10,000,000 coins**.
- **`reengagement_config.csv`**:
  - Boost `PeopleOrderCoinBonus` and order rewards.

### 3. Professional Branding (`HAY_STAR`)
- In all localization CSVs (`update/localization/*.csv`):
  - `TID_LOADING_SCREEN_LOADING`: Replace old tags (`❣️s1_v11❣️`, `GAU`, etc.) with `✨ HAY_STAR ✨ Loading...` / localized equivalent.
  - `TID_ORDER_TABLE_TITLE`: Set to `✨ HAY_STAR ✨ Orders`.
  - `TID_SETTINGS_TITLE`: Set to `✨ HAY_STAR ✨ Settings` (and by `Ashraf Morningstar`).
  - `TID_SETTINGS_TAB_SETTINGS`: Set to `✨ HAY_STAR ✨ Settings`.
  - `TID_SETTINGS_SCID_CONNECTED`: Set to `✨ HAY_STAR ✨ Connected`.
  - `TID_ROADSIDE_SHOP_FRIEND_TITLE`: Replace custom names with `✨ HAY_STAR ✨`.

### 4. Integrity & Final Structure
- Regenerate SHA1 hashes in `fingerprint.json` for all modified files to ensure checksum consistency.
- Deploy the merged `update/` folder directly to the main folder `com.supercell.hayday/update`, as well as maintaining `HAY_STAR/update`.
- Delete the old source directories `نسخة اقل سعر` and `نسخه اعلى سعر`.

---

## Verification Plan

### Automated Verification
- Run a Python verification script that checks:
  1. Every goods file has `DumbValue == 1` (Tom price lowest).
  2. Every goods file has `ExpCollect` within [1,000, 1,000,000].
  3. Every goods file has `OrderPrice` within [1,000, 10,000,000].
  4. Every goods file has `OrderExp` within [1,000, 1,000,000].
  5. `people_spawners_rewards.csv` has `ConstantExp` within [1,000, 1,000,000].
  6. Localization files contain `HAY_STAR` and zero occurrences of legacy tags (`s1_v11`, `سجاد هادي`, `Trần Thuận`).
  7. `fingerprint.json` has valid matching SHA1 hashes for all files.
  8. Directory structure matches expectations.
