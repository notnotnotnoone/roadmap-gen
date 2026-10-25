# Master Agent Directive: The Roadmap System

You are the developer's AI coding partner. In this repository, project progress and architectural direction are managed by an in-repo, visual roadmap system located at `docs/roadmap/` and managed via `scripts/roadmap.py`.

---

## 1. Core Philosophy: Destinations vs. Roadwork
* **Versions are destinations. Tasks are roadwork.**
  Completing tasks never automatically allocates a release or tags Git. Several tasks share a `targetRelease`.
* **The human developer does NOT touch the terminal.**
  The human will not run commands like `python scripts/roadmap.py ...` or git commits. You (the AI agent) own all CLI interactions.
* **Keep the visual feedback loop alive:**
  When reporting progress or completing work, always provide clickable local file links so the human can review the live state in their browser:
  - [Open Highway Map Atlas](file:///docs/roadmap/index.html)
  - [Open Task Board](file:///docs/roadmap/tasks.html)
* **It's an adaptable HTML file system:**
  You have full permission to adapt, modify, rewrite, or extend the HTML/CSS/JS/Python files of this roadmap system as part of the project. It is not an untouchable external black box.

---

## 2. Working Agreements With The Human
1. **Plain English, Zero Jargon**: Explain updates simply. Name real concepts (e.g. a specific file or function) in a phrase, but skip internal minutiae.
2. **Before You Change Code**: State in 2-3 sentences what you plan to change and why. If there is a real design or scope choice, present 1-2 distinct options and ask.
3. **After You Change Code**: Explain what was done, why it was done that way, and what could go wrong. Point to the 1 or 2 files that matter.
4. **Give the human something to check or decide**: A choice, a behavior to verify in the browser/app, or a short checklist.
5. **No Token Waste on Full JSON**: Never dump the raw ~200KB `roadmap.js` into context. Always use `python scripts/roadmap.py brief`.

---

## 3. Strict Task Lifecycle & Statuses
Every task flows through a strict state machine:
* `todo`: Queued work planned for a destination.
* `next`: The immediate next task queued for execution.
* `doing`: Active implementation is underway right now.
* `unverified`: **Implementation is complete in code, but real-world human verification is pending.** (e.g., human checking in browser or app). *Unverified tasks block releases until verified!*
* `done`: Verification criteria are fully met.
* `dropped`: Work intentionally cancelled or superseded (appears as faded spur on map).

### Golden Rule: Every Commit Updates the Roadmap
Every single commit MUST stage `docs/roadmap/roadmap.js` with a new log entry at the top of `log`.
Before finalizing any turn, run:
```bash
python scripts/check_roadmap.py
```
It MUST print `roadmap ok`. If it reports an error, fix it immediately before reporting to the user.

---

## 4. Routine CLI Commands
```bash
# 1. Orientation at the start of a session (saves token budget)
python scripts/roadmap.py brief

# 2. Starting work on a task
python scripts/roadmap.py start TASK_ID

# 3. Marking implementation complete, awaiting human check
python scripts/roadmap.py unverified TASK_ID --note "Code complete; waiting for human to test in browser."

# 4. Marking verified and complete
python scripts/roadmap.py done TASK_ID --refs "PR#12,src/main.py" --note "Verified in real browser."

# 5. Adding new discoveries as roadwork (never invent patch numbers for tasks!)
python scripts/roadmap.py add-task 0.1.0 --area core --title "Implement JWT validation" --label "JWT Validation"

# 6. Reordering or retargeting tasks
python scripts/roadmap.py move TASK_ID --before OTHER_ID
python scripts/roadmap.py retarget TASK_ID 0.2.0

# 7. Logging changes
python scripts/roadmap.py log "Refactored auth middleware and updated unit tests."

# 8. Shipping a release (separate explicit action)
python scripts/roadmap.py release 0.1.0 --validated "All integration tests passed." --text "Initial foundation release establishing core engine and visual roadmap."
```

---

## 5. Proportional Release Writing Rules
When shipping releases, the validator enforces proportional writing:
* **Patch release**: Exactly 1 sentence, at most 50 words, ending in punctuation.
* **Minor release**: Exactly 1 paragraph, 50 to 220 words, at least 2 sentences.
* **Major release**: An essay of at least 4 paragraphs and at least 450 words.
