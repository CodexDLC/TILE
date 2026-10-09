# Ownership and evidence checks

Read this when a project skill's authority or a proposed removal is unclear.

## Creating or refactoring

Use YAML `name` and a short `description` identifying the project's actual workflow and activation conditions. Keep the body to essential safety/business constraints and task-based reference routing. A single short skill needs no reference directory. For larger guidance, separate architecture, operational procedures or integration details only when those are independently useful; load them conditionally.

Inventory existing content before moving it: preserve required decisions and source links, merge actual duplicates, and label unresolved claims. Choose scopes by task rather than making one skill per file. Keep global process guidance and vendor API instructions at their owning level. When renaming or moving owned files, update their local callers/index links and verify no relevant content was dropped. Preserve existing metadata and discovery policy. A request to refactor project skills authorizes this work, not a new business rule, dependency upgrade or change to vendor-managed instructions.

Validate frontmatter and local links; check operational commands against the project's real environment. Review positive and unrelated-task trigger examples, and report reasoning-only checks separately from execution. Exact token savings cannot be inferred from character counts.

## Ownership

- Follow the repository's existing skill discovery convention. Check project instructions and any local skill index before creating a new path. A skill under `.agents/skills/` can still be managed by a dependency.
- Inspect generated headers, package/version/hash manifests, source links, and installer commands. Treat a managed copy as read-only to the project maintainer, including its manifest and managed `AGENTS.md` marker.
- For library integration, locate the installed skill or its official source by package identity and version. Keep the application's adapter behavior, permissions, data rules, and business invariants in project-owned references.
- Trace a proposed instruction to current code, tests, schema, or a recorded owner decision. If those disagree, state the mismatch. Remove a supposedly stale rule only after confirming that the underlying behavior or policy changed.
- Before replacing a file with user additions, preserve a recoverable copy or work from a narrow diff. Record which claims were verified by execution and which were verified only by inspection.
