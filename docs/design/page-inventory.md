# Page Inventory

## Purpose
This inventory maps the current static prototype pages to the future dynamic Atlas site architecture.

## Prototype To Runtime Mapping
### Home
- Prototype: `ui-kit/web/home.html`
- Runtime role: editorial homepage assembled from featured page records and reusable content blocks
- Likely sections: hero, featured destinations, editorial intro, thematic collections, CTA

### Country
- Prototype: `ui-kit/web/country.html`
- Runtime role: `Page` with country type
- Likely sections: hero, introduction, regions grid, featured places, journey CTA

### Region
- Prototype: `ui-kit/web/region.html`
- Runtime role: `Page` with region type
- Likely sections: hero, cities grid, layer tabs, places grid, practical content

### City
- Prototype: `ui-kit/web/city.html`
- Runtime role: `Page` with city type
- Likely sections: skyline hero, editorial body, neighborhood or district navigation, places list, practical sidebars

### Place
- Prototype: `ui-kit/web/place.html`
- Runtime role: `Page` with place type
- Likely sections: full-bleed hero, long-form story, facts, gallery, seasonality, nearby places

### Map View
- Prototype: `ui-kit/web/map-view.html`
- Runtime role: supporting feature that consumes shared page/place data
- Likely responsibilities: filtered map interface, place markers, sidebar results

### Grid View
- Prototype: `ui-kit/web/grid-view.html`
- Runtime role: supporting feature that consumes shared page/place data
- Likely responsibilities: filter bar, search/filter state, card grid, pagination

### Search
- Prototype: `ui-kit/web/search.html`
- Runtime role: supporting search feature
- Likely responsibilities: query parsing, filters, hybrid result layouts, pagination

## Reusable Content Sections
The prototype set suggests a reusable block library rather than template-only layouts. Candidate reusable sections include:
- hero
- breadcrumb/meta band
- editorial rich text
- pull quote
- margin note
- places grid
- regions grid
- cities grid
- facts/stat list
- tabs/layers navigation
- CTA strip

## Implementation Reminder
Do not translate these pages into one-template-per-prototype without a shared content model.

The target architecture remains:
- hierarchical `Page` records for route ownership
- typed blocks for body composition
- separate supporting features for search/map/forms when behavior is specialized
