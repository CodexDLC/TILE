---
name: project-skills-maintainer
description: Create or maintain application-owned project skills for architecture, business rules, and integrations. Use for authorized project guidance work, excluding managed library, global, system, and plugin skills.
---

# Project Skills Maintainer

Maintain operational guidance owned by the application. Use the project's existing discovery convention and location; do not impose a new directory hierarchy just because one is familiar. Read the applicable project instructions, current implementation, and existing skills before deciding whether a new entrypoint, a focused reference, or a small correction is needed.

For an audit, identify stale or missing guidance without editing. For authorized edits, describe the project's actual architecture, business invariants, safety rules, integration contracts, and verification steps that change an agent's decisions. Ground each statement in code, schema, tests, or an explicit owner decision. Preserve important constraints while removing obsolete ones only with evidence; mark unknown behavior as unknown and seek human review for unresolved business requirements. Keep the entrypoint short and link conditional references only for tasks that need them. Do not copy a vendor API guide into a project skill; link or locate the installed library skill, then document the application's adapter and contract in project-owned references. Avoid absolute paths tied to a developer's machine.

Check ownership before every edit. Package manifests, version/hash records, generated headers, or managed markers can identify vendor-managed content even when it sits in a project folder. Do not modify a managed library copy or its manifest, nor global, system, or plugin skills. If the library guidance needs repair, work in its proven canonical source under separate authorization. See [references/ownership-and-evidence.md](references/ownership-and-evidence.md) for authoring/refactoring structure and ownership/evidence checks.

Protect existing user changes: inspect the diff and make a recoverable backup before replacing substantial content or generated material. Prefer a narrow edit. Keep implemented behavior separate from plans and proposals. Do not add automatic maintenance on every edit, mandatory agents, or broad reference loading. Keep configuration, MCP, and runtime code unchanged unless separately requested.

Validate the skill structure and any instructions whose behavior can be exercised. Report what changed, the evidence used, checks actually run, and unresolved claims. Do not claim token savings or workflow improvement without observation.
