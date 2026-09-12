# 📁 Project Logging Rule — Always On

Whenever you begin, continue, or finish **any** work task — no matter how small — you **MUST** create and maintain a dedicated logging folder inside the workspace root. Follow every rule below without exception.

---

## 1. Folder Structure

Create a folder named **`project-logs/`** at the root of the workspace (if it does not already exist). Inside it, always maintain the following four files:

```
project-logs/
├── work.md        ← Work Journal      (what was done, what's next, how it was done)
├── decision.md    ← Decision Log      (every decision made, why, alternatives, impact)
├── progress.md    ← Progress Log      (checklist, commands run, prompts received, % complete)
└── extras.md      ← Extras & Changes  (bonus steps, change notes, gotchas, build narrative)
```

> **Rule:** Create ALL four files immediately at the start of the very first task. Never skip this step, even for trivial requests.

---

## 2. `work.md` — Work Journal

**Purpose:** A running journal of everything that has been done and what is planned next.

Every time you do any work, update `work.md` with a new dated section containing:

- **Session date & time** — in ISO 8601 format (e.g., `2026-09-10T18:30:00-07:00`).
- **What was done this session** — a bullet list of every action taken:
  - Files created or edited
  - Commands run
  - Features implemented
  - Bugs fixed
  - Configurations changed
- **Current status** — a short sentence describing the current state of the project.
- **What is planned next** — a bullet list of the next steps to be taken.
- **How the work was approached** — a brief explanation of the method, pattern, or reasoning used to carry out the work.

### Example Entry

```markdown
## Session — 2026-09-10T18:30:00-07:00

### What Was Done
- Created `index.html` with base HTML structure
- Added CSS reset and global typography styles
- Ran `npm install` to install dependencies

### Current Status
Project scaffold is complete. Core UI layout is ready.

### What Is Planned Next
- Build the navigation component
- Add routing logic
- Connect to the backend API

### How It Was Approached
Used a mobile-first approach, starting with semantic HTML before adding styles.
```

---

## 3. `decision.md` — Decision Log

**Purpose:** Records every important design, architectural, or implementation decision made during the work.

Every time you make a significant decision, add an entry to `decision.md` with:

- **Decision title** — a short descriptive heading (e.g., `## Use React Router over Next.js`).
- **What was decided** — a clear statement of the choice made.
- **Why it was needed** — the problem or requirement that triggered this decision.
- **Alternatives considered** — any other options that were evaluated (and why they were rejected).
- **Steps taken to arrive at the decision** — the reasoning process used.
- **Impact** — what this decision affects in the project (files, architecture, performance, etc.).

### Example Entry

```markdown
## Decision: Use Vanilla CSS instead of Tailwind

- **Decided:** Use plain CSS with custom properties for all styling.
- **Why needed:** The project requires full design control and no build-tool dependency.
- **Alternatives considered:** TailwindCSS (rejected — adds build complexity), Bootstrap (rejected — too opinionated).
- **Steps taken:** Reviewed project scope, assessed team familiarity, evaluated bundle size impact.
- **Impact:** All component files use `.css` files; no utility class framework is loaded.
```

---

## 4. `progress.md` — Progress & Process Log

**Purpose:** Tracks measurable progress, every command run, and all prompts/instructions received from the user.

After every session or meaningful milestone, update `progress.md` with:

- **What has been created so far** — a checklist of all files, components, features, and assets:
  - `- [x]` for completed items
  - `- [ ]` for pending items
- **Commands executed** — every shell/terminal command run, with a one-line description of its purpose.
- **Prompts & instructions received** — a record of what the user asked for (paraphrased or quoted), preserving the full context of the conversation.
- **Overall completion percentage** — an honest estimate of how far along the project is (e.g., `45% complete`).

### Example Entry

```markdown
## Progress Update — 2026-09-10T18:30:00-07:00

### Files & Features Created
- [x] `index.html` — base HTML scaffold
- [x] `styles/main.css` — global CSS reset and tokens
- [ ] `components/Navbar.js` — navigation component
- [ ] `pages/Home.js` — home page

### Commands Executed
| Command | Purpose |
|---------|---------|
| `npm install` | Install all project dependencies |
| `npm run dev` | Start the local development server |

### Prompts & Instructions Received
1. "Create a landing page with a hero section and a contact form."
2. "Make the design dark mode with glassmorphism effects."

### Overall Completion
**35% complete** — Scaffold and styles done; components and pages pending.
```

---

## 5. `extras.md` — Extra Steps & Change Notes

**Purpose:** Documents bonus context, extra implementation steps, and any changes made beyond the core user request.

Use `extras.md` to record:

- **Extra implementation steps** — steps taken beyond the direct user request:
  - Performance optimizations
  - Accessibility improvements (e.g., ARIA labels, keyboard nav)
  - Additional error handling or validation
  - Security hardening
- **Changes made** — a diff-style summary of what changed compared to the original state, and why.
- **Gotchas & notes** — tricky parts, edge cases, or things to watch out for in the future.
- **How the program/feature was built** — a narrative walkthrough of the creation process, useful for someone reading the code cold for the first time.

### Example Entry

```markdown
## Extras — 2026-09-10T18:30:00-07:00

### Extra Steps Taken
- Added `aria-label` to all icon buttons for screen reader support (not requested, but important).
- Added `loading="lazy"` to all images to improve initial page load.
- Added a `robots.txt` and `sitemap.xml` for basic SEO.

### Changes Made
- **CHANGED:** Switched font from `Roboto` to `Inter` — Inter has better legibility at small sizes.
- **ADDED:** `manifest.json` — makes the app installable as a PWA.
- **REMOVED:** Unused `legacy.css` file that was causing style conflicts.

### Gotchas & Notes
- The CSS `backdrop-filter` property does not work in Firefox without the `--MOZ` flag.
- The API rate limit is 100 requests/minute; add caching if traffic grows.

### How It Was Built
Started by scaffolding the HTML structure, then applied a dark-mode color system using CSS custom properties.
Components were built bottom-up: atoms first (buttons, inputs), then molecules (cards, forms), then pages.
```

---

## 6. Enforcement Rules

These rules are **non-negotiable** and must be followed at all times:

1. **Create the folder and files at the very start of any task.** Do not wait until work is finished.
2. **Update all four files at the end of every session or significant step.** Never leave them stale.
3. **All files must use clear Markdown formatting** — headings, bullet lists, code blocks, and tables where appropriate.
4. **Never delete or overwrite previous entries.** Always append new sessions below existing content so the full history is preserved.
5. **If a file already exists, continue from where it left off** — add a new dated section at the bottom of the file.
6. **Record every user prompt.** Even if the request is tiny (e.g., "fix the button color"), log it in `progress.md`.
7. **Record every command.** Every shell/terminal command run during the task must be logged in `progress.md`.
8. **Record every decision.** Any time a choice is made between two or more approaches, it must be logged in `decision.md`.
9. **The folder name is always `project-logs/`.** It must always live at the root of the workspace.
10. **Failure to maintain these logs is a critical rule violation.** This logging system is always active, for every task, without exception.