---
name: code-compatibility-decision
description: Decide whether code changes must preserve old behavior or fully replace it; use for refactors, contract migrations, legacy paths, fallbacks, and MVP architecture.
---

# Code Compatibility Decision

Before changing production code, decide whether existing data, public APIs, external clients, saved state, rolling deployments, or explicit user direction require old behavior. If so, use `compatibility-required`: state the contract, cover old input/output behavior with tests, and keep migration adapters at the boundary around one internal representation. Give temporary paths explicit removal conditions.

Otherwise use `replacement-only`, especially for an MVP/core change or an explicit request to remove legacy behavior. Replace the old path completely: update callers and tests, remove obsolete code, constants, configuration and helpers, and avoid fallback branches or dual sources of truth. A temporary bridge requires explicit user approval.

If the contract remains genuinely unclear after checking available context, ask one concise compatibility question before editing. Do not add an approval gate when the user's direction or system evidence already resolves it. In the final report, name the mode and which old paths were removed or retained.
