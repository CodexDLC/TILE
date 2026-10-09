# Research and reuse

Use when introducing a utility, dependency, integration or unfamiliar API; a routine local change does not require an ecosystem survey.

1. Search the repository and its tests for existing behavior and conventions first. Read the actual implementation and dependency/version declarations.
2. If the repository has no suitable solution, consult primary vendor documentation and relevant package or source repositories. Check which search channels are actually available; unavailable search is not evidence that no solution exists.
3. Compare only plausible candidates against the required behavior, version compatibility, maintenance, license, dependency cost and data boundaries. Choose reuse, a narrow extension or custom implementation with a concrete reason.
4. Verify APIs before relying on them. Do not install packages, MCP servers or skills merely because research found them; remain within the authorized change and explain material new dependencies in the plan.

Return the useful evidence and decision, not an exhaustive list of searches. No mandatory researcher agent, broad MCP discovery or external search when local evidence already settles the question.
