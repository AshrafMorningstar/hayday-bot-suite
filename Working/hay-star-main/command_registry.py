#!/usr/bin/env python3
"""
=============================================================================
Hay Star - Central Command Registry & Alias System
Author: Ashraf Morningstar
Repository: https://github.com/AshrafMorningstar/hay-star
License: MIT
=============================================================================
Maps every command (full name and 1-3 letter shortcut) to its handler.
Provides search, lookup, and formatted listing for all available commands.
=============================================================================
"""

import sys

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# =============================================================================
#  MASTER COMMAND REGISTRY
#  Each entry: (shortcut, full_name, description, category)
# =============================================================================

COMMANDS = [
    # --- Farming Commands ---
    ("hv",  "harvest",          "Harvest all ripe crops from fields",                     "Farming"),
    ("pl",  "plant",            "Plant crops in all empty fields (pl <crop_id>)",         "Farming"),
    ("ca",  "collect_animals",  "Collect eggs, milk, bacon, wool from animals",           "Farming"),
    ("fa",  "feed_animals",     "Feed all animals with correct matched feed",             "Farming"),
    ("cm",  "collect_machines", "Collect finished products from all machines",             "Farming"),
    ("pm",  "produce_machines", "Queue recipes in Bakery, Dairy, Sugar Mill, etc.",        "Farming"),
    ("cf",  "collect_fruits",   "Harvest apples, berries, cherries from trees/bushes",    "Farming"),
    ("cal", "collect_all",      "MASTER COLLECT: crops + animals + machines + fruits",     "Farming"),
    ("ch",  "chop_all",         "Chop dead trees & bushes, collect fruits, request help",  "Farming"),
    ("wp",  "wake_pets",        "Wake up and feed all pets & sanctuary animals with Wheat", "Farming"),
    ("nfp", "feed_pets",        "Native auto-feed all pets with Wheat (0-click)",           "Native"),

    # --- Shop & Economy ---
    ("ss",  "shop_sell",        "Sell items in roadside shop (ss <id> <slot> <count> <price> <ad>)", "Shop"),
    ("cc",  "collect_coins",    "Collect all coins from sold roadside shop crates",        "Shop"),
    ("ad",  "ad_status",        "Check newspaper ad cooldown timer",                       "Shop"),

    # --- Navigation ---
    ("j",   "jump",             "Teleport camera (j shop/farm/animals/mine/boat/town)",    "Navigation"),

    # --- Automation ---
    ("af",  "auto_farm",        "Full loop: harvest→plant→sell→collect (continuous)",       "Automation"),
    ("ma",  "master_auto",      "13-subsystem autonomous farming loop",                    "Automation"),
    ("mc",  "master_cycle",     "Complete 11-step master farm loop (continuous)",           "Automation"),
    ("mr",  "master_rotate",    "Multi-account auto-switching master farm loop",           "Automation"),
    ("rc",  "auto_heal",        "Auto-heal: dismiss popups, reconnect & verify native engine", "Automation"),
    ("x",   "stop",             "Emergency stop all automation",                           "Automation"),

    # --- Mining & Fishing ---
    ("mn",  "mine",             "Smart mining with diamond target & tool priority",         "Mining"),
    ("fh",  "fishing",          "Fishing lake: lures, catch fish, lobsters, nets",          "Fishing"),

    # --- Newspaper & Maintenance ---
    ("sn",  "sniper",           "Newspaper sniper: browse & buy expansion materials",       "Newspaper"),
    ("mt",  "maintenance",      "Daily chores: mail, mystery box, wheel, farm pass",        "Maintenance"),

    # --- Account & Config ---
    ("as",  "account_switch",   "Switch to a different account profile",                   "Account"),
    ("cr",  "config_reload",    "Reload farm config from Assest/configs/farm/loll.json",   "Config"),

    # --- Native & Direct Engine ---
    ("ln",  "loadnative",       "Load ARM64 C++ native injection engine into game",        "Native"),
    ("nf",  "nfields",          "Scan farm & locate all crop field coordinate addresses",  "Native"),
    ("np",  "nplant",           "Native plant crops: np <crop_id> (e.g. np 400001)",       "Native"),
    ("nh",  "nharvest",         "Native harvest all ready crops across all fields",        "Native"),
    ("ns",  "nsell",            "Native sell: ns <start> <slots> <price> <ad> <item_id>",  "Native"),
    ("nfa", "nfarm",            "Native autonomous farm loop with countdown timers",       "Native"),
    ("db",  "dashboard",        "Open interactive master control dashboard menu",          "Utility"),
    ("all", "auto",             "Run full autonomous master cycle pipeline",               "Automation"),

    # --- Utilities ---
    ("s",   "search",           "Search item by name or ID (s bread, s 1300082)",           "Utility"),
    ("h",   "help",             "Show all commands with shortcuts",                        "Utility"),
    ("ex",  "exec_cmd",         "Execute raw vtable memory command",                       "Utility"),
    ("ids", "list_ids",         "Show Global ID architecture summary",                     "Utility"),
    ("st",  "status",           "Show bot status, cycle count, uptime",                    "Utility"),
    ("al",  "list_accounts",    "List all available account profiles",                     "Utility"),
    ("tst", "test",             "Run diagnostic test suite",                               "Utility"),
]

