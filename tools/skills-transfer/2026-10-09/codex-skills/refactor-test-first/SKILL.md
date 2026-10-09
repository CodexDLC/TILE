---
name: refactor-test-first
description: Write failing tests for new behavior before refactoring an existing tested system, changing contracts, migrating architecture, or removing legacy paths and fallbacks.
---

# Refactor Test First

When refactoring or replacing an existing tested system, identify the required new behavior and existing tests that may encode the old behavior. Add or update an observable contract test **before production edits**, run it, and confirm it fails for the expected reason. Then change production code, pass the targeted test, and run the wider relevant set. Existing green tests alone do not prove the replacement.

For migration, legacy or fallback removal, include a test or static guard that fails if the old path still runs. For text/rendering and catalog/recipe systems, cover the actual producer-to-consumer runtime selection, not merely catalog existence. Do not claim completion until the new tests pass and the old behavior is removed, unreachable, or explicitly preserved by an approved compatibility contract.

If the behavior is undefined, the harness is missing, or requirements conflict so that no meaningful failing test can be written, stop before production edits and report the blocker. Report the initial expected failure, passing result, and how the old path was removed or guarded.
