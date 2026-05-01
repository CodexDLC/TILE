# Atlas Editorial — Design System

**A travel aggregator with editorial depth.** Not dry listings — long-form encyclopedic storytelling where each destination is a chapter.

## Product Context

### What It Is
Atlas Editorial is a travel platform structured as an encyclopedia of wandering:

```
Country → Region → City → Place of Interest
(Germany → Bavaria → Munich → Marienplatz)
```

Each level is presented as a narrative article, not a data sheet. Think: National Geographic meets Kinfolk meets Atlas Obscura.

### Target Audience
- Ages 30–55, values history/culture/architecture over beach resorts
- Reads long-form content; appreciates literary travel writing
- Expects good typography and visual refinement

### Technical Stack
- Django templates + Alpine.js + HTMX
- Static HTML prototypes are the design deliverable (converted to Django later)

### Source Materials Provided
- `DESIGN_SYSTEM.md` — Complete brand spec (palette, typography, components, voice) — pasted by user
- `bavaria.html` — Working prototype of a Bavaria region page — pasted by user
- No Figma link or codebase repository attached

---

## Content Fundamentals

### Voice & Tone
**Contemplative, not breathless.** Literary and precise.

- ✅ "Where mad kings built impossible castles, where beer halls outnumber churches"
- ❌ "OMG you HAVE to see this!"

**Rules:**
- **Specific details** over generic adjectives — name the architect, the year, the irony
- **Historical depth** — every place has layers, give context
- **Admit uncertainty** — "Some say," "legends claim," "no one has fully explained"
- **Restraint** — never more than necessary; white space in prose as much as layout
- **Slow travel** — itineraries are for the "unhurried traveler"

### Casing & Formatting
- Section labels: ALL CAPS, letter-spacing 0.24em, Inter 500
- Chapter labels: "Chapter Seven · Southern Germany · Alpine Region" — title case, bronze dots as separators
- Card numbers: "N°01 · Bayern" — Fraunces Italic
- Marginalia: "Marginalia № 01" — ALL CAPS label, then Fraunces Italic text
- Layer tabs: Roman numerals — "I. Overview · II. History · III. Getting There"

### No Emoji Policy
No emoji in body copy or UI. The 🌍 globe appears only in breadcrumbs (as a geographic anchor). Otherwise, decorative elements are typographic or SVG.

---

## Visual Foundations

### Color System
The palette is warm neutrals anchored by parchment, bronze accents, and forest green for dark sections.

| Token | Hex | Use |
|-------|-----|-----|
| `--bg` | `#F5EFE3` | Main body background (warm champagne) |
| `--bg-warm` | `#EFE7D5` | Alternating sections (e.g. regions grid) |
| `--bg-paper` | `#FAF6EC` | Cards, overlays, lightest surface |
| `--ink` | `#1A1D23` | Body text (near-black graphite) |
| `--ink-soft` | `#3A3D44` | Secondary text |
| `--ink-muted` | `#6B6860` | Metadata, captions, muted |
| `--bronze` | `#A67A3F` | Primary accent — all interactive highlights |
| `--bronze-deep` | `#8B6330` | Hover state for bronze |
| `--forest` | `#2C3E3A` | Dark sections (footer, CTA strip) |
| `--line` | `rgba(26,29,35,0.12)` | Borders |
| `--line-soft` | `rgba(26,29,35,0.06)` | Ultra-subtle dividers |

**Color philosophy:** Warm neutrals dominate. Bronze replaces typical orange/blue travel clichés. Dark sections use forest green, not pure black.

### Typography
Three families, each with a distinct role:

| Family | Role | Weights |
|--------|------|---------|
| **Fraunces** (Variable, Google Fonts) | Display, editorial body, pull quotes, all headlines | 300–600, Italic variants |
| **Inter** (Google Fonts) | UI only: nav, labels, metadata, breadcrumbs, buttons | 300–600 |
| **Playfair Display Italic** (Google Fonts) | Pull-quotes exclusively | 400–500 Italic |

**Type scale:**
- Hero title: `clamp(56px, 9vw, 132px)` / line-height 0.92 / Fraunces 400
- Section title: 56px / 1.0 / Fraunces 400
- Article title: 52px / 1.05 / Fraunces 400
- Subsection: 32px / 1.15 / Fraunces 400
- Editorial body: 19px / 1.65 / Fraunces 400
- Standard body: 16px / 1.6 / Inter 400
- Pull quote: 32px / 1.3 / Playfair Display Italic
- Labels/metadata: 11–13px / Inter 500 / letter-spacing 0.16–0.24em / UPPERCASE

**Special treatments:**
- **Drop cap:** 96px Fraunces Italic, bronze, float left — first paragraph of long articles
- **Pull quotes:** Top/bottom borders, giant decorative `"` (100px, bronze, 0.3 opacity)
- **Marginalia:** 15px Fraunces Italic, bronze left border 2px, sticky on desktop

### Backgrounds & Texture
- **Paper noise texture:** SVG fractalNoise overlay on `body::before`, 35% opacity, fixed — gives parchment feel
- **Hero backgrounds:** Dark gradient (`--forest` tones) with inline SVG mountain silhouettes layered
- **Section alternation:** `--bg` (default) ↔ `--bg-warm` (sections like regions grid)
- No photography used as section backgrounds (except hero); no full-bleed page backgrounds

