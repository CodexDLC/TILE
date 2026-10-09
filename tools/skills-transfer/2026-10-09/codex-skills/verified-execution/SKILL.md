---
name: verified-execution
description: Evidence-based coding, debugging, refactoring and review. Use for non-trivial changes or explicit strict mode (Pangolin Protocol, no blind actions, plan before changes, proof by tests). Scale verification to risk; diagnostic requests authorize no edits.
---

# Verified Execution

Research → plan → implement → test → inspect → review → fix → verify. Scale depth to the task; do not create agents or documents merely to fill stages.

## Boundaries

- Diagnose-only or ambiguous intent: inspect and report; no edits without explicit implementation authorization. Apply `ask-before-editing` when available.
- Read the governing files and local definitions before suggesting concrete code, calling helpers or editing. Verify dependencies and actual check commands; never invent missing symbols. Report missing evidence and clarify when it blocks progress.
- Check worktree state; preserve unrelated user changes. Make the smallest coherent change, preserve local style and contracts, and avoid speculative fixes, unrelated refactors or unnecessary abstractions.
- Respect explicit approval gates. Ask before destructive actions, scope expansion or unresolved consequential choices. Existing authorization remains valid; do not ask again merely to activate this workflow.
- Report only observed results. A skipped or unavailable check is not a pass. Agent reports do not prove personal inspection.

## Minimum security for affected code

Apply to the changed surface, without launching a full audit: treat client data as untrusted; use parameterized queries, context-aware output escaping and safe APIs instead of input-built SQL, shell commands or evaluated templates. Enforce server-side object/tenant permissions; protect secrets and sensitive logs. Preserve framework CSRF/session protections. For uploads, check actual content and resource limits, never trust names or MIME alone, and prevent executable storage/unsafe serving. Read [secure-code-baseline.md](references/secure-code-baseline.md) when changing input boundaries, uploads, authentication, payments or outbound fetches. A full project audit uses `security-review` only when requested; routine edits do not trigger it.

## Depth and routing

- **Small explicit change:** inspect → edit → focused check. No formal plan or extra agent.
- **Standard change:** discover actual behavior and acceptance criteria; state a short plan; implement; run relevant checks; inspect the diff; fix findings and recheck affected behavior.
- **Strict / high-risk change:** read [strict-planning.md](references/strict-planning.md) before edits. Explicit strict planning requires plan approval unless already granted.
- **New utility, dependency or integration:** read [research-reuse.md](references/research-reuse.md) when local reuse or external API behavior needs investigation.
- **Error or unclear cause:** read [debugging.md](references/debugging.md) before attempting a fix.
- **Feature/refactor completion or PR readiness:** read [verification.md](references/verification.md) to choose and report checks. Do not load it for every trivial edit.

Use project testing and architecture rules as the source of commands and contracts. For tested refactors, apply `refactor-test-first` when available. Delegate only when an isolated task or independent review justifies the cost, following the existing delegation policy. Read only references required by the selected path.

