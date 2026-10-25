window.ROADMAP_DATA = {
  "schema": 4,
  "project": "Roadmap-Gen",
  "now": "Initial release of the generalized visual roadmap engine",
  "prd": "https://github.com/notnotnotnoone/roadmap-gen#readme",
  "repo": "https://github.com/notnotnotnoone/roadmap-gen",
  "updated": "2026-10-24",
  "activeRelease": "0.1.0",
  "highways": [
    {
      "id": "core",
      "title": "Engine & CLI",
      "areas": [
        "engine",
        "cli"
      ]
    },
    {
      "id": "ui",
      "title": "Highway Map & Board",
      "areas": [
        "map",
        "board",
        "theme"
      ]
    },
    {
      "id": "infra",
      "title": "Scaffolder & Docs",
      "areas": [
        "scaffolder",
        "docs"
      ]
    }
  ],
  "releases": [
    {
      "version": "0.1.0",
      "status": "next",
      "title": "Universal Visual Roadmap Engine",
      "text": "Initial release of the generalized in-repo roadmap system featuring zero terminal friction for humans and seamless agent coordination."
    },
    {
      "version": "1.0.0",
      "status": "planned",
      "title": "Public Open Source Release",
      "essay": [
        "The first general release brings complete end-to-end functionality to users with validated workflows.",
        "Core engine operations run with predictable performance, minimal overhead, and deterministic state transitions.",
        "The user experience is refined and responsive, providing immediate feedback and keyboard navigation.",
        "Comprehensive documentation and automated verification ensure long-term stability and effortless maintenance across teams."
      ]
    }
  ],
  "releasePlans": {
    "0.1.0": {
      "title": "Universal Visual Roadmap Engine",
      "goal": "Extract, generalize, and package the Completionist Roadmap System for use in any project.",
      "done_when": "All template files, multi-theme CSS, pure stdlib CLI, and one-command init generator are working.",
      "scope": "contained"
    },
    "1.0.0": {
      "title": "Public Open Source Release",
      "goal": "Publish to GitHub and provide turn-key adoption for open-source developers.",
      "done_when": "Feature complete, thoroughly tested, and documented with live demo.",
      "scope": "medium"
    }
  },
  "stories": {
    "1": "Users can view visual highway map and task board in any browser offline.",
    "2": "Agents can inspect tasks with minimal tokens and execute deterministic updates."
  },
  "tasks": [
    {
      "id": "extract-engine",
      "stage": 1,
      "title": "Extract and parameterize roadmap engine and schema validator",
      "label": "Engine Extraction",
      "area": "engine",
      "targetRelease": "0.1.0",
      "status": "done",
      "stories": [
        "2"
      ],
      "refs": [
        "scripts/roadmap.py",
        "scripts/check_roadmap.py"
      ],
      "completed": "2026-10-24",
      "notes": "Decoupled project name, window variables, and added flexible release check rules."
    },
    {
      "id": "multi-theme-support",
      "stage": 2,
      "title": "Build multi-theme support (Evergreen, Blueprint, Neon, Minimal, Sunset)",
      "label": "Custom Themes",
      "area": "theme",
      "targetRelease": "0.1.0",
      "status": "done",
      "stories": [
        "1"
      ],
      "refs": [
        "docs/roadmap/theme.css",
        "docs/roadmap/common.js"
      ],
      "completed": "2026-10-24",
      "notes": "Added interactive palette selector and full Day/Night mode support across all themes."
    },
    {
      "id": "scaffolder-generator",
      "stage": 3,
      "title": "Create zero-friction init_roadmap.py generator for any target repository",
      "label": "Project Scaffolder",
      "area": "scaffolder",
      "targetRelease": "0.1.0",
      "status": "done",
      "stories": [
        "1",
        "2"
      ],
      "refs": [
        "init_roadmap.py"
      ],
      "completed": "2026-10-24",
      "notes": "Tested in sandbox; handles project names, custom highways, and sets up AGENTS.md."
    },
    {
      "id": "agent-philosophy-docs",
      "stage": 4,
      "title": "Document zero-terminal user workflow and agent permission contract",
      "label": "Agent Contracts",
      "area": "docs",
      "targetRelease": "0.1.0",
      "status": "done",
      "stories": [
        "2"
      ],
      "refs": [
        "README.md",
        "AGENTS.md"
      ],
      "completed": "2026-10-24",
      "notes": "Explicitly instructed agents that they have full permission to modify or rewrite the HTML file system."
    }
  ],
  "decisions": [
    {
      "date": "2026-10-24",
      "text": "Designed as an in-repo, zero-dependency HTML/JS/CSS system rather than an external npm/pip package."
    },
    {
      "date": "2026-10-24",
      "text": "Targeted zero-terminal interaction for the human creator; AI agents drive 100% of the roadmap maintenance."
    }
  ],
  "risks": [
    {
      "status": "mitigated",
      "text": "Windows console encoding when printing unicode emojis (switched to clean ASCII banners in init CLI)."
    }
  ],
  "log": [
    {
      "date": "2026-10-24",
      "text": "Fixed SVG map rendering, restored full highway styling, and bundled prompt suite"
    },
    {
      "date": "2026-10-24",
      "text": "Published Roadmap-Gen to GitHub with live GitHub Pages"
    },
    {
      "date": "2026-10-24",
      "text": "Completed core implementation of Roadmap-Gen: engine extraction, multi-theme CSS, scaffolder, and agent guides."
    }
  ]
};
