# Agent Guide: The Visual Roadmap System

## The Roadmap: Keep It Current (Required for Agents)

`docs/roadmap/roadmap.js` is the single source of truth. It defines `window.ROADMAP_DATA = { ... };` (or `window.PROJECT_ROADMAP` / `window.COMPLETIONIST_ROADMAP`) with strict JSON after the assignment. The two plain HTML pages work directly from disk: `index.html` is the Release Atlas and `tasks.html` is the Task Board. Nothing requires a local web server or build process.

**Versions are destinations. Tasks are roadwork.** Several tasks share a `targetRelease`. Completing a task never creates a release, allocates a patch number, or tags Git. Every change, including documentation, fixes, and refactoring, is a task.

**Every commit updates the roadmap. No exceptions.** Stage `roadmap.js` with at least a new entry at the top of `log` describing the commit, and run `python scripts/check_roadmap.py` before committing. It must print `roadmap ok`.

---

## Critical Directive: The Human User Does NOT Touch The Terminal
The human creator using this project will not run terminal commands.
- **You (the AI agent)** own all CLI interactions (`python scripts/roadmap.py ...`, git commits, checks).
- When reporting progress or completing work, give the human user clickable file links to open the visual roadmap directly in their browser from disk:
  - [Open Highway Map Atlas](file:///docs/roadmap/index.html)
  - [Open Task Board](file:///docs/roadmap/tasks.html)

---

## Full Permission to Modify & Rewrite
> **To all AI Agents:** It is **perfectly okay to rewrite, adapt, modify, or extend** the entire roadmap system (the HTML files, CSS styling, JavaScript layout algorithms, data model, or Python scripts) as part of the project.
> It is **not** an untouchable external black-box package. It is literally just an HTML/JS/CSS/Python file system living transparently in your repository. If the project needs new lanes, different visualization rules, custom cards, or special filters--hack on it directly!

---

## Model and Routine Edits
- **Schema 4** has flat `tasks`, `releases`, `releasePlans`, `highways`, and one `activeRelease` (or null if no future destination remains).
- **`releases`** contains actual shipped versions and coherent planned destinations, in ascending version order, with shipped versions first. Preserve genuine shipped records, tags, and historical writing.
- **`releasePlans[VERSION]`** stores the destination title, goal, `done_when`, and broad `scope`: `contained`, `medium`, or `large`.
- **Tasks** have a stable internal `id`, full `title`, `status`, `area`, `targetRelease`, `stories`, optional `refs`/`notes`, optional concise `label`, and optional local numeric `stage`. No task has a `version`. New IDs are descriptive slugs (e.g. `build-jwt-auth`). Never reuse or renumber IDs.
- A done task can have a `completed` date. `shippedIn` names the actual released version carrying its work; absence means not yet shipped. Completed work and shipped software are different facts.
- **Task array order** controls local order. Stages are local sequence information; reorder tasks without renumbering IDs or releases. Retargeting logs the old and new destination, preserves the task, and removes its old local stage.

---

## Strict Task Lifecycle & Statuses
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

## Labels, Sizing & The Map (How to Write Tasks)
- **Every task gets a short `--label`:** Use 2-4 words, about 28 characters at most, **naming the thing and not the action** ("Fuzzy Index", not "Build the fuzzy index"; "JWT Auth", not "Implement the JWT authentication"). Dots on the map display this label. Without one, the map falls back to the full title trimmed with an ellipsis.
- **Task Titles:** The full `--title` should clearly and concisely describe the exact capability or fix being delivered.
- **How the map draws work:** Each task is a dot on its highway lane. Shipped tasks are grouped under the release that shipped them, with the release number as a small caption under the first dot. A run of dots between two signs shows how much work a release took. Major and minor releases are signs.
- **Never create a release to make a dot appear:** A task is already visible as a dot on the highway.
- **`--area` chooses the lane:** The areas-to-highway mapping is defined in `highways` in `roadmap.js`, so pick the area on purpose (e.g., `core`, `ui`, `infra`).
- **`shippedIn` places a done task in history:** The `release` command sets it automatically. Do not set it by hand.

---

## Session Start & Token Efficiency (Never Read Full JSON)
**Start every session with `python scripts/roadmap.py brief`.** Generated briefs are lightweight markdown files ignored by Git; never edit them directly.
Use the CLI helper instead of dumping the raw ~200KB `roadmap.js` into context:
- **Minimal (`--level minimal` or default):** Current `doing`, `unverified`, `next`, and `blocked` work with IDs, target releases, areas, and local stages.
- **Medium (`--level medium`):** Current goals and criteria, all remaining active-release work with full notes, recent completions, and latest shipped releases.
- **Maximum (`--level maximum`):** Lossless snapshot of every field and historical log.

---

## Routine CLI Commands Cheat Sheet
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

## Shipping Releases & Proportional Writing Rules
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

### Proportional Writing (Strictly Enforced by `check_roadmap.py`):
The checker strictly validates word counts and sentence structures for both planned and shipped releases:
- **PATCH:** Exactly **one sentence**, at most **50 words**, ending in punctuation.
- **MINOR:** Exactly **one paragraph** of **50 to 220 words**, containing at least two sentences.
- **MAJOR:** An essay of **at least 4 paragraphs** and **at least 450 words**.

The helper records shipping and moves `activeRelease` to the next destination; it never tags, pushes, or publishes. Tag `vX.Y.Z` on Git as a separate authorized shipping step.

---

## Working Agreements With The Human
1. **Plain English, Zero Jargon:** Explain updates simply. Name real concepts (e.g. a specific file or function) in a phrase, but skip internal minutiae.
2. **Before You Change Code:** State in 2-3 sentences what you plan to change and why. If there is a real design or scope choice, present 1-2 distinct options and ask.
3. **After You Change Code:** Explain what was done, why it was done that way, and what could go wrong. Point to the 1 or 2 files that matter.
4. **Give the human something to check or decide:** A choice, a behavior to verify in the browser/app, or a short checklist.
5. **No Token Waste on Full JSON:** Never dump raw `roadmap.js` into context. Always use `python scripts/roadmap.py brief`.
