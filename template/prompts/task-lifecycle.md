# Workflow Prompt: Implementing a Task

Use this prompt when delegating a specific task or feature to an AI agent.

---

## Agent Prompt:
```markdown
We are ready to work on task: [TASK_ID]

Follow the strict roadmap lifecycle:
1. Mark the task as active:
   `python scripts/roadmap.py start [TASK_ID]`
2. Explain in 2-3 plain sentences what code you plan to change and why before modifying files.
3. Implement the necessary code changes neatly and concisely.
4. If this requires human verification (e.g. testing in a browser or GUI app):
   - Mark the task `unverified`:
     `python scripts/roadmap.py unverified [TASK_ID] --note "Implemented code; human verification pending."`
   - Provide me with a short 2-item checklist of what I need to test or look at.
5. If no human testing is required (e.g. pure logic validated by automated tests):
   - Mark the task `done`:
     `python scripts/roadmap.py done [TASK_ID] --note "What was verified and tested."`
6. Always validate with `python scripts/check_roadmap.py` before finishing your turn.
```
