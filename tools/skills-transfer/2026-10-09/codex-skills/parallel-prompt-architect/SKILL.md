---
name: parallel-prompt-architect
description: Write isolated prompts for parallel chats, agents, or contractors, with disjoint leaf ownership and one final integration prompt.
---

# Parallel Prompt Architect

When writing prompts for parallel workers, first identify shared layers, independent leaf scopes, and a final integration owner. State this boundary map briefly. Give each leaf one disjoint artifact, layer, module or data slice; only the final integrator may reconcile contracts or change shared consumers, runtime, frontend, API, migrations and cross-layer tests. If a requested prompt count forces overlap, explain and propose a safer split.

Each leaf prompt must state its exact ownership and exclusions, whether it is design/data only, implementation or review, its expected output, and a small local example. Design/data-only prompts must explicitly forbid code edits. Implementation prompts must name permitted files/layers and require the worker to report needed shared changes without making them. The final integration prompt consumes leaf outputs and owns shared reconciliation; it should not recreate leaf work.

For prompt wording and a final overlap check, read [references/prompt-boundaries.md](references/prompt-boundaries.md).
