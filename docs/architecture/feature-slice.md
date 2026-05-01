# Feature Slice Conventions

## Intent
Atlas uses feature-oriented Django apps. Each feature should own its behavior end-to-end instead of scattering domain logic across unrelated global modules.

## Standard Layout
For larger or evolving features, prefer:

```text
feature_name/
  admin/
  forms/
  models/
  selectors/
  services/
  tests/
  views/
  urls.py
```

Use flat single files only when the surface is genuinely small. Once a module starts collecting multiple concepts, split it into package files by topic or class.

## Responsibilities
### `views/`
- thin HTTP entry points only
- call selectors for reads
- call services for writes
- return rendered responses or redirects

Never hide business-heavy code directly in Django CBVs/function views.

### `selectors/`
- read-only query logic
- list/detail retrieval
- prefetch/select-related tuning
- context assembly for templates, admin dashboards, or APIs

Selectors should be safe to call from views or other services when read access is needed.

### `services/`
- writes and mutations
- orchestration across models
- transactions
- side effects such as notifications, cache invalidation, or workflow triggers

### `models/`
- persistence layer
- domain entities
- model methods only when behavior is naturally local to that entity

For non-trivial features, prefer one file per model or tightly related model cluster.

### `tests/`
Split tests by behavior rather than by framework convenience. At minimum, cover:
- selector behavior
- service behavior
- view integration for critical public routes or actions

## Naming Guidance
- Name modules by domain topic, not by generic suffix-heavy buckets.
- Use singular model filenames when one file owns one main model.
- Keep selector and service names explicit about the operation they perform.

## Atlas-Specific Rules
- Public editorial page logic belongs in a public-site/content feature, not in `system`.
- `system` remains reserved for shared site-wide concerns.
- `features.main` should move toward dynamic page delivery instead of accumulating more static page views.
- All public-site read composition should flow through selectors.
- All public-site mutations should flow through services.

## Existing Project Alignment
The current codebase already points in the right direction:
- `features.conversations` uses `models/`, `views/`, `selector/`, and `services/`
- `system` uses package-based `models/`, `selectors/`, and `services/`

This document makes that pattern the default rule for future features.
