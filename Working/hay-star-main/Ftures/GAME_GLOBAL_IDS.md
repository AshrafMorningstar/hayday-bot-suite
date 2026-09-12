# Hay Day - Complete Global Game IDs & In-Game Objects Reference

This official reference contains the reverse-engineered in-game Global IDs and data attributes
for Hay Day (`com.supercell.hayday`). Used directly by the `inxernal` native engine and loader.

> **Global ID Architecture**:
> - Type 4 Objects (Plots / Fields): `400000 + Index` (e.g. Wheat = `400001`, Corn = `400002`).
> - Standard Supercell Entity IDs: `ClassID * 1000000 + InstanceID`.

---

## 1. Plots & Crops (`fields.csv` - Class 4)
These IDs are passed directly to `nplant <cropId>` and field automation.

| Global ID | Crop Name | Unlock Level | Grow Time | Harvest Yield | Max Coin Price | XP |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `400000` | **EmptyField** | 0 | 0s | 0 | 1 | 0 |
| `400001` | **Wheat** | 1 | 2m 0s | 2 | 0 | 100 |
| `400002` | **Corn** | 2 | 5m 0s | 2 | 0 | 100 |
| `400003` | **Soybean** | 5 | 20m 0s | 2 | 0 | 100 |
| `400004` | **Sugarcane** | 7 | 30m 0s | 2 | 0 | 100 |
| `400005` | **Carrot** | 9 | 10m 0s | 2 | 0 | 100 |
| `400006` | **Indigo** | 13 | 120m 0s | 2 | 0 | 100 |
| `400007` | **Pumpkin** | 15 | 180m 0s | 2 | 0 | 100 |
| `400008` | **Chili** | 25 | 240m 0s | 2 | 0 | 100 |
| `400009` | **Tomato** | 30 | 360m 0s | 2 | 0 | 100 |
| `400010` | **Strawberry** | 34 | 480m 0s | 2 | 0 | 100 |
| `400011` | **Potato** | 35 | 220m 0s | 2 | 0 | 100 |
| `400012` | **Rice** | 56 | 45m 0s | 2 | 0 | 100 |
| `400013` | **Lettuce** | 58 | 210m 0s | 2 | 0 | 100 |
| `400014` | **Cotton** | 18 | 150m 0s | 2 | 0 | 100 |
| `400015` | **Onion** | 68 | 300m 0s | 2 | 0 | 100 |
| `400016` | **TeaLeaves** | 80 | 390m 0s | 2 | 0 | 100 |
| `400017` | **Grapes** | 84 | 180m 0s | 2 | 0 | 100 |
| `400018` | **Sunflower** | 63 | 90m 0s | 2 | 0 | 100 |
| `400019` | **Peony** | 82 | 240m 0s | 2 | 0 | 100 |
| `400020` | **Bellpepper** | 74 | 270m 0s | 2 | 0 | 100 |
| `400021` | **Mint** | 85 | 180m 0s | 2 | 0 | 100 |
| `400022` | **Watermelon** | 92 | 300m 0s | 2 | 0 | 100 |
| `400023` | **Cucumber** | 70 | 35m 0s | 2 | 0 | 100 |
| `400024` | **Pineapple** | 52 | 30m 0s | 2 | 0 | 100 |
| `400025` | **Eggplant** | 90 | 40m 0s | 2 | 0 | 100 |
| `400026` | **Broccoli** | 83 | 80m 0s | 2 | 0 | 100 |
| `400027` | **Mushroom** | 89 | 20m 0s | 2 | 0 | 100 |
| `400028` | **Ginger** | 78 | 150m 0s | 2 | 0 | 100 |
| `400029` | **Sesame** | 50 | 60m 0s | 2 | 0 | 100 |
| `400030` | **Lily** | 53 | 90m 0s | 2 | 0 | 100 |
| `400031` | **Beetroot** | 72 | 40m 0s | 2 | 0 | 100 |
| `400032` | **Garlic** | 60 | 30m 0s | 2 | 0 | 100 |
| `400033` | **Cabbage** | 65 | 45m 0s | 2 | 0 | 100 |
| `400034` | **Clay** | 94 | 110m 0s | 2 | 0 | 100 |
| `400035` | **Chickpea** | 95 | 60m 0s | 2 | 0 | 100 |
| `400036` | **PassionFruit** | 88 | 60m 0s | 2 | 0 | 100 |
| `400037` | **Asparagus** | 49 | 360m 0s | 2 | 0 | 100 |
| `400038` | **Oats** | 119 | 7m 0s | 2 | 0 | 100 |
| `400039` | **Chamomile** | 45 | 20m 0s | 2 | 0 | 100 |
| `400040` | **BlackBean** | 25 | 10m 0s | 2 | 0 | 100 |

## 2. Storage & Marketplace Infrastructure
| Global ID | Name | Category | Description |
|:---|:---|:---|:---|
| `610001` | **Silo (Crops)** | Storage / Market | Silo storage for crops and fruits |
| `610002` | **Barn (Items)** | Storage / Market | Barn storage for animal goods, tools, and products |
| `610003` | **Roadside Shop** | Storage / Market | Roadside Shop marketplace for selling items |