### Imagery
- Source: Unsplash (travel, architecture, nature)
- Cards use `object-fit: cover` with gradient overlay: `linear-gradient(to top, rgba(15,24,20,0.92), rgba(15,24,20,0.1))`
- Images are warm-toned landscapes, historic architecture
- Aspect ratios: 16/11 (featured region), 4/5 (secondary regions), 5/6 (place cards)

### Spacing System
```
Micro:  4, 6, 8px
Small:  12, 16, 20px
Medium: 24, 32, 40px
Large:  60, 80, 100px
XL:     120px (section padding)
```

### Layout & Grid
- Max content width: **1400px**, 40px horizontal padding (24px mobile)
- Editorial column: **680px** centered
- Three-column editorial: `1fr 680px 1fr`
- Regions: 12-column asymmetric grid (7+5, 4+3 span patterns)
- Places: symmetric 3-column

### Corner Radii
- Cards: `4px` (very subtle)
- Buttons/pills: `100px` (fully rounded)
- Badges: `100px`
- No large border-radius cards (no 12px+ rounded cards)

### Shadows & Elevation
- Essentially shadowless — depth created by gradient overlays and background alternation, not box-shadow
- Headers use `backdrop-filter: blur(12px)` with semi-transparent background

### Borders
- `--line`: `rgba(26,29,35,0.12)` — card borders, section dividers
- `--line-soft`: `rgba(26,29,35,0.06)` — ultra-subtle
- Marginalia: 2px solid `--bronze` left border
- Pull quotes: 1px `--line` top/bottom

### Animation & Motion
- Entrance: `fadeUp` — `opacity 0→1`, `translateY(30px→0)`, staggered (0.2s, 0.4s, 0.6s, 0.8s)
- Card hover: `translateY(-4px)` + image `scale(1.05)`, 0.5s cubic-bezier
- CTA hover: `translateX(6px)`
- Region arrow hover: `rotate(-45deg)` + fills bronze
- Reading progress bar: 2px bronze line, top of viewport
- Easing: `cubic-bezier(0.2, 0.8, 0.2, 1)` for cards, `ease` for UI
- Duration: 0.2–0.3s UI, 0.5–0.8s images
- Philosophy: **Restraint** — meaningful motion only

### Hover States
- Links: bronze color shift + underline
- Cards: `translateY(-4px)` lift
- Icon buttons: fill ink, invert color
- Nav links: bronze underline
- Footer links: opacity 75% → 100% + bronze

### Icons
No custom icon font. Uses minimal inline SVG — Feather/Lucide-style strokes (16–18px, 2px stroke-width). See ICONOGRAPHY section.

---

## Iconography

### Approach
**Inline SVG only.** No icon font, no sprite sheet, no emoji (except 🌍 in breadcrumbs).

### Style
- Stroke-based, no fills
- 2px stroke-width
- 16–18px render size
- Set in icon buttons (`38px` circle containers)
- Color: inherits from parent (`currentColor`)

### Icons Used (from bavaria.html)
| Icon | Usage |
|------|-------|
| Search (circle + line) | Header search button |
| Bookmark (path) | Header save button |
| Text lines (4 lines) | Story view switcher |
| Map (path) | Map view switcher |
| Grid (4 squares) | Grid view switcher |
| Arrow NE (path) | Region card link arrow |
| Arrow right (path) | CTA button |

### CDN Substitution
Since no icon font/sprite was provided, icons are hand-coded inline SVG using Feather icon geometry. **Flag:** If the production codebase uses a specific icon set, replace these with the correct references.

---

## Assets

```
assets/           — logos, brand SVGs
fonts/            — Google Fonts used via CDN (see below)
preview/          — design system card HTML files
ui_kits/web/      — full UI kit for the travel editorial web app
```

### Fonts (Google Fonts CDN)
All fonts loaded via Google Fonts. No local font files provided.
```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;1,9..144,400&family=Inter:wght@300;400;500;600&family=Playfair+Display:ital,wght@1,400;1,500&display=swap" rel="stylesheet">
```

---

## File Index

| File | Description |
|------|-------------|
| `README.md` | This file — full design system documentation |
| `colors_and_type.css` | CSS custom properties for all tokens |
| `SKILL.md` | Agent skill definition |
| `preview/colors-primary.html` | Primary color palette swatches |
| `preview/colors-semantic.html` | Semantic/utility color tokens |
| `preview/type-scale.html` | Full type scale specimen |
| `preview/type-editorial.html` | Editorial components (drop cap, pull quote, marginalia) |
| `preview/spacing-tokens.html` | Spacing scale tokens |
| `preview/spacing-layout.html` | Layout grid and column system |
| `preview/components-nav.html` | Header, breadcrumb, view switcher |
| `preview/components-hero.html` | Hero section pattern |
| `preview/components-cards.html` | Region and place cards |
| `preview/components-buttons.html` | Buttons, icon buttons, badges |
| `preview/components-editorial.html` | Pull quote, margin note, layer tabs |
| `ui_kits/web/index.html` | Full interactive UI kit — Bavaria region page |
