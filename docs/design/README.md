# Atlas Design System

## Role
This directory is the project-local design reference for Atlas. It is adapted from the root-level `Design System` source material so architecture docs, future agents, and production work can reference one documentation area under `docs/`.

## Important Note
The HTML and CSS artifacts in this directory are static prototypes.

They are not the final production implementation.

Production pages must be:
- rendered from DB-backed content
- assembled from reusable typed section data
- aligned with the shared `Page + typed blocks` public-site architecture

## Prototype Coverage
The current prototype set covers:
- home
- country
- region
- city
- place
- map view
- grid view
- search

These represent the future public site surface, but they should be implemented as dynamic Django pages and supporting features rather than static template copies.

## Visual Direction
Atlas is an editorial travel product with:
- warm neutral backgrounds
- bronze as the main interactive accent
- forest green for dark surfaces
- typography built around Fraunces, Inter, and Playfair Display Italic
- restrained motion
- strong use of narrative spacing and long-form composition

## Main Rules
- Avoid generic SaaS styling.
- Preserve the editorial tone and typography hierarchy from the prototype set.
- Use bronze for emphasis and interaction; do not drift into random accent colors.
- Keep motion meaningful and restrained.
- Prefer texture, rhythm, and typography over heavy shadows or over-rounded cards.
- Reuse component patterns from the prototype library before inventing new ones.

## Directory Map
- `preview/` contains token and component examples
- `ui-kit/web/` contains the page prototypes
- `colors_and_type.css` contains copied token and typography references
- `SKILL.md` is the original imported design-system skill source from the prototype package
- [page-inventory.md](./page-inventory.md) maps the prototypes to future dynamic page behavior

## Canonical References
For agent-facing rules, see:
- `docs/agent-skills/design-system/SKILL.md`

For implementation direction, see:
- `docs/architecture/README.md`
- `docs/architecture/content-platform.md`