## 3. Production Buildings (`processing_buildings.csv` - Class 6) [62 Buildings]
| Global ID | Building Name | Level | Build Coins | Build Time | Grid Size | Slots |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| `600000` | **Bakery** | 2 | 20 | 0m | 3x3 | 2 |
| `600001` | **Hammermill** | 3 | 5 | 0m | 3x3 | 3 |
| `600002` | **Popcorn_Pot** | 8 | 100 | 3m | 3x3 | 2 |
| `600003` | **Dairy** | 6 | 50 | 0m | 4x4 | 2 |
| `600004` | **Sugar_Mill** | 7 | 100 | 2m | 2x2 | 2 |
| `600005` | **Pie_Oven** | 14 | 1,000 | 5m | 3x3 | 2 |
| `600006` | **Loom** | 17 | 3,200 | 1440m | 2x2 | 2 |
| `600007` | **Cake_Oven** | 21 | 12,100 | 1440m | 3x3 | 2 |
| `600008` | **Barbecue_Grill** | 9 | 500 | 5m | 2x2 | 2 |
| `600009` | **Juice_Press** | 26 | 31,000 | 1920m | 2x2 | 2 |
| `600010` | **Jam_Maker** | 35 | 59,000 | 2160m | 2x2 | 2 |
| `600011` | **Smelter** | 24 | 12,500 | 1080m | 2x2 | 1 |
| `600012` | **Ice_Cream_Maker** | 29 | 38,000 | 1920m | 2x3 | 2 |
| `600013` | **Jeweler** | 38 | 68,000 | 2160m | 2x2 | 2 |
| `600014` | **Cafe_Kiosk** | 42 | 75,000 | 2160m | 2x2 | 2 |
| `600015` | **Candy_Machine** | 51 | 120,000 | 1920m | 2x2 | 2 |
| `600016` | **Soup_Kitchen** | 46 | 115,000 | 2160m | 2x2 | 2 |
| `600017` | **Sauce_Mixer** | 54 | 135,000 | 2400m | 3x3 | 2 |
| `600018` | **Sushi_Bar** | 56 | 150,000 | 2640m | 2x2 | 2 |
| `600019` | **Salad_Bar** | 58 | 165,000 | 2880m | 3x3 | 2 |
| `600020` | **Sandwich_Bar** | 61 | 180,000 | 3120m | 3x3 | 2 |
| `600021` | **Smoothie_Mixer** | 64 | 220,000 | 4320m | 2x2 | 2 |
| `600022` | **Sewing_Machine** | 19 | 4,500 | 1200m | 2x2 | 2 |
| `600023` | **Honey_Extractor** | 39 | 35,000 | 1440m | 2x2 | 2 |
| `600024` | **Candle_Maker** | 48 | 118,000 | 2280m | 2x2 | 2 |
| `600025` | **Hat_Maker** | 70 | 260,000 | 4560m | 2x2 | 2 |
| `600026` | **Pasta_Maker** | 67 | 400,000 | 4800m | 2x2 | 2 |
| `600027` | **Hotdog_Stand** | 75 | 650,000 | 5280m | 2x2 | 2 |
| `600028` | **Pasta_Kitchen** | 72 | 550,000 | 5040m | 2x2 | 2 |
| `600029` | **Taco_Kitchen** | 77 | 700,000 | 5400m | 2x2 | 2 |
| `600030` | **Tea_Stand** | 80 | 750,000 | 5700m | 2x2 | 2 |
| `600031` | **Flowershop** | 49 | 120,000 | 2400m | 2x2 | 2 |
| `600032` | **Wok_Kitchen** | 69 | 350,000 | 4800m | 2x2 | 2 |
| `600033` | **Fondue_Maker** | 81 | 800,000 | 5760m | 2x2 | 2 |
| `600034` | **Deep_Fryer** | 87 | 900,000 | 5760m | 2x2 | 2 |
| `600035` | **Bath_Kiosk** | 84 | 850,000 | 5760m | 2x2 | 2 |
| `600036` | **Donut_Maker** | 76 | 680,000 | 5400m | 2x2 | 2 |
| `600037` | **Preservation_Station** | 91 | 950,000 | 5760m | 2x2 | 2 |
| `600038` | **Pottery_Studio** | 94 | 1,000,000 | 5760m | 2x2 | 2 |
| `600039` | **Fudge_Shop** | 99 | 1,050,000 | 5760m | 2x2 | 2 |
| `600040` | **Yoghurt_Maker** | 103 | 1,100,000 | 5760m | 2x2 | 2 |
| `600041` | **Stew_Pot** | 106 | 1,150,000 | 5760m | 2x2 | 2 |
| `600042` | **Cupcake_Maker** | 109 | 1,200,000 | 5760m | 2x2 | 2 |
| `600043` | **Gift_Wrapping_Station** | 1 | 10 | 0m | 2x2 | 2 |
| `600044` | **Waffle_Maker** | 114 | 1,250,000 | 5760m | 2x2 | 2 |
| `600045` | **Easter_Egg_Maker** | 1 | 10 | 0m | 2x2 | 2 |
| `600046` | **Omelet_Maker** | 77 | 600,000 | 4800m | 2x2 | 2 |
| `600047` | **Porridge_Bar** | 119 | 1,300,000 | 5760m | 2x2 | 2 |
| `600048` | **Gift_Wrapping_Station_2023** | 1 | 10 | 0m | 2x2 | 2 |
| `600049` | **Milkshake_Bar** | 124 | 1,350,000 | 5760m | 2x2 | 2 |
| `600050` | **Easter_Egg_Maker_2024** | 1 | 10 | 0m | 2x2 | 2 |
| `600051` | **Essentials_Oil_Lab** | 68 | 85,000 | 4800m | 2x2 | 2 |
| `600052` | **Birthday_Balloon_Maker_2024** | 1 | 10 | 0m | 2x2 | 2 |
| `600053` | **Halloween_Candy_Maker_2024** | 1 | 10 | 0m | 2x2 | 2 |
| `600054` | **Gift_Wrapping_Station_2024** | 1 | 10 | 0m | 2x2 | 2 |
| `600055` | **Perfumerie** | 110 | 1,000,000 | 5760m | 2x2 | 2 |
| `600056` | **Easter_Egg_Maker_2025** | 1 | 10 | 0m | 2x2 | 2 |
| `600057` | **Birthday_Balloon_Maker_2025** | 1 | 10 | 0m | 2x2 | 2 |
| `600058` | **Halloween_Candy_Maker_2025** | 1 | 10 | 0m | 2x2 | 2 |
| `600059` | **Gift_Wrapping_Station_2025** | 1 | 10 | 0m | 2x2 | 2 |
| `600060` | **Doner_Kebab_Stand** | 32 | 22,000 | 1440m | 2x2 | 2 |
| `600061` | **Birthday_Balloon_Maker_2026** | 1 | 10 | 0m | 2x2 | 2 |

## 4. Expansion & Upgrade Materials (`collection_tools.csv`) [16 Items]
Essential upgrade parts for Silo, Barn, Land Expansion, and Town service buildings.

| Global ID | Item Name | Category |
|:---|:---|:---|
| `1410000` | **Plank** | Expansion & Building Upgrade Material |
| `1410001` | **Nail** | Expansion & Building Upgrade Material |
| `1410002` | **Bolt** | Expansion & Building Upgrade Material |
| `1410003` | **Screw** | Expansion & Building Upgrade Material |
| `1410004` | **Duct Tape** | Expansion & Building Upgrade Material |
| `1410005` | **Wood Panel** | Expansion & Building Upgrade Material |
| `1410006` | **Land Deed** | Expansion & Building Upgrade Material |
| `1410007` | **Mallet** | Expansion & Building Upgrade Material |
| `1410008` | **Marker Stake** | Expansion & Building Upgrade Material |
| `1410009` | **Hammer** | Expansion & Building Upgrade Material |
| `1410010` | **Hand Drill** | Expansion & Building Upgrade Material |
| `1410011` | **Paint Bucket** | Expansion & Building Upgrade Material |
| `1410012` | **Stone Block** | Expansion & Building Upgrade Material |
| `1410013` | **Brick** | Expansion & Building Upgrade Material |
| `1410014` | **Tar Bucket** | Expansion & Building Upgrade Material |
| `1410015` | **Map Piece** | Expansion & Building Upgrade Material |

## 5. Clearing & Mining Tools (`tools.csv` - Class 14)
| Global ID | Tool Name | Unlock Level | Max Price | Diamond Price |
|:---|:---|:---:|:---:|:---:|
| `1400000` | **Dynamite** | 5 | 0 | 3 |
| `1400001` | **Demolition Charge** | 5 | 0 | 7 |
| `1400002` | **Axe** | 5 | 0 | 4 |
| `1400003` | **Saw** | 5 | 0 | 5 |
| `1400004` | **Shovel** | 5 | 0 | 10 |
| `1400005` | **Pickaxe** | 34 | 0 | 12 |

## 6. Farm Animals & Products (`animals.csv` & `animal_goods.csv`)
### Farm Animals
| Global ID | Animal Name | Habitat | Level | Buy Price |
|:---|:---|:---|:---:|:---:|
| `800000` | **Chicken** |  | 1 | 10 |
| `800001` | **Cow** |  | 6 | 50 |
| `800002` | **Sheep** |  | 16 | 800 |
| `800003` | **Pig** |  | 10 | 500 |
| `800004` | **Goat** |  | 32 | 2150 |
| `800005` | **Lamb** |  | 25 | 800 |

### Animal Products
| Global ID | Product Name | Unlock Level | Produce Time | Max Coin Price | XP |
|:---|:---|:---:|:---:|:---:|:---:|
| `810000` | **Egg** | 1 | 20m | 0 | 100 |
| `810001` | **Milk** | 6 | 60m | 0 | 100 |
| `810002` | **Wool** | 16 | 360m | 0 | 100 |
| `810003` | **Bacon** | 10 | 240m | 0 | 100 |
| `810004` | **Goat Milk** | 32 | 480m | 0 | 100 |
| `810005` | **Lamb Meat** | 25 | 30m | 0 | 100 |

## 7. Fruit Trees & Bushes (`fruit_trees.csv` - Class 10)
| Global ID | Tree / Bush Name | Unlock Level | Buy Price | Harvests | Grow Time |
|:---|:---|:---:|:---:|:---:|:---:|
| `1000000` | **AppleTree** | 1 | 160 | 3 | 960m |
| `1000001` | **CherryTree** | 1 | 410 | 3 | 1680m |
| `1000002` | **RaspberryBush** | 1 | 220 | 3 | 1080m |
| `1000003` | **BlackberryBush** | 1 | 530 | 3 | 1920m |
| `1000004` | **CacaoTree** | 1 | 550 | 3 | 2100m |
| `1000005` | **CoffeeBush** | 1 | 375 | 3 | 1500m |
| `1000006` | **OliveTree** | 1 | 620 | 3 | 1440m |
| `1000007` | **LemonTree** | 1 | 670 | 3 | 1800m |
| `1000008` | **PeachTree** | 1 | 750 | 3 | 1800m |
| `1000009` | **OrangeTree** | 1 | 720 | 3 | 1860m |
| `1000010` | **BananaTree** | 1 | 800 | 3 | 1680m |
| `1000011` | **PlumTree** | 1 | 600 | 3 | 1500m |
| `1000012` | **MangoTree** | 1 | 770 | 3 | 1920m |
| `1000013` | **CoconutTree** | 1 | 810 | 3 | 2160m |
| `1000014` | **GuavaTree** | 1 | 860 | 3 | 2040m |
| `1000015` | **PomegranateTree** | 1 | 910 | 3 | 1620m |
| `1000016` | **BlueberryBush** | 1 | 550 | 3 | 2100m |

