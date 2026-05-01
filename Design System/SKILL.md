---
name: atlas-editorial-design
description: Use this skill to generate well-branded interfaces and assets for Atlas Editorial, a travel aggregator with editorial depth. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping all 7 page types (Country, Region, City, Place, Map View, Grid View, Search).
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

Key files to read first:
- README.md — full brand context, visual foundations, content voice
- colors_and_type.css — all CSS custom properties (colors, type, spacing, animation tokens)
- ui_kits/web/_base.css — shared component styles used across all 7 pages
- ui_kits/web/index.html — UI kit index with links to all 7 page prototypes

Design system essentials:
- Background: #F5EFE3 (warm champagne) with SVG paper texture overlay
- Accent: #A67A3F (bronze) — all interactive elements, labels, accents
- Dark sections: #2C3E3A (forest green) — footer, hero, CTA strip
- Fonts: Fraunces (serif, editorial + display) + Inter (sans, UI only) + Playfair Display (pull-quotes only)
- Cards: 4px radius, gradient overlays, translateY(-4px) hover lift
- Buttons: 100px border-radius pills, bronze fill or outline
- Hero: Dark forest gradient + inline SVG mountain silhouettes
- Editorial: 3-col grid (1fr 680px 1fr), drop caps, pull quotes, sticky margin notes

Page hierarchy: Country → Region → City → Place of Interest
All pages share: sticky header (blur), breadcrumb bar, view switcher (Story/Map/Grid), reading progress bar, forest-green footer.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.
