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
      "text": "The initial release of the universal roadmap system generalizes the visual highway atlas and interactive task board into an in-repo, zero-dependency engine suitable for any software project. It establishes the foundational mental model where versions are milestones and tasks represent active roadwork, completely removing terminal friction for human creators through automated agent coordination. With built-in theme support across five distinct palettes and offline browser accessibility, development teams can inspect progress transparently without reliance on external project management infrastructure."
    },
    {
      "version": "1.0.0",
      "status": "planned",
      "title": "Public Open Source Release",
      "essay": [
        "The 1.0.0 release marks the complete realization of the universal roadmap architecture, delivering a transformative approach to developer-agent collaboration across modern software engineering workflows. By reimagining project planning not as a detached external issue tracker but as an immutable, Git-versioned artifact living directly alongside application source code, this release eliminates the cognitive dissonance between documentation, task planning, and actual execution. Teams and solo developers no longer need to navigate heavyweight commercial project management suites or maintain complex API synchronizations to track their engineering velocity across distributed branches. Instead, the roadmap serves as a living, transparent contract between human creative vision and autonomous implementation, establishing an intuitive operational cadence where every single code commit permanently records its architectural contribution directly within repository history.",
        "At the center of this release is the matured highway map visualization, which translates complex release engineering concepts into an immediately understandable spatial transit diagram. Rather than reducing milestone progress to arbitrary percentage bars, burn-down charts, or inaccurate velocity estimates, the atlas portrays software evolution as an expansive physical journey through geographical space. Distinct architectural subsystems operate as dedicated colored highways, while planned destinations emerge as grand interchanges where multiple engineering lanes converge into cohesive product releases. Shipped work remains permanently preserved as historical mile markers, allowing stakeholders and creators to inspect the precise historical effort that brought each major capability into existence without visual compression, artificial grouping, or arbitrary truncation of past achievements.",
        "Under the hood, the entire system adheres strictly to a zero-dependency philosophy, ensuring that the visual interface and its command-line companion execute reliably across any computing environment without package installation overhead or network dependencies. Written entirely using vanilla browser standards and the standard Python runtime library, the roadmap requires zero Node modules, zero Webpack configurations, zero compilers, and zero third-party packages to render or validate. Developers and AI coding agents interact with identical deterministic data models, utilizing streamlined command-line interfaces that compress hundreds of kilobytes of state into lightweight context briefs designed specifically to optimize large language model token efficiency and completely eliminate context window exhaustion during long programming sessions.",
        "Looking forward, the 1.0.0 milestone establishes a durable foundation for wide community adoption, providing adaptable templates, customizable color palettes, and extensible prompt frameworks that empower developers to tailor the system to any creative or technical domain imaginable. Whether deployed in game development, systems programming, web applications, or infrastructure automation, the roadmap system preserves the essential human prerogative of high-level creative direction while delegating mechanical verification and routine tracking to intelligent coding partners. This release demonstrates unequivocally that modern software development tools can achieve exceptional elegance, playful tactile charm, and visual beauty while remaining transparent, fully accessible, completely offline-first, and permanently under developer ownership for years to come."
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
      "text": "Enforced strict proportional release writing and bundled major highway lanes"
    },
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
