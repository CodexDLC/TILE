# Atlas

Atlas is an editorial travel guide: a hybrid between a structured destination
aggregator and a light editorial blog. The public hierarchy is:

`Country -> Region -> City -> Place`

The public site is moving away from the transitional `features.main` static
surface toward a DB-backed `Page + typed blocks` content platform.

## Stack

- Django 6.0 (6.0.4 in the current lock-file)
- Python 3.14 and dependencies from PyPI, pinned by `uv.lock`
- codex-ai 0.2.6, codex-core 0.5.0, codex-django 0.7.0,
  codex-django-cli 0.4.0, codex-platform 0.6.0, codex-services 0.1.4
- django-unfold admin
- django-allauth
- django-modeltranslation
- Redis-backed codex-django settings/cache helpers
- pytest, ruff, mypy, django-stubs for development checks

## Project Skills

Read these before architectural or feature work:

- `.agents/skills/atlas-architecture/SKILL.md`
- `.agents/skills/atlas-design-system/SKILL.md`
- `.agents/skills/atlas-change-triage/SKILL.md`
- `.agents/skills/atlas-page-blocks/SKILL.md`

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

- Read the installed codex-django usage skill and relevant source in the project's
  `.venv` before creating local mixins or changing library integration.
- Local `codex_tools` checkouts are not required by this project's installation.
- Reuse library model mixins where available; project-local mixins should stay
  thin and domain-specific.

## Commands

- Install: `uv sync --locked --extra dev`
- Django command entry point: `uv run --locked --extra dev manage <cmd>`
- Tests: `uv run --locked --extra dev pytest <path>`
- Ruff: `uv run --locked --extra dev ruff check src tests`
- Mypy: `uv run --locked --extra dev mypy <path>`

The PyPI installation and site tests were checked in the developer's environment
on 2026-10-10. Installation and the author workflow on the new computer remain
unverified; record those checks separately.

Ruff is configured in `pyproject.toml` with line length 120. Per-file ignores
currently exclude generated feature migrations from `RUF012`.

## Transitional Code

`src/atlas/features/main/` is transitional. Do not add more static public-page
logic there. Static prototype templates should be absorbed into `features.content`
and supporting feature slices such as `features.contacts`.
