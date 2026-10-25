# Workflow Prompt: Shipping a Release

Use this prompt when all tasks for a target release are complete and you want to formally ship the release.

---

## Agent Prompt:
```markdown
All roadwork for destination [VERSION] is complete. Let's officially ship this release:
1. Verify that all required tasks in [VERSION] are marked `done` (or explicitly `dropped`). No `unverified` tasks may remain.
2. Draft the release description following the strict proportional writing rules:
   - For a PATCH (e.g. 1.0.1): exactly 1 sentence, max 50 words.
   - For a MINOR (e.g. 1.1.0): exactly 1 paragraph, 50 to 220 words, at least 2 sentences.
   - For a MAJOR (e.g. 2.0.0): an essay of at least 4 paragraphs and at least 450 words.
3. Execute the release action:
   `python scripts/roadmap.py release [VERSION] --validated "Summary of integration and owner checks passed." --text "Your proportional release writing."`
4. Run `python scripts/check_roadmap.py` to ensure schema integrity.
5. Create the Git release commit and tag:
   `git commit -am "chore(release): v[VERSION]"`
   `git tag v[VERSION]`
6. Give me clickable file links to inspect the updated historical sign on the Highway Map:
   - [Highway Map Atlas](file:///docs/roadmap/index.html)
```
