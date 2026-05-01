# Atlas Map

## Status
The Atlas map is a future feature, not part of the current public prototype.

Do not expose map navigation in the public header until the feature has real
content, filtering, and a useful reader workflow. The existing `/places/map/`
route may remain as a technical placeholder, but it should not be promoted to
users yet.

## Target Direction
The long-term target is a branded interactive map built with MapLibre GL and
vector tiles.

MapLibre is preferred over an immediate Google Maps integration because Atlas
is an editorial guide, not only a utility directory. A custom map style can
match the site's warm neutral, bronze, and forest visual language while still
supporting practical exploration.

## Data Contract To Keep
Keep map-ready data in the domain models:

- `Place.latitude`
- `Place.longitude`
- country, region, and city relationships
- future place type/category fields
- future season and topic filters

The current starter fixtures already include coordinates for seeded places.

## Future Feature Scope
When there are enough places to justify a map, implement a dedicated Atlas Map
feature with:

- JSON endpoint for map places
- filtering by country, region, city, place type, and season
- clustering for dense areas
- context-aware map entry points from country, region, and city pages
- list fallback for mobile and accessibility
- tile provider or tile hosting decision
- MapLibre style aligned with the Atlas design system

## Non-Goals For Now
Do not build custom map tiles, map controls, or Google Maps integration during
the current content-platform foundation work.

Do not add a global `Map` item to the public header while the map is still a
placeholder.
