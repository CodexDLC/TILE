---
name: skill-stocktake
description: Audit a selected skills library for overlap, trigger quality, stale guidance and context cost. Use for skill-library maintenance or a requested skill audit, not for every coding task.
---

# Skill Stocktake

Produce evidence-backed keep, improve, merge or retire recommendations. Auditing never authorizes changes or deletion.

1. Establish roots and exclusions from the request and available context; ask only if unresolved scope materially changes the audit. Inventory names, descriptions, entrypoint sizes, references and maintained mirrors; distinguish user, project, system and plugin ownership. Do not scan secrets or raw session histories by default.
2. Read [audit-method.md](references/audit-method.md). Inspect changed or selected skills first, then their direct overlaps; do not load the whole library to judge one skill.
3. Report each finding with paths, evidence, proposed action and its impact. Separate configured, currently available and observed use; mark frequency unknown without reliable records.
4. If edits are explicitly authorized, preserve critical constraints, invocation policy and metadata, check callers, save a rollback snapshot and verify links and realistic positive/negative scenarios. Never auto-uninstall dependencies or modify MCP, hooks, config or project files as a side effect.

Metadata has a discovery cost; full instructions and references are conditional. Report character counts as proxies, not exact active tokens or subscription savings. Do not retire a rare but necessary safety skill because usage is low.
