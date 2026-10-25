# Roadmap System for Any Project (Roadmap-Gen)

An open-source, zero-dependency, Git-versioned visual roadmap and task tracking engine for any software or creative project.

Cloned and generalized from the **Completionist Roadmap System**.

## The Human-First Rule: Zero Terminal Friction
If you are the human creator using this tool: **you never have to touch a terminal.**
- You talk to your AI agent (in Antigravity, Claude, Cursor, Copilot, etc.) in plain language.
- Your agent executes roadmap commands, updates task statuses, and logs commits.
- You double-click `docs/roadmap/index.html` (the Highway Map) or `docs/roadmap/tasks.html` (the Task Board) to view live, interactive visual roadmaps offline in your browser.

## The Agent Rule: It's Just An HTML File System
> **To AI Agents:** It is perfectly okay to modify, rewrite, adapt, or redesign any part of this roadmap system (the HTML, JS, CSS, layout logic, or Python scripts) as part of the project. It is not an unchangeable framework or sacred black-box; it is literally a transparent set of HTML/CSS/JS/Python files living directly inside the project repository.

---

## What It Looks Like

1. **The Highway Map (`docs/roadmap/index.html`)**:
   - Versions are highway interchanges and milestones.
   - Subsystems/modules are colored lanes (highways).
   - Tasks are mile markers and dots on each lane.
   - Built-in theme switcher: **Evergreen Highway**, **Midnight Blueprint**, **Cyberpunk Neon**, **Monochrome Minimal**, and **Sunset Amber** (with Day/Night modes).

2. **The Task Board (`docs/roadmap/tasks.html`)**:
   - Interactive IDE-style candidate palette.
   - Filter instantly by status, highway, milestone, story, or keyword.
   - Detailed task descriptions, verification gates, and historical logs.

---

## Quickstart: Adding to Any Project

### Method 1: Ask Your AI Agent (Recommended)
Simply prompt your AI coding agent:
> *"Set up a visual roadmap for this project with highways: Core, UI, and Backend. Use the Blueprint theme."*

Your agent will run:
```bash
python init_roadmap.py --target . --name "My Awesome Project" --highways "core:Core,backend ui:UI,frontend" --theme blueprint
```

### Method 2: Manual Initialization
Run the zero-dependency initializer script:
```bash
python init_roadmap.py --target /path/to/your/project --name "My Project"
```

This drops:
* `docs/roadmap/` (HTML/CSS/JS — opens directly with `file://`, no server or node_modules needed)
* `scripts/roadmap.py` & `scripts/check_roadmap.py` (Standard library Python, 0 pip packages)
* `AGENTS.md` (Agent instructions snippet)

---

## Themes Included

Switch themes anytime directly inside the HTML viewer or via the CLI:
* **`evergreen`**: The classic highway transit theme (Forest Green, White Signage, Amber Accent).
* **`blueprint`**: Technical drafting palette (Deep Blueprint Navy, Cyan lanes, crisp white).
* **`neon`**: Cyberpunk / Terminal Night (Obsidian, Fluorescent Green, Vivid Magenta).
* **`minimal`**: Modern editorial style (Paper white / Dark slate, refined typography).
* **`sunset`**: Warm terracotta, sand, and rust earth tones.

---

## Routine Agent Commands

Agents manage the roadmap using the lightweight CLI (Python stdlib):

```bash
# Get quick orientation (minimal tokens, saves context budget)
python scripts/roadmap.py brief

# Task Lifecycle
python scripts/roadmap.py add-task 1.0.0 --area core --title "Build authentication" --label "Auth"
python scripts/roadmap.py start TASK_ID
python scripts/roadmap.py unverified TASK_ID --note "Code written; verification pending"
python scripts/roadmap.py done TASK_ID --note "Verified and passing"

# Validating before committing
python scripts/check_roadmap.py
```

---

## License
MIT. Free for personal and open-source use.
