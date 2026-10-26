#!/usr/bin/env python3
"""Roadmap-Gen Initializer: Zero-friction, agent-friendly project roadmap scaffolder.

Usage:
    python init_roadmap.py --target /path/to/project --name "My Awesome Project"
    python init_roadmap.py --target . --name "App" --theme blueprint --highways "core:backend,api ui:web,mobile"

No external packages or pip dependencies required (Python standard library only).
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE_DIR = ROOT / "template"

AGENT_INSTRUCTIONS = """
## The Roadmap System: Keep It Current (Required for Agents)

`docs/roadmap/roadmap.js` is the single source of truth. It defines `window.ROADMAP_DATA = { ... };` (or `window.PROJECT_ROADMAP` / `window.COMPLETIONIST_ROADMAP`) with strict JSON after the assignment. The two plain HTML pages work directly from disk: `index.html` is the Release Atlas and `tasks.html` is the Task Board. Nothing requires a local web server or build process.

**Versions are destinations. Tasks are roadwork.** Several tasks share a `targetRelease`. Completing a task never creates a release, allocates a patch number, or tags Git. Every change, including documentation, fixes, and refactoring, is a task.

**Every commit updates the roadmap. No exceptions.** Stage `roadmap.js` with at least a new entry at the top of `log` describing the commit, and run `python scripts/check_roadmap.py` before committing. It must print `roadmap ok`.

---

