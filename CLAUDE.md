# Atlas

Atlas is an editorial travel guide: a hybrid between a structured destination
aggregator and a light editorial blog. The public hierarchy is:

`Country -> Region -> City -> Place`

The public site is moving away from the transitional `features.main` static
surface toward a DB-backed `Page + typed blocks` content platform.

## Stack

- Django 5
- codex-django and codex-core from `C:/install/projects/codex_tools/`
- django-unfold admin
- django-allauth
- django-modeltranslation
- Redis-backed codex-django settings/cache helpers
- pytest, ruff, mypy, django-stubs for development checks

## Project Skills

Read these before architectural or feature work:

- `docs/agent-skills/architecture/SKILL.md`
- `docs/agent-skills/design-system/SKILL.md`
- `docs/agent-skills/feature-slice/SKILL.md`
- `docs/agent-skills/page-blocks/SKILL.md`

## Architecture Docs

- `docs/architecture/README.md`
- `docs/architecture/content-platform.md`
- `docs/architecture/feature-slice.md`

Layer rules:

- Views are thin.
- Selectors own reads and template-context assembly.
- Services own writes, orchestration, and side effects.
- Do not place heavy business logic directly in Django views.

## Design

- `docs/design/README.md`
- `docs/design/page-inventory.md`
- Static prototypes: `Design System/ui_kits/web/`
- Preview references: `docs/design/preview/`

The visual direction is editorial travel: Fraunces, Inter, Playfair Display
Italic, warm neutrals, bronze accents, and forest dark surfaces.

## Library References

- codex-django library: `C:/install/projects/codex_tools/codex-django/src/codex_django/`
- Always grep the codex-django library before creating local mixins.
- Reuse library model mixins where available; project-local mixins should stay
  thin and domain-specific.

## Commands

- Django command entry point: `uv run manage <cmd>`
- Tests: `uv run pytest <path>`
- Ruff: `uv run ruff check src tests`
- Mypy: `uv run mypy <path>`

Ruff is configured in `pyproject.toml` with line length 120. Per-file ignores
currently exclude generated feature migrations from `RUF012`.

## Transitional Code

`src/atlas/features/main/` is transitional. Do not add more static public-page
logic there. Static prototype templates should be absorbed into `features.content`
and supporting feature slices such as `features.contacts`.
