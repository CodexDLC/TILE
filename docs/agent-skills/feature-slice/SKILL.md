---
name: atlas-feature-slice
description: Load this skill when adding or refactoring Atlas feature modules. Covers package layout, file ownership, and selector/service usage.
---

Read:
- `docs/architecture/feature-slice.md`

Default feature structure:
- `models/`
- `views/`
- `selectors/`
- `services/`
- `tests/`
- optional `admin/`, `forms/`, `templates/`, `urls.py`

Rules:
- Use package-based modules for non-trivial features.
- Split files by domain topic or main class when the surface grows.
- Route reads through selectors.
- Route writes through services.
- Keep views thin and declarative.
- Do not create giant `models.py` or `views.py` files when the feature is already complex.

Atlas-specific reminder:
- New public-site functionality should reinforce the shared content-platform direction instead of adding isolated static page code.
