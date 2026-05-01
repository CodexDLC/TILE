# Content Platform

## Goal
Atlas needs one shared public content platform that can render all editorial page levels dynamically from the database without creating a separate hard-coded app for every page type.

## Base Interface
The initial platform contract is:
- `Page + typed blocks`

This means:
- one shared hierarchical `Page` model owns routing and common page metadata
- reusable typed content blocks/sections assemble the body of each page
- domain-specific experiences build on the same contract rather than bypassing it

## Page Model Responsibilities
The shared `Page` model should own:
- hierarchy and parent-child relationships
- slug and canonical path ownership
- page type classification
- SEO binding
- publication state
- template/view resolution hints

The hierarchy must support:
- country pages
- region pages
- city pages
- place pages

## Typed Blocks
Page bodies should be assembled from typed blocks/sections stored in the database. Examples include:
- hero
- editorial introduction
- rich text narrative
- pull quote
- quick facts
- card grid
- related places
- map entry point
- CTA strip

The important rule is not the exact block list. The important rule is that production pages are assembled from reusable typed sections, not from template-specific hard-coded markup.

## Supporting Features
Some surfaces are better modeled as supporting features rather than inline page blocks:
- search
- map views
- contact/forms

These features may have their own routes, selectors, services, and templates, but they should still:
- resolve against the shared page hierarchy where relevant
- reuse the same editorial content and metadata
- avoid forking a second content model

Map views are intentionally hidden from public navigation until the Atlas Map
feature is useful. Keep coordinates on `Place`, but treat the map as a future
MapLibre GL feature documented in [Atlas Map](./atlas-map.md).

## Routing Direction
The content platform should support route resolution across the public hierarchy:

`Country -> Region -> City -> Place`

The route layer should resolve the page object first, then use selectors to assemble the template context.

## Relationship To Existing Code
The current `features.main` app serves static templates. It should not remain a permanent static landing-page bucket. It should be evolved or replaced by a public-site/content feature that implements:
- shared page lookup
- template selection
- typed-block rendering
- dynamic page context assembly

## Non-Goals For This Pass
This document does not freeze:
- the exact Django model fields
- admin UX
- migration sequence
- block storage format

It only locks the architectural direction so future implementation work stays consistent.