## 8. Boats & Fishing Lake (`boats.csv`, `fishing_boat.csv`, `fishing_areas.csv`, `nets.csv`)
| Global ID | Name | Category | Unlock Level |
|:---|:---|:---|:---:|
| `2000000` | **Cargo River Boat: Boat** | Cargo Boat | 17 |
| `2010000` | **Fishing Boat: FishingBoatWreck** | Fishing Boat | 27 |
| `2010001` | **Fishing Boat: FishingBoat** | Fishing Boat | 27 |
| `2010002` | **Fishing Boat: FishingBoatFishing** | Fishing Boat | 27 |
| `2030000` | **Fishing Net/Trap: LobsterBox** | Net / Trap | 44 |
| `2030001` | **Fishing Net/Trap: FishingNet** | Net / Trap | 30 |
| `2030002` | **Fishing Net/Trap: MysteryNet** | Net / Trap | 30 |
| `2030003` | **Fishing Net/Trap: DuckTrap** | Net / Trap | 50 |

## 9. Delivery Truck & Orders (`orders.csv`)
| Global ID | Destination / Customer | Description |
|:---|:---|:---|
| `700000` | **Order Kindergarten** | Truck Delivery Customer: Order Kindergarten |
| `700001` | **Order School** | Truck Delivery Customer: Order School |
| `700002` | **Order Church** | Truck Delivery Customer: Order Church |
| `700003` | **Order Joan's Salon** | Truck Delivery Customer: Order Joan's Salon |
| `700004` | **Order Susan's Store** | Truck Delivery Customer: Order Susan's Store |
| `700005` | **Order Mike's Mill** | Truck Delivery Customer: Order Mike's Mill |
| `700006` | **Order Ben's Brewery** | Truck Delivery Customer: Order Ben's Brewery |
| `700007` | **Order Fabio's Fishery** | Truck Delivery Customer: Order Fabio's Fishery |
| `700008` | **Order Frank's Factory** | Truck Delivery Customer: Order Frank's Factory |
| `700009` | **Order Grant's Graveyard** | Truck Delivery Customer: Order Grant's Graveyard |

## 10. Town & Trains (`service_buildings.csv`, `train.csv`)
| Global ID | Name | Category | Level | Cost |
|:---|:---|:---|:---:|:---:|
| `1800000` | **Grocery Store** | Town Service Building | 0 | 500 |
| `1800001` | **Movietheater** | Town Service Building | 0 | 4,500 |
| `1800002` | **Diner** | Town Service Building | 0 | 19,000 |
| `1800003` | **Bed and Breakfast** | Town Service Building | 0 | 31,000 |
| `1800004` | **Spa** | Town Service Building | 0 | 62,000 |
| `1800005` | **Beach cafe** | Town Service Building | 0 | 71,000 |
| `1800006` | **Gift shop** | Town Service Building | 0 | 67,000 |
| `1810000` | **EGGspress Train: PassengerTrain** | Town Train Transport | - | - |

## 11. Produced Goods & Food Recipes (Class 12) [407 Items]
All manufactured items across all production buildings (Bakery, Dairy, Grill, Pie Oven, Jam Maker, Smelter, etc.).

