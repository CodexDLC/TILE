---
name: project-skill-loader
description: Load project-specific agent skills at session start or workspace changes; check affected operational skills when code, schemas, APIs, catalogs, or data changes alter their workflow.
---

# Project Skill Loader

At the start of a session or after changing workspaces, check project instructions and `.agents/skills/` or `docs/agent-skills/` where present. Before relevant edits or design decisions, read the project `SKILL.md` files that apply to the task, plus any project context explicitly marked mandatory. Project instructions take precedence over generic patterns while remaining subject to higher-priority instructions. Tell the user which project skills you loaded; do not assume mirrors are synchronized or load both copies of identical content.

After changing code, schemas, APIs, catalogs, meaningful data or workflow rules, inspect only the affected operational skills and references for stale reading, editing or verification instructions. Cosmetic changes need no such check unless they invalidate an instruction. Keep implemented behavior distinct from planned behavior, and account for local/API guidance and maintained mirrors. If the change is within authorized scope, update affected skill instructions; otherwise report the exact pending update without silently expanding the task. Before handoff, state the update or that the affected instructions remain valid.

For the operational alignment check, read [references/operational-alignment.md](references/operational-alignment.md) when a change can alter an agent workflow.