# Build lookup dictionaries
_by_shortcut = {}
_by_fullname = {}
_all_aliases = {}  # Maps every possible input to the canonical full name

for shortcut, fullname, description, category in COMMANDS:
    entry = {
        "shortcut": shortcut,
        "fullname": fullname,
        "description": description,
        "category": category,
    }
    _by_shortcut[shortcut] = entry
    _by_fullname[fullname] = entry
    _all_aliases[shortcut] = fullname
    _all_aliases[fullname] = fullname
    # Also add underscore-free versions
    _all_aliases[fullname.replace("_", "")] = fullname


def resolve_command(user_input):
    """
    Resolve any user input (shortcut or full name) to the canonical command name.
    Returns (full_name, entry_dict) or (None, None) if not found.
    """
    key = user_input.strip().lower().split()[0] if user_input else ""
    if key in _all_aliases:
        fullname = _all_aliases[key]
        return fullname, _by_fullname[fullname]
    return None, None


def search_commands(query):
    """Search commands by partial name or description match."""
    query = query.strip().lower()
    results = []
    for shortcut, fullname, description, category in COMMANDS:
        if (query in shortcut.lower() or
            query in fullname.lower() or
            query in description.lower() or
            query in category.lower()):
            results.append((shortcut, fullname, description, category))
    return results


def get_all_commands():
    """Return the full command list."""
    return COMMANDS


def print_all_commands():
    """Print a beautifully formatted command reference table."""
    print()
    print("=" * 78)
    print("  🌾 HAY STAR — COMPLETE COMMAND REFERENCE (Shortcuts + Full Names)")
    print("=" * 78)

    current_category = None
    for shortcut, fullname, description, category in COMMANDS:
        if category != current_category:
            current_category = category
            print(f"\n  ┌─── {category.upper()} {'─' * (60 - len(category))}")

        print(f"  │ {shortcut:<4} │ {fullname:<20} │ {description}")

    print(f"\n  └{'─' * 76}")
    print()
    print("  TIP: Type the shortcut OR the full command name. Both work!")
    print("  TIP: Use 's <query>' to search items by name or ID.")
print_commands_table = print_all_commands


def print_search_results(query):
    """Search and print matching commands."""
    results = search_commands(query)
    print(f"\n  Search results for '{query}': ({len(results)} matches)")
    print("  " + "-" * 65)
    if not results:
        print("  No matching commands found.")
    else:
        for shortcut, fullname, description, category in results:
            print(f"  {shortcut:<4} │ {fullname:<20} │ {description}")
    print("  " + "-" * 65 + "\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        # Try to resolve as command first
        fullname, entry = resolve_command(query)
        if entry:
            print(f"\n  Command: {entry['fullname']}")
            print(f"  Shortcut: {entry['shortcut']}")
            print(f"  Category: {entry['category']}")
            print(f"  Description: {entry['description']}\n")
        else:
            print_search_results(query)
    else:
        print_all_commands()
