# Verification and completion

Choose checks from actual project configuration and the changed behavior. Do not install tools or invent commands to satisfy a generic checklist.

| Check | When needed |
|---|---|
| Focused behavior/regression tests | Changed observable behavior or a reproduced defect |
| Wider tests | Shared contracts, cross-module effects or unresolved regression risk |
| Lint/types | Relevant project checks for the touched files |
| Build/package/render | Packaging, bundles, generated output or rendering affected |
| Runtime/browser inspection | Tests do not establish the actual UI or integration behavior |
| Security review | Access boundaries, sensitive data, payments, untrusted inputs or command execution affected |
| Diff review | Before claiming completion; include relevant staged, unstaged and newly created files |

Preserve real exit codes and enough output to diagnose failure. A truncated log or successful pipeline tail does not prove the underlying check passed. Do not impose a universal coverage threshold; follow project requirements and cover meaningful behavior.

Inspect the implementation against acceptance criteria, unintended changes, error paths and edge cases. Use an independent reviewer only when risk and isolation justify it. Fix findings, then repeat affected checks; do not rerun unrelated successful checks without new reason.

Report each relevant check as PASS, FAIL, NOT RUN (reason) or NOT APPLICABLE. Keep the final report proportional: what changed, observed validation, unresolved findings and material limitations. Do not claim security from simple grep results or browser correctness from backend tests alone.