| Global ID | Item Name | Machine / Facility | Unlock Level | Time | Max Price | XP |
|:---|:---|:---|:---:|:---:|:---:|:---:|
| `1200000` | **Bread** | Bakery | 2 | 5m 0s | 0 | 100 |
| `1200001` | **Cookie** | Bakery | 10 | 60m 0s | 0 | 100 |
| `1200002` | **Corn Bread** | Bakery | 7 | 30m 0s | 0 | 100 |
| `1200003` | **Pizza** | Bakery | 33 | 15m 0s | 0 | 115 |
| `1200004` | **Spicy Pizza** | Bakery | 37 | 15m 0s | 0 | 135 |
| `1200005` | **Raspberry Muffin** | Bakery | 19 | 45m 0s | 0 | 100 |
| `1200006` | **Blackberry Muffin** | Bakery | 26 | 45m 0s | 0 | 135 |
| `1200007` | **Potato Bread** | Bakery | 39 | 45m 0s | 0 | 170 |
| `1200008` | **Frutti di Mare Pizza** | Bakery | 45 | 15m 0s | 0 | 240 |
| `1200009` | **BananaBread** | Bakery | 91 | 30m 0s | 0 | 250 |
| `1200010` | **Gingerbread Cookie** | Bakery | 86 | 30m 0s | 0 | 165 |
| `1200011` | **Macaroon** | Bakery | 101 | 30m 0s | 0 | 250 |
| `1200012` | **Pineapple coconut bars** | Bakery | 120 | 40m 0s | 0 | 170 |
| `1200013` | **Blueberry Muffin** | Bakery | 33 | 45m 0s | 0 | 140 |
| `1200014` | **Pancakes** | Barbecue Grill | 9 | 30m 0s | 0 | 100 |
| `1200015` | **Bacon and Eggs** | Barbecue Grill | 11 | 60m 0s | 0 | 120 |
| `1200016` | **Hamburger** | Barbecue Grill | 18 | 120m 0s | 0 | 110 |
| `1200017` | **Roasted Tomatoes** | Barbecue Grill | 30 | 90m 0s | 0 | 100 |
| `1200018` | **Baked Potato** | Barbecue Grill | 35 | 35m 0s | 0 | 180 |
| `1200019` | **Fishburger** | Barbecue Grill | 27 | 120m 0s | 0 | 135 |
| `1200020` | **Fish and Chips** | Barbecue Grill | 41 | 90m 0s | 0 | 145 |
| `1200021` | **Lobster Skewer** | Barbecue Grill | 48 | 40m 0s | 0 | 250 |
| `1200022` | **Grilled Onion** | Barbecue Grill | 68 | 60m 0s | 0 | 115 |
| `1200023` | **BananaPancakes** | Barbecue Grill | 94 | 60m 0s | 0 | 210 |
| `1200024` | **Grilled Eggplant** | Barbecue Grill | 90 | 40m 0s | 0 | 195 |
| `1200025` | **FishSkewer** | Barbecue Grill | 96 | 30m 0s | 0 | 105 |
| `1200026` | **Roast veggies** | Barbecue Grill | 72 | 25m 0s | 0 | 120 |
| `1200027` | **Garlic bread** | Barbecue Grill | 60 | 15m 0s | 0 | 120 |
| `1200028` | **Stuffed Bellpeppers** | Barbecue Grill | 80 | 20m 0s | 0 | 210 |
| `1200029` | **Grilled Asparagus** | Barbecue Grill | 67 | 75m 0s | 0 | 290 |
| `1200030` | **Grilled Lamb Skewer** | Barbecue Grill | 25 | 20m 0s | 0 | 100 |
| `1200031` | **Exfoliating Soap** | Bath Kiosk | 93 | 60m 0s | 0 | 215 |
| `1200032` | **Face Mask** | Bath Kiosk | 99 | 90m 0s | 0 | 190 |
| `1200033` | **Honey Soap** | Bath Kiosk | 84 | 60m 0s | 0 | 195 |
| `1200034` | **Lemon Lotion** | Bath Kiosk | 84 | 75m 0s | 0 | 240 |
| `1200035` | **Rich soap** | Bath Kiosk | 121 | 70m 0s | 0 | 160 |
| `1200036` | **Espreso** | Cafe | 42 | 5m 0s | 0 | 145 |
| `1200037` | **Latte** | Cafe | 43 | 10m 0s | 0 | 130 |
| `1200038` | **Mocha** | Cafe | 45 | 15m 0s | 0 | 175 |
| `1200039` | **Raspberry Mocha** | Cafe | 46 | 30m 0s | 0 | 155 |
| `1200040` | **Hot Chocolate** | Cafe | 47 | 25m 0s | 0 | 190 |
| `1200041` | **BananaLatte** | Cafe | 88 | 20m 0s | 0 | 165 |
| `1200042` | **Caramel latte** | Cafe | 62 | 15m 0s | 0 | 205 |
| `1200043` | **Cheese Cake** | Cake Oven | 24 | 240m 0s | 0 | 170 |
| `1200044` | **Carrot Cake** | Cake Oven | 21 | 90m 0s | 0 | 100 |
| `1200045` | **Birthday Cake** | Cake Oven | 23 | 180m 0s | 0 | 130 |
| `1200046` | **Chocolate Cake** | Cake Oven | 36 | 120m 0s | 0 | 190 |
| `1200047` | **Strawberry Cake** | Cake Oven | 35 | 180m 0s | 0 | 190 |
| `1200048` | **Berry Cake** | Cake Oven | 23 | 60m 0s | 0 | 155 |
| `1200049` | **Potato Feta Cake** | Cake Oven | 38 | 120m 0s | 0 | 185 |
| `1200050` | **Lemon Cake** | Cake Oven | 68 | 150m 0s | 0 | 535 |
| `1200051` | **Honey Apple Cake** | Cake Oven | 42 | 200m 0s | 0 | 285 |
| `1200052` | **Fruitcake** | Cake Oven | 89 | 180m 0s | 0 | 270 |
| `1200053` | **Pineapple Cake** | Cake Oven | 65 | 75m 0s | 0 | 155 |
| `1200054` | **Fancy Cake** | Cake Oven | 54 | 15m 0s | 0 | 245 |
| `1200055` | **Chocolate Roll** | Cake Oven | 95 | 90m 0s | 0 | 360 |
| `1200056` | **Pomegranate Cake** | Cake Oven | 108 | 160m 0s | 0 | 190 |
| `1200057` | **Blueberry Cheesecake** | Cake Oven | 31 | 240m 0s | 0 | 300 |
| `1200058` | **Strawberry Candle** | Candle Maker | 48 | 120m 0s | 0 | 220 |
| `1200059` | **Raspberry Candle** | Candle Maker | 52 | 105m 0s | 0 | 215 |
| `1200060` | **Lemon Candle** | Candle Maker | 72 | 135m 0s | 0 | 275 |
| `1200061` | **Floral candle** | Candle Maker | 95 | 120m 0s | 0 | 265 |
| `1200062` | **Party Candle** | Candle Maker | 84 | 110m 0s | 0 | 195 |
| `1200063` | **Caramel Apple** | Candy Machine | 51 | 120m 0s | 0 | 155 |
| `1200064` | **Toffee** | Candy Machine | 52 | 90m 0s | 0 | 105 |
| `1200065` | **Chocolate** | Candy Machine | 54 | 1200m 0s | 0 | 275 |
| `1200066` | **Lollipop** | Candy Machine | 57 | 720m 0s | 0 | 205 |
| `1200067` | **Jelly Beans** | Candy Machine | 60 | 1440m 0s | 0 | 405 |
| `1200068` | **SesameBrittle** | Candy Machine | 78 | 60m 0s | 0 | 160 |
| `1200069` | **CandiedPeanuts** | Candy Machine | 63 | 40m 0s | 0 | 320 |
| `1200070` | **Cotton Candy** | Candy Machine | 75 | 30m 0s | 0 | 135 |
| `1200071` | **CountyFairDummyLuckyBonusTicket** | Countyfair Dummy | 1 | 0s | 0 | 0 |
| `1200072` | **CountyFairDummyRibbon** | Countyfair Dummy | 1 | 0s | 0 | 0 |
| `1200073` | **Plain Cupcake** | Cupcake Maker | 109 | 40m 0s | 0 | 170 |
| `1200074` | **Tropical Cupcake** | Cupcake Maker | 112 | 90m 0s | 0 | 340 |
| `1200075` | **Cookie Cupcake** | Cupcake Maker | 114 | 120m 0s | 0 | 425 |
| `1200076` | **Guava Cupcake** | Cupcake Maker | 109 | 70m 0s | 0 | 350 |
| `1200077` | **Cream** | Dairy | 6 | 20m 0s | 0 | 100 |
| `1200078` | **Butter** | Dairy | 9 | 30m 0s | 0 | 100 |
| `1200079` | **Cheese** | Dairy | 12 | 60m 0s | 0 | 100 |
| `1200080` | **Goat Cheese** | Dairy | 33 | 90m 0s | 0 | 100 |
| `1200081` | **Loaded Fries** | Deep Fryer | 87 | 25m 0s | 0 | 180 |
| `1200082` | **Stuffed Peppers** | Deep Fryer | 98 | 40m 0s | 0 | 240 |
| `1200083` | **Hand Pies** | Deep Fryer | 91 | 20m 0s | 0 | 175 |
| `1200084` | **Fried Candy** | Deep Fryer | 100 | 15m 0s | 0 | 435 |
| `1200085` | **Falafel** | Deep Fryer | 98 | 55m 0s | 0 | 135 |
| `1200086` | **Samosa** | Deep Fryer | 103 | 75m 0s | 0 | 135 |
| `1200087` | **Lamb Doner Wrap** | Doner Kebab Stand | 32 | 20m 0s | 0 | 100 |
| `1200088` | **Spicy Bean Doner** | Doner Kebab Stand | 32 | 30m 0s | 0 | 280 |
| `1200089` | **Tower Doner Supreme** | Doner Kebab Stand | 58 | 40m 0s | 0 | 210 |
| `1200090` | **Plain donut** | Donut Maker | 76 | 15m 0s | 0 | 100 |
| `1200091` | **Cream donut** | Donut Maker | 86 | 25m 0s | 0 | 135 |
| `1200092` | **Bacon donut** | Donut Maker | 88 | 30m 0s | 0 | 230 |
| `1200093` | **Filled donut** | Donut Maker | 93 | 35m 0s | 0 | 240 |
| `1200094` | **Crunchy donut** | Donut Maker | 82 | 30m 0s | 0 | 355 |
| `1200095` | **Sprinkles donut** | Donut Maker | 79 | 20m 0s | 0 | 185 |
| `1200096` | **Lemon essential oil** | Essentials Oils Lab | 68 | 10m 0s | 0 | 170 |
| `1200097` | **Mint essential oil** | Essentials Oils Lab | 85 | 15m 0s | 0 | 100 |
| `1200098` | **Ginger essential oil** | Essentials Oils Lab | 80 | 20m 0s | 0 | 100 |
| `1200099` | **Chamomile essential oil** | Essentials Oils Lab | 74 | 10m 0s | 0 | 100 |
| `1200100` | **Fish Meat** | Fishing | 27 | 0s | 0 | 100 |
| `1200101` | **Lobster Meat** | Fishing | 44 | 0s | 0 | 120 |
| `1200102` | **Duck Down** | Fishing | 50 | 0s | 0 | 100 |
| `1200103` | **Mussel Meat** | Fishing | 1 | 0s | 0 | 100 |
| `1200104` | **Rustic Bouquet** | Flowershop | 49 | 45m 0s | 0 | 125 |
| `1200105` | **Bright Bouquet** | Flowershop | 65 | 20m 0s | 0 | 200 |
| `1200106` | **Soft Bouquet** | Flowershop | 93 | 30m 0s | 0 | 180 |
| `1200107` | **Candy bouquet** | Flowershop | 90 | 20m 0s | 0 | 330 |
| `1200108` | **Gracious bouquet** | Flowershop | 73 | 40m 0s | 0 | 300 |
| `1200109` | **Veggie Bouquet** | Flowershop | 106 | 15m 0s | 0 | 210 |
| `1200110` | **Birthday Bouquet** | Flowershop | 92 | 20m 0s | 0 | 210 |
| `1200111` | **Cheese fondue** | Fondue Pot | 91 | 20m 0s | 0 | 295 |
| `1200112` | **Meat fondue** | Fondue Pot | 86 | 30m 0s | 0 | 300 |
| `1200113` | **Chocolate fondue** | Fondue Pot | 81 | 25m 0s | 0 | 370 |
| `1200114` | **Tropical fondue** | Fondue Pot | 100 | 35m 0s | 0 | 250 |
| `1200115` | **Mint Fudge** | Fudge Shop | 102 | 150m 0s | 0 | 310 |
| `1200116` | **Chili Fudge** | Fudge Shop | 104 | 170m 0s | 0 | 320 |
| `1200117` | **Lemon Fudge** | Fudge Shop | 108 | 110m 0s | 0 | 350 |
| `1200118` | **Peanut Fudge** | Fudge Shop | 111 | 90m 0s | 0 | 680 |
| `1200119` | **Rich Fudge** | Fudge Shop | 99 | 120m 0s | 0 | 385 |
| `1200120` | **Honeycomb** | Gatherer Nest | 39 | 0s | 0 | 100 |
| `1200121` | **ClocheHat** | Hat Maker | 70 | 120m 0s | 0 | 280 |
| `1200122` | **TopHat** | Hat Maker | 72 | 210m 0s | 0 | 370 |
| `1200123` | **SunHat** | Hat Maker | 74 | 150m 0s | 0 | 330 |
| `1200124` | **FlowerCrown** | Hat Maker | 86 | 120m 0s | 0 | 200 |
| `1200125` | **Honey** | Honey Extractor | 39 | 20m 0s | 0 | 100 |
| `1200126` | **Beeswax** | Honey Extractor | 48 | 45m 0s | 0 | 140 |
| `1200127` | **Hot Dog** | Hotdog Stand | 75 | 30m 0s | 0 | 220 |
| `1200128` | **Tofu Dog** | Hotdog Stand | 76 | 45m 0s | 0 | 220 |
| `1200129` | **Corn Dog** | Hotdog Stand | 78 | 60m 0s | 0 | 315 |
| `1200130` | **Onion Dog** | Hotdog Stand | 80 | 75m 0s | 0 | 180 |
| `1200131` | **Vanilla Ice Cream** | Ice Cream Maker | 29 | 120m 0s | 0 | 100 |
| `1200132` | **Cherry Popsicle** | Ice Cream Maker | 33 | 180m 0s | 0 | 210 |
| `1200133` | **Strawberry Ice Cream** | Ice Cream Maker | 34 | 240m 0s | 0 | 200 |
| `1200134` | **Chocolate Ice Cream** | Ice Cream Maker | 39 | 150m 0s | 0 | 205 |
| `1200135` | **Orange Sorbet** | Ice Cream Maker | 78 | 210m 0s | 0 | 240 |
| `1200136` | **Peach Ice Cream** | Ice Cream Maker | 83 | 180m 0s | 0 | 270 |
| `1200137` | **BananaSplit** | Ice Cream Maker | 96 | 210m 0s | 0 | 240 |
| `1200138` | **MintIcecream** | Ice Cream Maker | 85 | 135m 0s | 0 | 170 |
| `1200139` | **SesameIceCream** | Ice Cream Maker | 50 | 120m 0s | 0 | 105 |
| `1200140` | **Peanut Butter Milkshake** | Ice Cream Maker | 68 | 100m 0s | 0 | 430 |
| `1200141` | **Affogato** | Ice Cream Maker | 78 | 20m 0s | 0 | 260 |
| `1200142` | **Coconut Ice Cream** | Ice Cream Maker | 102 | 15m 0s | 0 | 190 |
| `1200143` | **Fruit Sorbet** | Ice Cream Maker | 106 | 60m 0s | 0 | 310 |
| `1200144` | **Apple Jam** | Jam Maker | 35 | 360m 0s | 0 | 130 |
| `1200145` | **Raspberry Jam** | Jam Maker | 36 | 420m 0s | 0 | 150 |
| `1200146` | **Blackberry Jam** | Jam Maker | 37 | 480m 0s | 0 | 230 |
| `1200147` | **Cherry Jam** | Jam Maker | 38 | 420m 0s | 0 | 200 |
| `1200148` | **Strawberry Jam** | Jam Maker | 50 | 450m 0s | 0 | 160 |
| `1200149` | **Marmelade** | Jam Maker | 74 | 510m 0s | 0 | 270 |
| `1200150` | **Peach Jam** | Jam Maker | 79 | 480m 0s | 0 | 275 |
| `1200151` | **Grape Jam** | Jam Maker | 85 | 390m 0s | 0 | 100 |
| `1200152` | **PlumJam** | Jam Maker | 94 | 300m 0s | 0 | 230 |
| `1200153` | **Passion Fruit Jam** | Jam Maker | 96 | 320m 0s | 0 | 100 |
| `1200154` | **Blueberry Chutney** | Jam Maker | 70 | 240m 0s | 0 | 345 |
| `1200155` | **Bracelet** | Jeweler | 38 | 120m 0s | 0 | 305 |
| `1200156` | **Necklace** | Jeweler | 39 | 180m 0s | 0 | 435 |
| `1200157` | **Diamond Ring** | Jeweler | 40 | 240m 0s | 0 | 490 |
| `1200158` | **IronBracelet** | Jeweler | 41 | 90m 0s | 0 | 395 |
| `1200159` | **Flower Pendant** | Jeweler | 98 | 60m 0s | 0 | 415 |
| `1200160` | **Carrot Juice** | Juice Press | 26 | 30m 0s | 0 | 100 |
| `1200161` | **Tomato Juice** | Juice Press | 31 | 90m 0s | 0 | 100 |
| `1200162` | **Apple Juice** | Juice Press | 28 | 120m 0s | 0 | 100 |
| `1200163` | **Cherry Juice** | Juice Press | 30 | 150m 0s | 0 | 130 |
| `1200164` | **Berry Juice** | Juice Press | 31 | 180m 0s | 0 | 120 |
| `1200165` | **Orange Juice** | Juice Press | 71 | 120m 0s | 0 | 140 |
| `1200166` | **Grape Juice** | Juice Press | 84 | 150m 0s | 0 | 100 |
| `1200167` | **WatermelonLemonade** | Juice Press | 92 | 60m 0s | 0 | 100 |
| `1200168` | **Pineapple Juice** | Juice Press | 52 | 45m 0s | 0 | 100 |
| `1200169` | **Passion Fruit Juice** | Juice Press | 88 | 45m 0s | 0 | 100 |
| `1200170` | **Mango Juice** | Juice Press | 97 | 50m 0s | 0 | 135 |
| `1200171` | **Guava Juice** | Juice Press | 104 | 55m 0s | 0 | 150 |
| `1200172` | **Sweater** | Loom | 17 | 120m 0s | 0 | 100 |
| `1200173` | **Blue Woolly Hat** | Loom | 19 | 60m 0s | 0 | 100 |
| `1200174` | **Blue Sweater** | Loom | 20 | 180m 0s | 0 | 125 |
| `1200175` | **Red Scarf** | Loom | 48 | 150m 0s | 0 | 170 |
| `1200176` | **Cotton Fabrics** | Loom | 18 | 30m 0s | 0 | 100 |
| `1200177` | **Flower Shawl** | Loom | 71 | 90m 0s | 0 | 175 |
| `1200178` | **Vanilla Milkshake** | Milkshake Bar | 124 | 45m 0s | 0 | 400 |
| `1200179` | **Mocha Milkshake** | Milkshake Bar | 125 | 30m 0s | 0 | 510 |
| `1200180` | **Fruity Milkshake** | Milkshake Bar | 126 | 35m 0s | 0 | 450 |
| `1200181` | **SilverOre** | Mine | 24 | 0s | 0 | 100 |
| `1200182` | **GoldOre** | Mine | 24 | 0s | 0 | 100 |
| `1200183` | **PlatinumOre** | Mine | 24 | 0s | 0 | 100 |
| `1200184` | **CoalOre** | Mine | 33 | 0s | 0 | 100 |
| `1200185` | **IronOre** | Mine | 34 | 0s | 0 | 100 |
| `1200186` | **Mussel** | Mollusc | 1 | 0s | 0 | 7 |
| `1200187` | **Colorful omelet** | Omelet Maker | 77 | 60m 0s | 0 | 100 |
| `1200188` | **Spring omelet** | Omelet Maker | 77 | 40m 0s | 0 | 135 |
| `1200189` | **Rice omelet** | Omelet Maker | 83 | 120m 0s | 0 | 340 |
| `1200190` | **Cheese omelet** | Omelet Maker | 79 | 90m 0s | 0 | 275 |
| `1200191` | **Potato omelet** | Omelet Maker | 87 | 75m 0s | 0 | 160 |
| `1200192` | **Gnocchi** | Pasta Kitchen | 72 | 80m 0s | 0 | 285 |
| `1200193` | **Lasagna** | Pasta Kitchen | 74 | 100m 0s | 0 | 315 |
| `1200194` | **Lobster Pasta** | Pasta Kitchen | 79 | 120m 0s | 0 | 380 |
| `1200195` | **Pasta Carbonara** | Pasta Kitchen | 83 | 150m 0s | 0 | 245 |
| `1200196` | **Spicy spaghetti** | Pasta Kitchen | 87 | 90m 0s | 0 | 345 |
| `1200197` | **Broccoli Mac** | Pasta Kitchen | 83 | 60m 0s | 0 | 205 |
| `1200198` | **MushroomPasta** | Pasta Kitchen | 101 | 75m 0s | 0 | 165 |
| `1200199` | **Raw Pasta** | Pasta Maker | 67 | 15m 0s | 0 | 100 |
| `1200200` | **Rice Noodles** | Pasta Maker | 73 | 20m 0s | 0 | 100 |
| `1200201` | **Fresh Diffuser** | Perfumerie | 110 | 20m 0s | 0 | 210 |
| `1200202` | **Zesty Perfume** | Perfumerie | 113 | 15m 0s | 0 | 230 |
| `1200203` | **Calming Diffuser** | Perfumerie | 116 | 25m 0s | 0 | 100 |
| `1200204` | **Carrot Pie** | Pie Oven | 14 | 60m 0s | 0 | 100 |
| `1200205` | **Bacon Pie** | Pie Oven | 18 | 180m 0s | 0 | 130 |
| `1200206` | **Pumpkin Pie** | Pie Oven | 15 | 120m 0s | 0 | 100 |
| `1200207` | **Apple Pie** | Pie Oven | 28 | 150m 0s | 0 | 160 |
| `1200208` | **Feta Pie** | Pie Oven | 34 | 90m 0s | 0 | 130 |
| `1200209` | **Casserole** | Pie Oven | 36 | 120m 0s | 0 | 220 |
| `1200210` | **Shepherds Pie** | Pie Oven | 39 | 100m 0s | 0 | 170 |
| `1200211` | **Fish Pie** | Pie Oven | 28 | 120m 0s | 0 | 135 |
| `1200212` | **Lemon Pie** | Pie Oven | 67 | 135m 0s | 0 | 265 |
| `1200213` | **Peach Tart** | Pie Oven | 76 | 150m 0s | 0 | 260 |
| `1200214` | **Eggplant Parmesan** | Pie Oven | 99 | 45m 0s | 0 | 265 |
| `1200215` | **Chocolate Pie** | Pie Oven | 65 | 75m 0s | 0 | 350 |
| `1200216` | **Mushroom Pot Pie** | Pie Oven | 97 | 60m 0s | 0 | 100 |
| `1200217` | **Passion Fruit Pie** | Pie Oven | 92 | 50m 0s | 0 | 100 |
| `1200218` | **Asparagus Quiche** | Pie Oven | 49 | 120m 0s | 0 | 180 |
| `1200219` | **Placeholder** | Placeholder | 150 | 20m 0s | 0 | 100 |
| `1200220` | **Popcorn** | Popcorn Pot | 8 | 30m 0s | 0 | 100 |
| `1200221` | **Butter Popcorn** | Popcorn Pot | 16 | 60m 0s | 0 | 100 |
| `1200222` | **Chili Popcorn** | Popcorn Pot | 25 | 120m 0s | 0 | 100 |
| `1200223` | **Chocolate Popcorn** | Popcorn Pot | 44 | 150m 0s | 0 | 145 |
| `1200224` | **Honey Popcorn** | Popcorn Pot | 40 | 90m 0s | 0 | 215 |
| `1200225` | **Snack Mix** | Popcorn Pot | 64 | 45m 0s | 0 | 250 |
| `1200226` | **Apple porridge** | Porridge Bar | 119 | 20m 0s | 0 | 310 |
| `1200227` | **Sweet porridge** | Porridge Bar | 120 | 45m 0s | 0 | 275 |
| `1200228` | **Fresh porridge** | Porridge Bar | 122 | 35m 0s | 0 | 260 |
| `1200229` | **Tea Pot** | Pottery Studio | 94 | 240m 0s | 0 | 130 |
| `1200230` | **Plant pot** | Pottery Studio | 96 | 220m 0s | 0 | 130 |
| `1200231` | **Mug** | Pottery Studio | 99 | 200m 0s | 0 | 125 |
| `1200232` | **Dried Fruit** | Preservation Station | 102 | 180m 0s | 0 | 160 |
| `1200233` | **Pickles** | Preservation Station | 91 | 240m 0s | 0 | 160 |
| `1200234` | **Canned Fish** | Preservation Station | 95 | 220m 0s | 0 | 280 |
| `1200235` | **Kimchi** | Preservation Station | 98 | 300m 0s | 0 | 130 |
| `1200236` | **Guava Compote** | Preservation Station | 104 | 260m 0s | 0 | 250 |
| `1200237` | **GreekSalad** | Salad Bar | 58 | 90m 0s | 0 | 445 |
| `1200238` | **BaconSalad** | Salad Bar | 62 | 105m 0s | 0 | 430 |
| `1200239` | **SeafoodSalad** | Salad Bar | 64 | 120m 0s | 0 | 455 |
| `1200240` | **Pasta Salad** | Salad Bar | 67 | 150m 0s | 0 | 450 |
| `1200241` | **Fruit Salad** | Salad Bar | 82 | 120m 0s | 0 | 355 |
| `1200242` | **Summer Salad** | Salad Bar | 84 | 180m 0s | 0 | 330 |
| `1200243` | **Summer Rolls** | Salad Bar | 78 | 60m 0s | 0 | 190 |
| `1200244` | **VeggieDip** | Salad Bar | 74 | 120m 0s | 0 | 160 |
| `1200245` | **MushroomSalad** | Salad Bar | 89 | 60m 0s | 0 | 130 |
| `1200246` | **Beetroot salad** | Salad Bar | 76 | 45m 0s | 0 | 140 |
| `1200247` | **Coleslaw** | Salad Bar | 75 | 75m 0s | 0 | 280 |
| `1200248` | **Orange Salad** | Salad Bar | 117 | 45m 0s | 0 | 330 |
| `1200249` | **Bean Salad** | Salad Bar | 58 | 60m 0s | 0 | 100 |
| `1200250` | **BLTToast** | Sandwich Bar | 65 | 100m 0s | 0 | 385 |
| `1200251` | **VeggieBagel** | Sandwich Bar | 61 | 40m 0s | 0 | 315 |
| `1200252` | **EggSandwich** | Sandwich Bar | 66 | 80m 0s | 0 | 345 |
| `1200253` | **Honey Toast** | Sandwich Bar | 69 | 60m 0s | 0 | 155 |
| `1200254` | **Goat Cheese Toast** | Sandwich Bar | 92 | 50m 0s | 0 | 180 |
| `1200255` | **Onion melt** | Sandwich Bar | 84 | 90m 0s | 0 | 250 |
| `1200256` | **Cucumber Sandwich** | Sandwich Bar | 79 | 35m 0s | 0 | 275 |
| `1200257` | **PBJ Sandwich** | Sandwich Bar | 71 | 25m 0s | 0 | 400 |
| `1200258` | **Hummus Wrap** | Sandwich Bar | 109 | 30m 0s | 0 | 225 |
| `1200259` | **SoySauce** | Sauce Mixer | 54 | 180m 0s | 0 | 100 |
| `1200260` | **OliveOil** | Sauce Mixer | 60 | 45m 0s | 0 | 165 |
| `1200261` | **Mayonaise** | Sauce Mixer | 62 | 15m 0s | 0 | 220 |
| `1200262` | **Lemon Curd** | Sauce Mixer | 66 | 25m 0s | 0 | 225 |
| `1200263` | **Tomato Sauce** | Sauce Mixer | 69 | 30m 0s | 0 | 135 |
| `1200264` | **Salsa** | Sauce Mixer | 77 | 20m 0s | 0 | 150 |
| `1200265` | **Olive Dip** | Sauce Mixer | 66 | 45m 0s | 0 | 280 |
| `1200266` | **Passion Fruit Sauce** | Sauce Mixer | 100 | 30m 0s | 0 | 170 |
| `1200267` | **Hummus** | Sauce Mixer | 95 | 30m 0s | 0 | 165 |
| `1200268` | **Bean Dip** | Sauce Mixer | 54 | 40m 0s | 0 | 100 |
| `1200269` | **Gift_Box1** | Seasonal | 17 | 10m 0s | 0 | 285 |
| `1200270` | **Gift_Box2** | Seasonal | 17 | 10m 0s | 0 | 420 |
| `1200271` | **Gift_Box3** | Seasonal | 30 | 10m 0s | 0 | 490 |
| `1200272` | **Gift_Box4** | Seasonal | 35 | 10m 0s | 0 | 665 |
| `1200273` | **Easter_egg1** | Seasonal | 17 | 30m 0s | 0 | 100 |
| `1200274` | **Easter_egg2** | Seasonal | 25 | 45m 0s | 0 | 240 |
| `1200275` | **Easter_egg3** | Seasonal | 43 | 60m 0s | 0 | 280 |
| `1200276` | **Easter_egg4** | Seasonal | 54 | 90m 0s | 0 | 295 |
| `1200277` | **Gift_Box1_23** | Seasonal | 17 | 45m 0s | 0 | 180 |
| `1200278` | **Gift_Box2_23** | Seasonal | 25 | 45m 0s | 0 | 340 |
| `1200279` | **Gift_Box3_23** | Seasonal | 43 | 60m 0s | 0 | 345 |
| `1200280` | **Gift_Box4_23** | Seasonal | 70 | 90m 0s | 0 | 350 |
| `1200281` | **Easter_egg1_24** | Seasonal | 17 | 10m 0s | 0 | 285 |
| `1200282` | **Easter_egg2_24** | Seasonal | 20 | 10m 0s | 0 | 500 |
| `1200283` | **Easter_egg3_24** | Seasonal | 35 | 10m 0s | 0 | 395 |
| `1200284` | **Easter_egg4_24** | Seasonal | 55 | 10m 0s | 0 | 395 |
| `1200285` | **Birthday_balloon1_24** | Seasonal | 17 | 15m 0s | 0 | 335 |
| `1200286` | **Birthday_balloon2_24** | Seasonal | 22 | 25m 0s | 0 | 385 |
| `1200287` | **Birthday_balloon3_24** | Seasonal | 35 | 45m 0s | 0 | 665 |
| `1200288` | **Birthday_balloon4_24** | Seasonal | 45 | 45m 0s | 0 | 830 |
| `1200289` | **Halloween_candy1_24** | Seasonal | 17 | 10m 0s | 0 | 135 |
| `1200290` | **Halloween_candy2_24** | Seasonal | 17 | 15m 0s | 0 | 225 |
| `1200291` | **Halloween_candy3_24** | Seasonal | 35 | 20m 0s | 0 | 545 |
| `1200292` | **Halloween_candy4_24** | Seasonal | 50 | 20m 0s | 0 | 630 |
| `1200293` | **Gift_Box1_24** | Seasonal | 20 | 10m 0s | 0 | 435 |
| `1200294` | **Gift_Box2_24** | Seasonal | 25 | 10m 0s | 0 | 425 |
| `1200295` | **Gift_Box3_24** | Seasonal | 45 | 10m 0s | 0 | 610 |
| `1200296` | **Gift_Box4_24** | Seasonal | 60 | 10m 0s | 0 | 530 |
| `1200297` | **Easter_egg1_25** | Seasonal | 17 | 10m 0s | 0 | 220 |
| `1200298` | **Easter_egg2_25** | Seasonal | 20 | 10m 0s | 0 | 350 |
| `1200299` | **Easter_egg3_25** | Seasonal | 30 | 10m 0s | 0 | 725 |
| `1200300` | **Easter_egg4_25** | Seasonal | 45 | 10m 0s | 0 | 610 |
| `1200301` | **Birthday_balloon1_25** | Seasonal | 17 | 10m 0s | 0 | 420 |
| `1200302` | **Birthday_balloon2_25** | Seasonal | 17 | 10m 0s | 0 | 375 |
| `1200303` | **Birthday_balloon3_25** | Seasonal | 20 | 10m 0s | 0 | 350 |
| `1200304` | **Birthday_balloon4_25** | Seasonal | 25 | 10m 0s | 0 | 225 |
| `1200305` | **Birthday_balloon5_25** | Seasonal | 30 | 10m 0s | 0 | 635 |
| `1200306` | **Birthday_balloon6_25** | Seasonal | 35 | 10m 0s | 0 | 645 |
| `1200307` | **Birthday_balloon7_25** | Seasonal | 45 | 10m 0s | 0 | 700 |
| `1200308` | **Birthday_balloon8_25** | Seasonal | 60 | 10m 0s | 0 | 665 |
| `1200309` | **Halloween_candy1_25** | Seasonal | 17 | 10m 0s | 0 | 170 |
| `1200310` | **Halloween_candy2_25** | Seasonal | 17 | 10m 0s | 0 | 140 |
| `1200311` | **Halloween_candy3_25** | Seasonal | 20 | 10m 0s | 0 | 270 |
| `1200312` | **Halloween_candy4_25** | Seasonal | 25 | 10m 0s | 0 | 510 |
| `1200313` | **Gift_Box1_25** | Seasonal | 17 | 10m 0s | 0 | 355 |
| `1200314` | **Gift_Box2_25** | Seasonal | 17 | 10m 0s | 0 | 240 |
| `1200315` | **Gift_Box3_25** | Seasonal | 20 | 10m 0s | 0 | 490 |
| `1200316` | **Gift_Box4_25** | Seasonal | 30 | 10m 0s | 0 | 290 |
| `1200317` | **Halloween_candy5_25** | Seasonal | 30 | 10m 0s | 0 | 300 |
| `1200318` | **Halloween_candy6_25** | Seasonal | 35 | 10m 0s | 0 | 400 |
| `1200319` | **Halloween_candy7_25** | Seasonal | 45 | 10m 0s | 0 | 715 |
| `1200320` | **Halloween_candy8_25** | Seasonal | 60 | 10m 0s | 0 | 465 |
| `1200321` | **Gift_Box5_25** | Seasonal | 50 | 10m 0s | 0 | 565 |
| `1200322` | **Gift_Box6_25** | Seasonal | 75 | 10m 0s | 0 | 400 |
| `1200323` | **Gift_Box7_25** | Seasonal | 80 | 10m 0s | 0 | 865 |
| `1200324` | **Gift_Box8_25** | Seasonal | 85 | 10m 0s | 0 | 520 |
| `1200325` | **Birthday_balloon1_26** | Seasonal | 17 | 10m 0s | 0 | 355 |
| `1200326` | **Birthday_balloon2_26** | Seasonal | 20 | 10m 0s | 0 | 240 |
| `1200327` | **Birthday_balloon3_26** | Seasonal | 35 | 10m 0s | 0 | 490 |
| `1200328` | **Birthday_balloon4_26** | Seasonal | 75 | 10m 0s | 0 | 290 |
| `1200329` | **Birthday_balloon5_26** | Seasonal | 17 | 10m 0s | 0 | 565 |
| `1200330` | **Birthday_balloon6_26** | Seasonal | 20 | 10m 0s | 0 | 400 |
| `1200331` | **Birthday_balloon7_26** | Seasonal | 30 | 10m 0s | 0 | 865 |
| `1200332` | **Birthday_balloon8_26** | Seasonal | 45 | 10m 0s | 0 | 520 |
| `1200333` | **Cotton Shirt** | Sewing Machine | 19 | 45m 0s | 0 | 145 |
| `1200334` | **Wooly Pants** | Sewing Machine | 21 | 90m 0s | 0 | 185 |
| `1200335` | **Violet Dress** | Sewing Machine | 25 | 135m 0s | 0 | 195 |
| `1200336` | **Pillow** | Sewing Machine | 51 | 180m 0s | 0 | 405 |
| `1200337` | **Blanket** | Sewing Machine | 59 | 210m 0s | 0 | 655 |
| `1200338` | **Soothing Pad** | Sewing Machine | 45 | 60m 0s | 0 | 190 |
| `1200339` | **SilverBar** | Smelter | 24 | 480m 0s | 0 | 100 |
| `1200340` | **GoldBar** | Smelter | 25 | 720m 0s | 0 | 105 |
| `1200341` | **PlatinumBar** | Smelter | 25 | 960m 0s | 0 | 120 |
| `1200342` | **CoalBar** | Smelter | 33 | 360m 0s | 0 | 100 |
| `1200343` | **IronBar** | Smelter | 34 | 420m 0s | 0 | 100 |
| `1200344` | **GreenSmoothie** | Smoothie Mixer | 66 | 45m 0s | 0 | 190 |
| `1200345` | **BerrySmoothie** | Smoothie Mixer | 64 | 75m 0s | 0 | 325 |
| `1200346` | **YogurtSmoothie** | Smoothie Mixer | 70 | 60m 0s | 0 | 210 |
| `1200347` | **MixedSmoothie** | Smoothie Mixer | 88 | 30m 0s | 0 | 300 |
| `1200348` | **Cocoa smoothie** | Smoothie Mixer | 100 | 40m 0s | 0 | 305 |
| `1200349` | **PlumSmoothie** | Smoothie Mixer | 102 | 35m 0s | 0 | 310 |
| `1200350` | **Cucumber Smoothie** | Smoothie Mixer | 70 | 40m 0s | 0 | 160 |
| `1200351` | **SesameSmoothie** | Smoothie Mixer | 93 | 45m 0s | 0 | 185 |
| `1200352` | **TropicalSmoothie** | Smoothie Mixer | 104 | 40m 0s | 0 | 285 |
| `1200353` | **Lobster Soup** | Soup Kitchen | 46 | 150m 0s | 0 | 365 |
| `1200354` | **Tomato Soup** | Soup Kitchen | 47 | 90m 0s | 0 | 285 |
| `1200355` | **Fish Soup** | Soup Kitchen | 53 | 180m 0s | 0 | 175 |
| `1200356` | **Pumpkin Soup** | Soup Kitchen | 49 | 120m 0s | 0 | 235 |
| `1200357` | **Noodle Soup** | Soup Kitchen | 73 | 120m 0s | 0 | 260 |
| `1200358` | **Onion Soup** | Soup Kitchen | 72 | 150m 0s | 0 | 195 |
| `1200359` | **PotatoSoup** | Soup Kitchen | 78 | 150m 0s | 0 | 155 |
| `1200360` | **PepperSoup** | Soup Kitchen | 81 | 60m 0s | 0 | 260 |
| `1200361` | **Broccoli Soup** | Soup Kitchen | 87 | 75m 0s | 0 | 140 |
| `1200362` | **MushroomSoup** | Soup Kitchen | 104 | 80m 0s | 0 | 105 |
| `1200363` | **Cabbage Soup** | Soup Kitchen | 65 | 90m 0s | 0 | 160 |
| `1200364` | **Asparagus Soup** | Soup Kitchen | 51 | 60m 0s | 0 | 150 |
| `1200365` | **Lamb Soup** | Soup Kitchen | 46 | 120m 0s | 0 | 105 |
| `1200366` | **PeanutBag** | Squirrel Nest | 62 | 0s | 0 | 215 |
| `1200367` | **Chickpea Stew** | Stew Pot | 106 | 90m 0s | 0 | 170 |
| `1200368` | **Winter Stew** | Stew Pot | 112 | 140m 0s | 0 | 175 |
| `1200369` | **Chili Stew** | Stew Pot | 109 | 120m 0s | 0 | 220 |
| `1200370` | **Brown_Sugar** | Sugar Mill | 7 | 20m 0s | 0 | 100 |
| `1200371` | **White Sugar** | Sugar Mill | 13 | 40m 0s | 0 | 100 |
| `1200372` | **Syrup** | Sugar Mill | 18 | 90m 0s | 0 | 100 |
| `1200373` | **SushiRoll** | Sushi Bar | 56 | 60m 0s | 0 | 290 |
| `1200374` | **LobsterSushi** | Sushi Bar | 59 | 60m 0s | 0 | 380 |
| `1200375` | **EggRoll** | Sushi Bar | 63 | 120m 0s | 0 | 330 |
| `1200376` | **Big sushi roll** | Sushi Bar | 76 | 90m 0s | 0 | 385 |
| `1200377` | **Rice Ball** | Sushi Bar | 110 | 45m 0s | 0 | 275 |
| `1200378` | **Taco** | Taco Kitchen | 77 | 45m 0s | 0 | 235 |
| `1200379` | **Fish Taco** | Taco Kitchen | 79 | 90m 0s | 0 | 235 |
| `1200380` | **Quesadilla** | Taco Kitchen | 82 | 60m 0s | 0 | 145 |
| `1200381` | **Nachos** | Taco Kitchen | 87 | 75m 0s | 0 | 260 |
| `1200382` | **Spicy Bean Taco** | Taco Kitchen | 77 | 120m 0s | 0 | 270 |
| `1200383` | **Green Tea** | Tea Stand | 80 | 30m 0s | 0 | 145 |
| `1200384` | **Milk Tea** | Tea Stand | 81 | 45m 0s | 0 | 115 |
| `1200385` | **Honey Tea** | Tea Stand | 83 | 40m 0s | 0 | 185 |
| `1200386` | **Lemon Tea** | Tea Stand | 86 | 20m 0s | 0 | 145 |
| `1200387` | **Orange Tea** | Tea Stand | 89 | 40m 0s | 0 | 150 |
| `1200388` | **Ice Tea** | Tea Stand | 92 | 30m 0s | 0 | 150 |
| `1200389` | **MintTea** | Tea Stand | 97 | 35m 0s | 0 | 155 |
| `1200390` | **GingerTea** | Tea Stand | 88 | 30m 0s | 0 | 100 |
| `1200391` | **Pomegranate Tea** | Tea Stand | 107 | 35m 0s | 0 | 185 |
| `1200392` | **Chamomile Tea** | Tea Stand | 100 | 20m 0s | 0 | 100 |
| `1200393` | **Plain Waffles** | Waffle Maker | 114 | 25m 0s | 0 | 120 |
| `1200394` | **Breakfast Waffles** | Waffle Maker | 119 | 45m 0s | 0 | 255 |
| `1200395` | **Berry Waffles** | Waffle Maker | 114 | 35m 0s | 0 | 360 |
| `1200396` | **Chocolate Waffles** | Waffle Maker | 117 | 40m 0s | 0 | 380 |
| `1200397` | **White Chocolate Blueberry Waffle** | Waffle Maker | 118 | 42m 0s | 0 | 400 |
| `1200398` | **Fried rice** | Wok Kitchen | 69 | 60m 0s | 0 | 120 |
| `1200399` | **Tofu stir fry** | Wok Kitchen | 89 | 75m 0s | 0 | 185 |
| `1200400` | **Spicy fish** | Wok Kitchen | 79 | 90m 0s | 0 | 325 |
| `1200401` | **Peanut noodles** | Wok Kitchen | 86 | 45m 0s | 0 | 400 |
| `1200402` | **Lamb Stir Fry** | Wok Kitchen | 69 | 120m 0s | 0 | 160 |
| `1200403` | **Plain Yoghurt** | Yoghurt Maker | 103 | 120m 0s | 0 | 140 |
| `1200404` | **Strawberry Yoghurt** | Yoghurt Maker | 105 | 40m 0s | 0 | 315 |
| `1200405` | **Tropical Yoghurt** | Yoghurt Maker | 109 | 60m 0s | 0 | 270 |
| `1200406` | **Breakfast Bowl** | Yoghurt Maker | 119 | 50m 0s | 0 | 360 |