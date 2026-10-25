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

`docs/roadmap/roadmap.js` is the single source of truth.
The human user does not use the terminal. **You (the agent) are responsible for updating tasks, running checks, and maintaining the roadmap.**

### Visual Pages (For Human Verification)
Tell the user they can double-click or open either page directly in their browser from disk:
- `docs/roadmap/index.html` (The Highway Map Atlas)
- `docs/roadmap/tasks.html` (The Task Board)

### Golden Rules
1. **Versions are destinations. Tasks are roadwork.**
2. **Every commit updates the roadmap.** Stage `roadmap.js` and run `python scripts/check_roadmap.py` before committing.
3. **Start every session with** `python scripts/roadmap.py brief`.
4. **Freedom to adapt:** It is perfectly okay to rewrite, adapt, modify, or extend the entire roadmap system (the HTML, CSS, JS, layout algorithms, or Python scripts) as part of the project. It's not a finished product or an unchangeable external framework; it is literally just an HTML file system committed directly to the repo.

### Routine Agent Commands
```bash
# Check current work (minimal tokens)
python scripts/roadmap.py brief

# Manage tasks
python scripts/roadmap.py add-task 0.1.0 --area core --title "Feature description" --label "Short Label"
python scripts/roadmap.py start TASK_ID
python scripts/roadmap.py unverified TASK_ID --note "Implementation complete; user review pending."
python scripts/roadmap.py done TASK_ID --note "Verified."
python scripts/roadmap.py move TASK_ID --before OTHER_ID
python scripts/roadmap.py retarget TASK_ID 0.2.0

# Pre-commit validation check
python scripts/check_roadmap.py
```
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
                "version": "0.0.1",
                "status": "released",
                "date": today,
                "title": "Groundwork & Environment",
                "highways": [first_hw["id"]],
                "text": "Initial project foundation establishing repository layout, baseline dependencies, and development environment."
            },
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
                "id": "repo-bootstrap",
                "stage": 1,
                "title": f"Initialize {project_name} repository structure and baseline tooling",
                "label": "Repo Bootstrap",
                "area": first_area,
                "targetRelease": "0.0.1",
                "status": "done",
                "shippedIn": "0.0.1",
                "completed": today,
                "stories": ["1"],
                "refs": ["README.md"],
                "notes": "Configured baseline directories and scripts."
            },
            {
                "id": "core-architecture",
                "stage": 1,
                "title": "Implement core subsystem architecture and interfaces",
                "label": "Core Architecture",
                "area": first_area,
                "targetRelease": "0.1.0",
                "status": "doing",
                "stories": ["1"],
                "refs": [],
                "notes": "Active engineering work."
            },
            {
                "id": "ui-prototype",
                "stage": 2,
                "title": "Build interactive user interface and view controls",
                "label": "UI Prototype",
                "area": second_area,
                "targetRelease": "0.1.0",
                "status": "next",
                "stories": ["2"],
                "refs": [],
                "notes": "Verify primary user journey."
            }
        ],
        "decisions": [
            { "date": today, "text": "Adopted the Roadmap System for zero-terminal agent-human coordination." }
        ],
        "risks": [
            { "status": "open", "text": "Scope creep during early exploration phase." }
        ],
        "log": [
            { "date": today, "text": f"Shipped 0.0.1 Groundwork and initialized {project_name} roadmap." }
        ]
    }


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

    # 4. Copy ready-to-use agent prompts
    target_prompts = target / "prompts"
    target_prompts.mkdir(parents=True, exist_ok=True)
    template_prompts = TEMPLATE_DIR / "prompts"
    if template_prompts.exists():
        for src in template_prompts.glob("*.md"):
            shutil.copy2(src, target_prompts / src.name)

    # 5. Append agent instructions
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
    parser = argparse.ArgumentParser(description="Initialize the Roadmap System in any project.")
    parser.add_argument("--target", default=".", help="Target project directory (default: current directory)")
    parser.add_argument("--name", default="Project", help="Project display name")
    parser.add_argument("--repo", default="", help="Git repository URL")
    parser.add_argument("--prd", default="", help="PRD or issue tracker link")
    parser.add_argument("--highways", default="", help="Highways & areas (e.g., 'core:engine,logic ui:frontend,styles')")
    parser.add_argument("--theme", default="evergreen", choices=["evergreen", "blueprint", "neon", "minimal", "sunset"], help="Color theme")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

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