### Critical Directive: The Human User Does NOT Touch The Terminal
The human creator using this project will not run terminal commands.
- **You (the AI agent)** own all CLI interactions (`python scripts/roadmap.py ...`, git commits, checks).
- When reporting progress or completing work, give the human user clickable file links to open the visual roadmap directly in their browser from disk:
  - [Open Highway Map Atlas](file:///docs/roadmap/index.html)
  - [Open Task Board](file:///docs/roadmap/tasks.html)

---

### Full Permission to Modify & Rewrite
> **To all AI Agents:** It is **perfectly okay to rewrite, adapt, modify, or extend** the entire roadmap system (the HTML files, CSS styling, JavaScript layout algorithms, data model, or Python scripts) as part of the project.
> It is **not** an untouchable external black-box package. It is literally just an HTML/JS/CSS/Python file system living transparently in your repository. If the project needs new lanes, different visualization rules, custom cards, or special filters--hack on it directly!

---

### Model and Routine Edits
- **Schema 4** has flat `tasks`, `releases`, `releasePlans`, `highways`, and one `activeRelease` (or null if no future destination remains).
- **`releases`** contains actual shipped versions and coherent planned destinations, in ascending version order, with shipped versions first. Preserve genuine shipped records, tags, and historical writing.
- **`releasePlans[VERSION]`** stores the destination title, goal, `done_when`, and broad `scope`: `contained`, `medium`, or `large`.
- **Tasks** have a stable internal `id`, full `title`, `status`, `area`, `targetRelease`, `stories`, optional `refs`/`notes`, optional concise `label`, and optional local numeric `stage`. No task has a `version`. New IDs are descriptive slugs (e.g. `build-jwt-auth`). Never reuse or renumber IDs.
- A done task can have a `completed` date. `shippedIn` names the actual released version carrying its work; absence means not yet shipped. Completed work and shipped software are different facts.
- **Task array order** controls local order. Stages are local sequence information; reorder tasks without renumbering IDs or releases. Retargeting logs the old and new destination, preserves the task, and removes its old local stage.

---

### Strict Task Lifecycle & Statuses
Every task flows through a strict state machine:
* `todo`: Queued work planned for a destination.
* `next`: The immediate next task queued for execution.
* `doing`: Active implementation is underway right now.
* `unverified`: **Implementation is complete in code, but real-world or owner verification is pending** (e.g., human checking in browser/app, running hardware, manual test flow). *Unverified tasks block shipping until verified!*
* `blocked`: Work is blocked by an external dependency or decision.
* `done`: Required verification is complete (or no verification was required). Record verification notes and results, then move `unverified` to `done`.
* `dropped`: Work intentionally cancelled or superseded (appears as faded spur on map).

When starting work, mark the task `doing`. When implementation is complete in code but verification remains, mark it `unverified`. Once verification criteria are met (or none are required), mark it `done`; the helper promotes the next waiting task when appropriate. Keep story links, planned release writing, decisions, and risks current. Add new discoveries as tasks; do not make software versions for them. Set `updated` to today's date and prepend a log entry with every change.

---

### Labels, Sizing & The Map (How to Write Tasks)
- **Every task gets a short `--label`:** Use 2-4 words, about 28 characters at most, **naming the thing and not the action** ("Fuzzy Index", not "Build the fuzzy index"; "JWT Auth", not "Implement the JWT authentication"). Dots on the map display this label. Without one, the map falls back to the full title trimmed with an ellipsis.
- **Task Titles:** The full `--title` should clearly and concisely describe the exact capability or fix being delivered.
- **How the map draws work:** Each task is a dot on its highway lane. Shipped tasks are grouped under the release that shipped them, with the release number as a small caption under the first dot. A run of dots between two signs shows how much work a release took. Major and minor releases are signs.
- **Never create a release to make a dot appear:** A task is already visible as a dot on the highway.
- **`--area` chooses the lane:** The areas-to-highway mapping is defined in `highways` in `roadmap.js`, so pick the area on purpose (e.g., `core`, `ui`, `infra`).
- **`shippedIn` places a done task in history:** The `release` command sets it automatically. Do not set it by hand.

---

### Session Start & Token Efficiency (Never Read Full JSON)
**Start every session with `python scripts/roadmap.py brief`.** Generated briefs are lightweight markdown files ignored by Git; never edit them directly.
Use the CLI helper instead of dumping the raw ~200KB `roadmap.js` into context:
- **Minimal (`--level minimal` or default):** Current `doing`, `unverified`, `next`, and `blocked` work with IDs, target releases, areas, and local stages.
- **Medium (`--level medium`):** Current goals and criteria, all remaining active-release work with full notes, recent completions, and latest shipped releases.
- **Maximum (`--level maximum`):** Lossless snapshot of every field and historical log.

---

### Routine CLI Commands Cheat Sheet
```bash
# 1. Inspect active work with minimal tokens (start of session)
python scripts/roadmap.py brief

# 2. Add a new task (always provide --area and short --label)
python scripts/roadmap.py add-task 0.1.0 --area core --title "Build authentication middleware" --label "Auth Middleware" --stories 1

# 3. Start working on a task
python scripts/roadmap.py start TASK_ID

# 4. Mark implementation complete in code, awaiting verification
python scripts/roadmap.py unverified TASK_ID --refs "src/auth.py" --note "Middleware implemented; user checking in browser."

# 5. Mark task verified and done
python scripts/roadmap.py done TASK_ID --refs "src/auth.py,tests/test_auth.py" --note "Tested token validation with positive and negative cases."

# 6. Reorganize or retarget tasks
python scripts/roadmap.py move TASK_ID --before OTHER_ID
python scripts/roadmap.py retarget TASK_ID 0.2.0
python scripts/roadmap.py drop TASK_ID --reason "Superseded by OAuth provider integration."

# 7. Log changes
python scripts/roadmap.py log "Integrated authentication middleware and updated test suite."

# 8. Pre-commit validation check
python scripts/check_roadmap.py
```

`add-task` optionally accepts `--id`, `--before`, and `--stage`. All edits validate before writing; rejected edits leave the file unchanged. Serialization is deterministic.

---

### Shipping Releases & Proportional Writing Rules
PATCH means a real small fix, regression, polish, or maintenance release. MINOR means a coherent capability. MAJOR means a major product, interface, or architecture expansion. Use judgment, not task counts. Do not reserve patch numbers for future work. Neither a commit, merge, nor the last completed task automatically ships a release.

A release becomes ready when its required work is complete or explicitly dropped. Ship only after validation, using a separate release action:
- **For an existing destination:**
  ```bash
  python scripts/roadmap.py release 0.2.0 --validated "Integration checks passed." --text "Retrospective release paragraph..."
  ```
- **For a concrete patch release:**
  ```bash
  python scripts/roadmap.py release 0.1.1 --tasks TASK_ID,OTHER_ID --title "Fix token expiry bug" --text "Fixed race condition in token expiration check." --validated "Regression test passed."
  ```
- **For a major release:** Major release writing can be supplied with `--essay-file PATH`, with blank lines separating paragraphs. Rewrite planned writing to describe what actually shipped.

#### Proportional Writing (Strictly Enforced by `check_roadmap.py`):
The checker strictly validates word counts and sentence structures for both planned and shipped releases:
- **PATCH:** Exactly **one sentence**, at most **50 words**, ending in punctuation.
- **MINOR:** Exactly **one paragraph** of **50 to 220 words**, containing at least two sentences.
- **MAJOR:** An essay of **at least 4 paragraphs** and **at least 450 words**.

The helper records shipping and moves `activeRelease` to the next destination; it never tags, pushes, or publishes. Tag `vX.Y.Z` on Git as a separate authorized shipping step.

---

### Working Agreements With The Human
1. **Plain English, Zero Jargon:** Explain updates simply. Name real concepts (e.g. a specific file or function) in a phrase, but skip internal minutiae.
2. **Before You Change Code:** State in 2-3 sentences what you plan to change and why. If there is a real design or scope choice, present 1-2 distinct options and ask.
3. **After You Change Code:** Explain what was done, why it was done that way, and what could go wrong. Point to the 1 or 2 files that matter.
4. **Give the human something to check or decide:** A choice, a behavior to verify in the browser/app, or a short checklist.
5. **No Token Waste on Full JSON:** Never dump raw `roadmap.js` into context. Always use `python scripts/roadmap.py brief`.
"""


def parse_highways(hw_str: str) -> list[dict]:
    """Parse format like 'core:backend,api ui:web,mobile' or default."""
    if not hw_str.strip():
        return [
            {"id": "core", "title": "Core Engine", "areas": ["core", "logic"]},
            {"id": "ui", "title": "User Interface", "areas": ["ui", "views"]},
            {"id": "infra", "title": "Tooling & Infra", "areas": ["infra", "docs"]},
        ]
    highways = []
    for item in hw_str.split():
        if ":" in item:
            hid, areas_str = item.split(":", 1)
            areas = [a.strip() for a in areas_str.split(",") if a.strip()]
        else:
            hid = item.strip()
            areas = [hid]
        title = " ".join(word.capitalize() for word in hid.replace("-", " ").replace("_", " ").split())
        highways.append({"id": hid, "title": title, "areas": areas or [hid]})
    return highways


def create_initial_data(project_name: str, repo: str, prd: str, highways: list[dict], theme: str) -> dict:
    today = date.today().isoformat()
    first_hw = highways[0]
    first_area = first_hw["areas"][0]
    second_hw = highways[1] if len(highways) > 1 else first_hw
    second_area = second_hw["areas"][0]

    return {
        "schema": 4,
        "project": project_name,
        "now": f"Building {project_name} baseline capabilities",
        "prd": prd or (repo + "#readme" if repo else "https://github.com"),
        "repo": repo or "https://github.com",
        "updated": today,
        "activeRelease": "0.1.0",
        "highways": highways,
        "releases": [
            {
                "version": "0.1.0",
                "status": "next",
                "title": "Foundation & Core Capabilities",
                "text": f"The initial release establishes the architectural foundation of {project_name}, configuring the baseline repository structure, core modules, and essential workflows. It verifies primary operational assumptions through lightweight end-to-end integration checks while proving the development loop. Early validation gates confirm system stability, reproducible builds, and seamless collaboration between human guidance and autonomous agent execution."
            },
            {
                "version": "1.0.0",
                "status": "planned",
                "title": "Initial Production Release",
                "essay": [
                    f"The 1.0.0 release marks the complete realization of the {project_name} architecture, delivering a transformative approach to developer-agent collaboration across modern software engineering workflows. By reimagining project planning not as a detached external issue tracker but as an immutable, Git-versioned artifact living directly alongside application source code, this release eliminates the cognitive dissonance between documentation, task planning, and actual execution. Teams and solo developers no longer need to navigate heavyweight commercial project management suites or maintain complex API synchronizations to track their engineering velocity across distributed branches. Instead, the roadmap serves as a living, transparent contract between human creative vision and autonomous implementation, establishing an intuitive operational cadence where every single code commit permanently records its architectural contribution directly within repository history.",
                    f"At the center of this release is the matured highway map visualization, which translates complex release engineering concepts into an immediately understandable spatial transit diagram. Rather than reducing milestone progress to arbitrary percentage bars, burn-down charts, or inaccurate velocity estimates, the atlas portrays software evolution as an expansive physical journey through geographical space. Distinct architectural subsystems operate as dedicated colored highways, while planned destinations emerge as grand interchanges where multiple engineering lanes converge into cohesive product releases. Shipped work remains permanently preserved as historical mile markers, allowing stakeholders and creators to inspect the precise historical effort that brought each major capability into existence without visual compression, artificial grouping, or arbitrary truncation of past achievements.",
                    f"Under the hood, the entire system adheres strictly to a zero-dependency philosophy, ensuring that the visual interface and its command-line companion execute reliably across any computing environment without package installation overhead or network dependencies. Written entirely using vanilla browser standards and the standard Python runtime library, the roadmap requires zero Node modules, zero Webpack configurations, zero compilers, and zero third-party packages to render or validate. Developers and AI coding agents interact with identical deterministic data models, utilizing streamlined command-line interfaces that compress hundreds of kilobytes of state into lightweight context briefs designed specifically to optimize large language model token efficiency and completely eliminate context window exhaustion during long programming sessions.",
                    f"Looking forward, the 1.0.0 milestone establishes a durable foundation for wide community adoption, providing adaptable templates, customizable color palettes, and extensible prompt frameworks that empower developers to tailor the system to any creative or technical domain imaginable. Whether deployed in game development, systems programming, web applications, or infrastructure automation, the roadmap system preserves the essential human prerogative of high-level creative direction while delegating mechanical verification and routine tracking to intelligent coding partners. This release demonstrates unequivocally that modern software development tools can achieve exceptional elegance, playful tactile charm, and visual beauty while remaining transparent, fully accessible, completely offline-first, and permanently under developer ownership for years to come."
                ]
            }
        ],
        "releasePlans": {
            "0.1.0": {
                "title": "Foundation & Core Capabilities",
                "goal": f"Establish the core foundation and primary workflows of {project_name}.",
                "done_when": "All initial tasks pass verification and core functionality is demonstrated.",
                "scope": "contained"
            },
            "1.0.0": {
                "title": "Initial Production Release",
                "goal": "Deliver fully validated production capability with full documentation.",
                "done_when": "Feature complete, thoroughly tested, and documented.",
                "scope": "medium"
            }
        },
        "stories": {
            "1": "Project can be initialized, built, and verified cleanly.",
            "2": "Users can run the primary application features without friction."
        },
        "tasks": [
            {
                "id": "baseline-architecture",
                "stage": 1,
                "title": f"Initialize {project_name} baseline architecture and project configuration",
                "label": "Project Setup",
                "area": first_area,
                "targetRelease": "0.1.0",
                "status": "doing",
                "stories": ["1"],
                "refs": ["README.md"],
                "notes": "Setting up directory structure and essential files."
            },
            {
                "id": "primary-workflow",
                "stage": 2,
                "title": "Build and verify primary user journey workflow",
                "label": "Primary Workflow",
                "area": second_area,
                "targetRelease": "0.1.0",
                "status": "next",
                "stories": ["2"],
                "refs": [],
                "notes": "Implement initial end-to-end functionality."
            }
        ],
        "decisions": [
            { "date": today, "text": "Adopted the Roadmap System for zero-terminal agent-human coordination." }
        ],
        "risks": [
            { "status": "open", "text": "Scope creep during early exploration phase." }
        ],
        "log": [
            { "date": today, "text": f"Initialized {project_name} roadmap." }
        ]
    }


def update_project(target: Path) -> int:
    """Update roadmap infrastructure (viewer, layout, and scripts) while strictly preserving roadmap.js."""
    target = target.resolve()
    target_docs = target / "docs" / "roadmap"
    target_scripts = target / "scripts"

    if not (target_docs / "roadmap.js").exists():
        print(f"Error: No existing roadmap found at {target_docs / 'roadmap.js'}")
        print("Run without --update to initialize a new project roadmap.")
        return 1

    target_docs.mkdir(parents=True, exist_ok=True)
    target_scripts.mkdir(parents=True, exist_ok=True)

    # 1. Update viewer files (NEVER touch roadmap.js)
    template_docs = TEMPLATE_DIR / "docs" / "roadmap"
    viewer_files = ["index.html", "tasks.html", "map-layout.js", "map.js", "common.js", "page.js", "theme.css"]
    updated_viewer = []
    for fname in viewer_files:
        src = template_docs / fname
        if src.exists():
            shutil.copy2(src, target_docs / fname)
            updated_viewer.append(fname)

    # 2. Update scripts
    template_scripts = TEMPLATE_DIR / "scripts"
    updated_scripts = []
    for fname in ["roadmap.py", "check_roadmap.py"]:
        src = template_scripts / fname
        if src.exists():
            shutil.copy2(src, target_scripts / fname)
            updated_scripts.append(fname)

    # 3. Check instructions in AGENTS.md / CLAUDE.md
    for guide_file in ["AGENTS.md", "CLAUDE.md"]:
        guide_path = target / guide_file
        if guide_path.exists():
            content = guide_path.read_text(encoding="utf-8")
            if "roadmap.js" not in content:
                guide_path.write_text(content.rstrip() + "\n\n" + AGENT_INSTRUCTIONS.strip() + "\n", encoding="utf-8")
                print(f"[+] Added roadmap instructions to {guide_file}")

    print("\n[+] Successfully updated Roadmap System infrastructure!")
    print(f"   - Target:     {target}")
    print(f"   - Preserved:  docs/roadmap/roadmap.js (intact)")
    print(f"   - Viewer:     Updated {len(updated_viewer)} files in docs/roadmap/")
    print(f"   - Scripts:    Updated {len(updated_scripts)} files in scripts/")

    # 5. Run validation
    check_script = target_scripts / "check_roadmap.py"
    if check_script.exists():
        import subprocess
        res = subprocess.run([sys.executable, str(check_script)], cwd=str(target))
        return res.returncode
    return 0


def init_project(target: Path, name: str, repo: str, prd: str, hw_str: str, theme: str, force: bool = False) -> int:
    target = target.resolve()
    target_docs = target / "docs" / "roadmap"
    target_scripts = target / "scripts"

    if target_docs.exists() and not force:
        print(f"Warning: {target_docs} already exists. Use --force to overwrite.")
        return 1

    target_docs.mkdir(parents=True, exist_ok=True)
    target_scripts.mkdir(parents=True, exist_ok=True)

    # 1. Copy web viewer files
    template_docs = TEMPLATE_DIR / "docs" / "roadmap"
    for fname in ["index.html", "tasks.html", "map-layout.js", "map.js", "common.js", "page.js", "theme.css"]:
        src = template_docs / fname
        if src.exists():
            shutil.copy2(src, target_docs / fname)

    # 2. Write customized roadmap.js
    highways = parse_highways(hw_str)
    roadmap_data = create_initial_data(name, repo, prd, highways, theme)
    roadmap_content = "window.ROADMAP_DATA = " + json.dumps(roadmap_data, ensure_ascii=False, indent=2) + ";\n"
    (target_docs / "roadmap.js").write_text(roadmap_content, encoding="utf-8")

    # Set default theme in theme.css or local storage if needed
    if theme and theme != "evergreen":
        # Inject theme default into index.html and tasks.html html tag
        for page_name in ["index.html", "tasks.html"]:
            page_path = target_docs / page_name
            if page_path.exists():
                text = page_path.read_text(encoding="utf-8")
                text = text.replace("<html lang=\"en\">", f'<html lang="en" data-palette="{theme}">')
                page_path.write_text(text, encoding="utf-8")

    # 3. Copy scripts
    template_scripts = TEMPLATE_DIR / "scripts"
    for fname in ["roadmap.py", "check_roadmap.py"]:
        src = template_scripts / fname
        if src.exists():
            shutil.copy2(src, target_scripts / fname)

    # 4. Append comprehensive agent instructions
    for guide_file in ["AGENTS.md", "CLAUDE.md"]:
        guide_path = target / guide_file
        if not guide_path.exists():
            guide_path.write_text(f"# {name} Agent Guide\n" + AGENT_INSTRUCTIONS.strip() + "\n", encoding="utf-8")
            print(f"Created {guide_path.relative_to(target)}")
        else:
            content = guide_path.read_text(encoding="utf-8")
            if "roadmap.js" not in content:
                guide_path.write_text(content.rstrip() + "\n\n" + AGENT_INSTRUCTIONS.strip() + "\n", encoding="utf-8")
                print(f"Updated {guide_path.relative_to(target)} with roadmap instructions")

    print(f"\n[+] Roadmap System successfully initialized in {target}!")
    print(f"   - Project:  {name}")
    print(f"   - Theme:    {theme}")
    print(f"   - Map:      docs/roadmap/index.html")
    print(f"   - Tasks:    docs/roadmap/tasks.html")
    print(f"   - CLI:      python scripts/roadmap.py brief\n")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize or update the Roadmap System in any project.")
    parser.add_argument("--target", default=".", help="Target project directory (default: current directory)")
    parser.add_argument("--update", action="store_true", help="Update viewer, layout, and scripts while strictly preserving roadmap.js")
    parser.add_argument("--name", default="Project", help="Project display name")
    parser.add_argument("--repo", default="", help="Git repository URL")
    parser.add_argument("--prd", default="", help="PRD or issue tracker link")
    parser.add_argument("--highways", default="", help="Highways & areas (e.g., 'core:engine,logic ui:frontend,styles')")
    parser.add_argument("--theme", default="evergreen", choices=["evergreen", "blueprint", "neon", "minimal", "sunset"], help="Color theme")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files (for new init)")
    args = parser.parse_args()

    if args.update:
        return update_project(target=Path(args.target))

    return init_project(
        target=Path(args.target),
        name=args.name,
        repo=args.repo,
        prd=args.prd,
        hw_str=args.highways,
        theme=args.theme,
        force=args.force,
    )


if __name__ == "__main__":
    sys.exit(main())
