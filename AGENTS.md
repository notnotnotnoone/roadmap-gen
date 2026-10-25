# Agent Handbook: Roadmap System

## Critical Directive: The Human User Does NOT Touch The Terminal
The human creator using this project will not run terminal commands.
- **You (the AI agent)** own all CLI interactions (`python scripts/roadmap.py ...`, git commits, checks).
- When reporting progress, give the human user clickable file links to open the visual roadmap directly in their browser from disk:
  - [Open Highway Map Atlas](file:///c:/projects/tools/roadmap-gen/docs/roadmap/index.html)
  - [Open Task Board](file:///c:/projects/tools/roadmap-gen/docs/roadmap/tasks.html)

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

# Validation
python scripts/check_roadmap.py
```
