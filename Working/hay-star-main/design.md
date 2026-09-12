# Interface Specification Document — Hay Star

## Design Philosophy
Hay Star embraces a realistic, minimalist, high-contrast CLI & terminal design philosophy. Output formatting prioritizes clarity, immediate readability, and zero clutter. Tacky neon, generic ASCII dumps, or oversaturated rainbow logs are strictly avoided in favor of curated ANSI accents (Cyan headers, Green success indicators, Yellow warnings, Red alerts).

## Color Hierarchy
- **Header & Title Banners:** Cyan Bold (`\033[96m\033[1m`)
- **Success & Passed Checks:** Green (`\033[92m`)
- **Warnings & Dry-Run Notices:** Yellow (`\033[93m`)
- **Critical Errors & Failures:** Red (`\033[91m`)
- **Subtext & Metadata:** Dim Gray (`\033[2m`)

## Terminal Dashboard Components
1. **Master Control Menu (`launcher.py`):**
   - Numbered options [1-8] with highlighted action verbs.
   - Clean dividers with 78-character width matching standard Windows console windows.
2. **Command Reference Table (`command_registry.py`):**
   - Categorized blocks (FARMING, SHOP, NAVIGATION, AUTOMATION, UTILITY).
   - Fixed-width column alignment (`shortcut` 4ch, `fullname` 20ch, description).
3. **Live REPL Prompt:**
   - Minimalist prompt: `hay-star > `
   - Instant response feedback with timestamped logging tags: `HH:MM:SS.mmm [tag]: message`.
4. **Diagnostic Status Table (`install.py`):**
   - Standardized `[ PASS ]`, `[ WARN ]`, `[ FAIL ]` tags with 36-character check names and details.
