---
name: frontend-design-codex
description: "Build, refine or verify server-rendered HTML interfaces and reusable cabinet components with semantic tokens and browser evidence. Preserve Django Templates or Jinja2, HTMX, Alpine and the existing CSS system. Use for responsive layouts, forms, dashboards and visual QA; skip backend-only work."
---

## Owner's server-template development mode

This installation is adapted for the owner's reusable cabinet component libraries and their consuming sites. These instructions govern framework-specific examples elsewhere in this package.

- Use the existing server-rendered HTML stack: Django Templates now; Jinja2 when the target project actually uses it. Use HTMX for server interactions and Alpine.js for local UI state. Do not introduce React, Vue, Next.js, shadcn, a SPA, or a new CSS framework to satisfy this skill. Translate examples into existing template components, native HTML and the installed CSS/icon system.
- A shared library owns reusable components, component contracts and theme extension points. A consuming site owns its brand, domain navigation, terminology and business policies. Do not copy a client's brand or business rules into the general library. Inspect the actual library in each task; do not assume every project uses codex-django.
- Reuse existing templates, includes, tokens and patterns. Server-side authorization, validation and state transitions remain authoritative. Hiding a control is not an access check. Alpine manages transient interaction state, not a duplicate domain model.
- Scope UI work to the user's request. Do not add search, bulk operations, optimistic writes, dashboards, media generation, governance documents or new dependencies merely because an upstream recipe mentions them. Preserve the repository's architecture, testing and compatibility decisions.
- For cabinets/admin/product tools use Operate priorities: clear task, compact hierarchy, readable data, safe actions, recovery and consistency. Preserve approved fonts, palette, icons and density; aesthetic warnings do not override a deliberate theme. Public/marketing pages can use a different composition when requested.
- Report actual verification. Template rendering and Python tests do not prove browser behavior; use appropriate desktop/mobile evidence and keyboard/HTMX checks when the task warrants them. Do not simulate test or tool output.
- Installation of this skill does not authorize installing hooks, scaffolding project documents, modifying global/project configuration, external uploads, or launching bundled subagents. Follow the user's existing authorization and delegation preferences. Hooks remain opt-in per project.

# Frontend Design Codex

## Overview

Use this skill to make browser-rendered product interfaces feel intentional, usable, and verified. Prefer the existing app framework and design conventions before adding new abstractions.

## Design Upskill Contribution

This skill teaches Codex to judge frontend design from rendered behavior rather than source code alone. It improves no-template work by forcing the agent to choose layout, hierarchy, spacing, controls, responsive states, accessibility, and screenshot evidence as one loop.

It matters because product UI without a template can easily become decorative or inconsistent. Codex should make useful interfaces that hold up under repeated use, mobile wrapping, and real browser rendering.

## Workflow

1. Inspect the existing app structure, framework, routes, components, styles, and design conventions.
2. Identify the primary user workflow and optimize the first screen for that workflow.
3. Define semantic design tokens before styling repeated components: background, surface, text, muted text, border, accent, status colors, type, spacing, and radius. Check contrast and keep the palette compact.
4. Build the smallest complete UI that covers normal, empty, loading, error, and narrow viewport states.
5. Use familiar controls: icon buttons for tools, toggles for binary choices, sliders or inputs for numbers, tabs for alternate views, and menus for option sets.
6. Apply the visual tokens consistently to core surfaces, controls, charts, and annotations. Keep typography and layout scaled to the surface; avoid hero-scale text inside compact panels.
7. Capture desktop and mobile screenshots before claiming visual quality.
8. Revise tokens and layout until screenshot evidence supports the design decisions.

## Shared Visual Runtime

The shared visual runtime is bundled at `<skill-base-dir>/runtime/`; resolve it relative to this installed skill, never relative to the target repository. Use its `scripts/` directory for browser evidence:

- `capture_page.mjs` for screenshots, console capture, request failures, and optional PDF export.
- `visual_lint.mjs` for text overflow, low contrast, tiny text, missing image alt text, and console findings.
- `make_contact_sheet.py` when comparing multiple screenshots.
- `runtime/references/design-tokens.md` when creating or auditing a visual system.

No Office COM is required. If this UI is later exported into PowerPoint, Word, or Excel, finish browser QA first and move the Office-specific step to the Office skills.

## Verification

Before completion:

- run the app's normal build/test/lint command when available;
- capture at least desktop and mobile screenshots;
- run visual lint and address blockers;
- inspect screenshots for responsive UI, accessibility, hierarchy, text fit, controls, spacing, palette, typography, and token consistency;
- preserve screenshot evidence and note any accepted tradeoffs.

## Common Mistakes

- Building a landing page when the user asked for a usable app.
- Inventing a visual language that conflicts with the existing app.
- Shrinking text to fix density instead of reducing content.
- Claiming responsive quality without a mobile screenshot.

For authenticated pages, use an authorized test session through the available browser tools. The bundled capture scripts create a fresh browser context and do not log in automatically. Do not capture real customer data into shared artifacts. Treat visual_lint as a heuristic: intentional table scrolling and decorative empty-alt images can be false positives; it is not a WCAG certification. Runtime dependencies: Node.js and Playwright Chromium; Python for contact sheets. See runtime/package.json.

Installation source and local changes: [provenance](references/provenance.md).
