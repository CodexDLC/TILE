# Prompt boundaries

Use clear ownership wording for a design/data-only leaf:

```text
This is a design/data contract task only.
Do not edit code.
Do not modify shared consumers, runtime, log builders, resolvers, frontend, API, tests, compiler outputs, generated files, migrations, or integration code.
Only return a design document, schema proposal, and local data examples for this layer.
```

For an implementation leaf:

```text
You own only these files/layers: ...
Do not edit files outside this ownership.
If integration requires shared files, report the required integration point instead of editing it.
```

No leaf prompt should ask a worker to connect its output to a shared consumer, update a common contract, wire runtime, render frontend output, or list shared files to modify. Ask it to describe the data its layer provides to a future consumer, with integration notes only.

The final integrator prompt may own shared contract reconciliation, common DTO changes, consumer integration, runtime/frontend/API/log builder wiring, conflict resolution, migration and tests crossing leaf layers. It consumes outputs from leaf prompts rather than reinventing them.

Before delivery, check that no two leaf prompts own the same file or layer, every prompt is autonomous with explicit do-not-touch boundaries, design prompts forbid edits, implementation prompts have disjoint write scopes, and the final prompt alone owns integration.
