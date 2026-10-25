# Agent Handbook: Roadmap System

## Critical Directive: The Human User Does NOT Touch The Terminal
The human creator using this project will not run terminal commands.
- **You (the AI agent)** own all CLI interactions (`python scripts/roadmap.py ...`, git commits, checks).
- When reporting progress, give the human user clickable file links to open the visual roadmap directly in their browser from disk:
  - [Open Highway Map Atlas](file:///docs/roadmap/index.html)
  - [Open Task Board](file:///docs/roadmap/tasks.html)

## Full Permission to Modify & Rewrite
> **To all AI Agents:** It is **perfectly okay to rewrite, adapt, modify, or extend** the entire roadmap system (the HTML files, the CSS styling, the JavaScript layout algorithms, the data model, or the Python scripts) as part of the game.
>
> It is **not** a finished sacred product or an external black-box package. It is literally just an HTML/JS/CSS/Python file system living transparently in your repository. If the project needs new lanes, different visualization rules, custom cards, or special filters—hack on it directly!

---

## The Golden Rules
1. **Versions are destinations. Tasks are roadwork.** Completing tasks never automatically ships a release.
2. **Every commit updates the roadmap.** Stage `docs/roadmap/roadmap.js` with a new log entry at the top of `log`.
3. **Always validate before finishing:** Run `python scripts/check_roadmap.py`. It must print `roadmap ok`.
4. **Start sessions with minimal brief:** Run `python scripts/roadmap.py brief` to inspect active tasks without wasting context tokens on full JSON files.

---

## Working Agreements With The Human
1. **Plain English, Zero Jargon**: Explain updates simply. Name real concepts (e.g. a specific file or function) in a phrase, but skip internal minutiae.
2. **Before You Change Code**: State in 2-3 sentences what you plan to change and why. If there is a real design or scope choice, present 1-2 distinct options and ask.
3. **After You Change Code**: Explain what was done, why it was done that way, and what could go wrong. Point to the 1 or 2 files that matter.
4. **Give the human something to check or decide**: A choice, a behavior to verify in the browser/app, or a short checklist.
5. **No Token Waste on Full JSON**: Never dump the raw ~200KB `roadmap.js` into context. Always use `python scripts/roadmap.py brief`.

---

## Strict Task Lifecycle & Statuses
Every task flows through a strict state machine:
* `todo`: Queued work planned for a destination.
* `next`: The immediate next task queued for execution.
* `doing`: Active implementation is underway right now.
* `unverified`: **Implementation is complete in code, but real-world human verification is pending.** (e.g., human checking in browser or app). *Unverified tasks block releases until verified!*
* `done`: Verification criteria are fully met.
* `dropped`: Work intentionally cancelled or superseded (appears as faded spur on map).

---

## Routine Commands Cheat Sheet
```bash
# Check active work
python scripts/roadmap.py brief

# Task lifecycle
python scripts/roadmap.py add-task 0.1.0 --area engine --title "Description" --label "Short Label"
python scripts/roadmap.py start TASK_ID
python scripts/roadmap.py unverified TASK_ID --note "Implementation done; user checking in browser."
python scripts/roadmap.py done TASK_ID --note "Verified and working."
python scripts/roadmap.py move TASK_ID --before OTHER_ID
python scripts/roadmap.py retarget TASK_ID 0.2.0
python scripts/roadmap.py drop TASK_ID --reason "Why it was dropped."
python scripts/roadmap.py log "Summary of what changed."

# Shipping releases (proportional writing enforced)
python scripts/roadmap.py release 0.1.0 --validated "Checks passed." --text "One sentence or paragraph describing what shipped."

# Pre-commit validation
python scripts/check_roadmap.py
```

---

## Available Prompts in `prompts/`
When delegating or orchestrating workflows, refer to:
* `prompts/system-directive.md`: Full master instructions for AI coding assistants.
* `prompts/session-start.md`: How to start every session with an orientation brief.
* `prompts/task-lifecycle.md`: How to transition tasks from start -> unverified -> done.
* `prompts/release-ship.md`: How to validate and ship a release destination.
