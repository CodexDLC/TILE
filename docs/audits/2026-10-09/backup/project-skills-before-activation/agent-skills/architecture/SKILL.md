---
name: atlas-architecture
description: Load this skill when working on Atlas backend or public-site architecture. Covers dynamic DB-driven pages, layer boundaries, and project structure expectations.
---

Read:
- `docs/architecture/README.md`
- `docs/architecture/content-platform.md`

Project rules:
- All public-facing pages must be designed for DB-backed rendering.
- The main public hierarchy is `Country -> Region -> City -> Place`.
- Use the shared `Page + typed blocks` content-platform direction.
- Keep public-site logic out of `system`; reserve `system` for site-wide shared concerns.
- Treat `features.main` as transitional; move toward a real public-site/content feature instead of adding more static pages.

Layer rules:
- Views are thin.
- Selectors own reads and template-context assembly.
- Services own writes, orchestration, and side effects.
- Do not place heavy business logic directly in Django views.
