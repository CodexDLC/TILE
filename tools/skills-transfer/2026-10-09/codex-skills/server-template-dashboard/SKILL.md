---
name: server-template-dashboard
description: Design and improve reusable cabinet/admin/dashboard components and working screens on Django Templates or Jinja2 with HTMX and Alpine. Use for table and form patterns, navigation, density, theme contracts, responsive states and shared-library versus consuming-site ownership. Skip marketing compositions and backend-only work.
---

# Server Template Dashboard

An adaptation of alt-wrk's dashboard-product-design-standard and dashboard-design-system for the owner's server-rendered component-library workflow. See [provenance](references/provenance.md).

## Ownership and stack

- Preserve Django Templates or Jinja2, HTMX, Alpine and the installed CSS/icon system. React, Vue, Next.js, shadcn, Tailwind and Lucide are not prerequisites. Do not change the frontend stack to satisfy a design recipe.
- Inspect the actual library API, templates and consumers before changing a shared component. Library components own neutral structure, behavior and theme extension points; consuming sites own branding, domain vocabulary, navigation choices and business policies.
- Reuse includes/macros, typed context contracts where present, and existing tokens. The backend computes domain data and authorization; templates render; Alpine manages transient UI state; HTMX performs server interactions.
- Respect the project's compatibility policy. Identify affected consumers for contract changes without creating speculative compatibility layers.

## Working interface principles

- Prioritize the current task, status, next action and recovery. Use compact headers, readable data and quiet navigation; density must not reduce text legibility or touch usability.
- Use icon plus concise label navigation. Organize destinations by real workflows while preserving a requested workspace structure. Keep the current location visible.
- Prefer a direct table/list for a collection. Cards are suitable for grouped properties, a side panel or a mobile adaptation, not an obligatory wrapper around every table.
- Put a primary action near the object it affects. Keep destructive actions distinct with appropriate confirmation or undo. Menus are useful for multiple row actions, not mandatory for a single clear action.
- Derive colors, typography, spacing, radii and layers from the existing token system. Map semantic roles to current tokens; do not impose alt-wrk's palette or a client's brand globally. Inspect stylesheet order and compiled/source boundaries before edits.
- Each applicable component covers normal, hover/focus, disabled, loading, empty/no-results, error and permission/read-only states. Read-only status must not look like a clickable button.

## Scope-aware recipes

Read [page patterns](references/page-patterns.md) for the requested page type. Treat patterns as design options, not authorization to add product features. Search, sorting, bulk actions, charts, command palettes, exports, offline queues and optimistic mutations need an actual user requirement and server capability. Do not ship plausible-looking controls wired to stubs.

## Verification

Use the repository's relevant tests. For meaningful UI changes, inspect rendered desktop/mobile output, keyboard/focus behavior, long translated labels, empty/error states and applicable HTMX requests. Do not claim browser QA from template-marker tests. Clearly state unavailable checks. Coordinate with other UX/design skills through one brief and one verification pass instead of repeating gates.
