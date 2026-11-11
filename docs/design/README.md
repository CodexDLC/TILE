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

## City Library — decision of 6 November 2026

The first home variant is a city bookshelf, grouped by existing regions. Desktop/tablet shows upright spines, with reliefs on fuller volumes; below 768 px the same upright books become smaller and retain their reliefs. The author explicitly replaced the earlier horizontal-stack proposal on 6 November 2026. The current visual study uses a multi-level dark-walnut cabinet in a bright, softly lit reading room, with supplied binding images and independently rendered relief, title and count layers. Thickness and numbers reflect published stories, not city population. Search, region selection and pagination support a growing catalogue. Exact proximity and thematic selections are future work, not simulated controls. Existing editorial colors, templates and public routes remain in use. See [acceptance evidence](library-acceptance.md) and PR-10–PR-13 in [product requirements](../PRODUCT_REQUIREMENTS.md).

### Book composition refinement of 6 November 2026

The hero and search now form the cabinet's wooden crown and inset catalogue panel. The room is lighter, with a single soft sunbeam from the left spanning the complete furniture block. Local Cormorant Infant regular / italic provides the proposed historical book lettering; font files, OFL license and provenance are in `static/fonts/cormorant-infant/`. Spine artwork keeps its full height, with bowed rounded caps rather than clipped rectangular ends.


Books touch with no horizontal gap and align left when a shelf is not full. A uniformly lit walnut bay replaces the previous per-row highlight; one diffuse light wash is applied over the entire cabinet, including books. Supplied complete city cover artwork can serve as the art layer for faithful relief proportions; live title and count sit on an independent plain leather label field, below a divider and clear of the gold bands. The reference for this arrangement is the supplied Quedlinburg cover. Upright smaller mobile books remain in use.

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
