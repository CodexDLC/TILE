# Strict planning

Use for explicit strict mode or changes with substantial impact, dependency changes, migrations, generated artifacts or non-obvious architecture choices.

Before proposing edits:
1. Search relevant code and tests with `rg`; read the governing project instructions and runtime definitions.
2. Confirm imports, dependencies, configuration and the real test/build commands. Search the repository for reusable behavior before introducing a new helper; consult primary documentation when external API behavior is uncertain.
3. Identify required behavior, acceptance criteria, affected consumers and user changes to preserve.

Present a short plan:

```text
[Context Confirmed]: governing files, definitions and current behavior
[Execution Steps]: intended edits and checks
[Impact Radius]: affected contracts, flows, dependencies and data
```

Dependency changes, migrations, generated artifacts and consequential architecture choices must be explicit in the plan. Wait when the user requested plan approval, a decision is unresolved, or an action is destructive or outside authorized scope. When the user already approved the concrete work, proceed within that authorization; diagnostic requests still permit no edits.

Revise the plan if new evidence materially changes scope or risk. Do not treat the word "strict" as authorization for unrelated tooling, full-project refactoring or extra agents.
