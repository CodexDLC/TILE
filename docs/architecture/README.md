# Atlas Architecture

## Purpose
This project is evolving from a generated `codex-django` scaffold into a dynamic editorial travel site. The public website must not stay a set of static templates. It should render all public-facing pages from database-backed content using a shared content platform.

## Core Direction
- All public pages are dynamic and assembled from database content.
- The primary hierarchy is `Country -> Region -> City -> Place`.
- The first implementation path is a shared content architecture, not separate hard-coded page apps.
- Search, map, and forms may live in separate supporting features, but they must consume the same content platform and route hierarchy.

## Project Boundaries
- `core` owns project-wide Django configuration, settings, URLs, and generic runtime integration.
- `system` owns cross-site models and workflows that belong to the whole project.
- `features` owns product-specific behavior and public-site feature modules.

`system` must not become the home for editorial page-domain logic. Country, region, city, place, and page-composition behavior belong in a public-site/content feature.

## Public Site Direction
The current `features.main` app is still a static template surface. It should evolve into the shared public-site content feature or be replaced by a dedicated feature with the same responsibilities:
- public route resolution
- page retrieval
- template/context assembly
- rendering of reusable sections

## Layer Responsibilities
### Views
Views stay thin. They are responsible for:
- request parsing
- calling selectors/services
- returning template or HTTP responses

Views must not contain heavy business rules, cross-feature orchestration, or complex query composition.

### Selectors
Selectors own the read path:
- query composition
- prefetch/select-related strategy
- DTO/context assembly for templates
- reusable read entry points for views and other features

Read path convention:

`view -> selector -> template context`

### Services
Services own the write and orchestration path:
- state changes
- transactions
- side effects
- cross-feature workflows
- admin/action driven mutations

Write path convention:

`view/admin/action -> service -> models/side effects`

### Models
Models own persistence and domain structure. When the surface becomes non-trivial, split them into `models/` package files by topic or class instead of growing a large `models.py`.

## Structural Conventions
Larger features should use package-based layout:
- `models/`
- `views/`
- `selectors/`
- `services/`
- `tests/`
- optional `admin/`, `forms/`, `templates/`, `urls.py`

The project already hints at this structure in `features.conversations` and `system`. New work should continue in that direction consistently.

## Related Documents
- [Content Platform](./content-platform.md)
- [Feature Slice](./feature-slice.md)
- [Design System](../design/README.md)
