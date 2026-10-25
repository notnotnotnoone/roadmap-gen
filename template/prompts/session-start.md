# Workflow Prompt: Session Start & Briefing

Use this prompt at the start of any work session, or whenever you want the agent to orient itself and give you a clean progress report.

---

## Agent Prompt:
```markdown
Please start our session by checking the project roadmap:
1. Run `python scripts/roadmap.py brief` to inspect our active in-progress and next tasks without reading full JSON files.
2. In plain English, give me a 3-bullet summary:
   - What target release we are building toward.
   - What task is currently in progress (`doing` or `unverified`).
   - What task is queued `next`.
3. Provide clickable file links to open the visual Highway Map and Task Board in my browser:
   - [Highway Map Atlas](file:///docs/roadmap/index.html)
   - [Task Board](file:///docs/roadmap/tasks.html)
4. Tell me what we should tackle first today and wait for my go-ahead.
```
