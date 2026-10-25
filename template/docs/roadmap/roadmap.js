window.ROADMAP_DATA = {
  "schema": 4,
  "project": "Starter Project",
  "now": "Initial architecture and core setup",
  "prd": "https://github.com/owner/repo#readme",
  "repo": "https://github.com/owner/repo",
  "updated": "2026-10-24",
  "activeRelease": "0.1.0",
  "highways": [
    { "id": "core", "title": "Core Engine", "areas": ["engine", "logic"] },
    { "id": "ui", "title": "User Interface", "areas": ["ui", "views"] },
    { "id": "infra", "title": "Tooling & Infra", "areas": ["infra", "docs"] }
  ],
  "releases": [
    {
      "version": "0.1.0",
      "status": "next",
      "title": "Foundation & Core Spike",
      "text": "Initial foundation establishing project structure, core workflow, and baseline interface."
    },
    {
      "version": "1.0.0",
      "status": "planned",
      "title": "First General Release",
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
      "title": "Foundation & Core Spike",
      "goal": "Establish the project architecture and verify the primary user journey.",
      "done_when": "All initial tasks pass verification and core functionality is demonstrated.",
      "scope": "contained"
    },
    "1.0.0": {
      "title": "First General Release",
      "goal": "Deliver production-ready functionality for all primary use cases.",
      "done_when": "Feature complete, thoroughly tested, and documented.",
      "scope": "medium"
    }
  },
  "stories": {
    "1": "Project can be initialized and configured cleanly.",
    "2": "Users can run the core functionality without friction."
  },
  "tasks": [
    {
      "id": "setup-foundation",
      "stage": 1,
      "title": "Initialize project structure and baseline configuration",
      "label": "Project Setup",
      "area": "engine",
      "targetRelease": "0.1.0",
      "status": "doing",
      "stories": ["1"],
      "refs": ["README.md"],
      "notes": "Setting up directory layout and initial scripts."
    },
    {
      "id": "build-ui-skeleton",
      "stage": 2,
      "title": "Create primary view and interactive controls",
      "label": "UI Prototype",
      "area": "ui",
      "targetRelease": "0.1.0",
      "status": "next",
      "stories": ["2"],
      "refs": [],
      "notes": "Basic view structure."
    }
  ],
  "decisions": [
    { "date": "2026-10-24", "text": "Adopted the Roadmap System for transparent, zero-terminal agent coordination." }
  ],
  "risks": [
    { "status": "open", "text": "Scope creep during early prototype phase." }
  ],
  "log": [
    { "date": "2026-10-24", "text": "Initialized project roadmap." }
  ]
};
