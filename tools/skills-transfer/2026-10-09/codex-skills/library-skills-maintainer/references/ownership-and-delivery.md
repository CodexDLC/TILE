# Ownership and delivery checks

Use this reference when a library skill's location, packaging, or update path matters.

## Authoring the consumer contract

Use `name` and a concise `description` in YAML frontmatter. Describe when the library skill applies, without triggering it for every task in the consumer. Keep the body to source/version discovery, task-to-reference routing, ownership boundaries and essential invariants. Put substantial API usage and integration examples in references by consumer task, not one file per exported symbol. A small library may need only one self-contained SKILL.md.

Examples should show real public imports and the minimum wiring needed; distinguish runnable examples from schematic fragments. Include relevant failure modes and unsupported use, not an exhaustive API dump. Check reference links within the shipped payload. Use portable package-relative source locators; don't depend on the author's checkout, secrets, unpublished docs or test fixtures being installed. Preserve existing invocation metadata unless its change is requested.

## Delivery

1. Establish ownership from the package's canonical build/release source, not merely from its location in a checkout or an editable install. Inspect the package metadata and the build artifact's included files.
2. Confirm the version and public API the skill describes. Prefer a tiny runnable example against that version over a broad copied API catalog. State constraints and extension points that a consumer cannot easily infer.
3. Identify the official consumer installation path before proposing a refresh. A packaged library may offer an optional offline skill installer; this is one delivery pattern, not a universal requirement.
4. For example, a `codex-django` source package can ship `resources/SKILL.md` and focused references, and optionally provide install/update/delete/status commands for `.agents/skills/codex-django`, a short managed `AGENTS.md` marker, and a version/hash manifest. In that design the source resource is editable; the consumer copy and its manifest are managed outputs.
5. If packaging or installer behavior changed, inspect the built artifact and test the affected lifecycle in an isolated consumer. Check how updates handle local edits and how deletion preserves unrelated user content. Avoid claiming validation from source-tree inspection alone.
