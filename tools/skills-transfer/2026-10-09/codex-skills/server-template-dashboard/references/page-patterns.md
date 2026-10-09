# Page Patterns

Choose only the patterns needed for the user's task and existing capabilities.

## Collection and table
Compact title/count and a primary create action when allowed; search/filter controls where required; semantic table headings; clear row navigation/actions; empty versus no-results states; pagination or an appropriate server query for large data. Preserve meaningful query state in the URL. Render visible labels or accessible names for controls. If bulk work is required, distinguish selected rows from hovered rows, define the selection scope and confirm destructive batches with a count. Do not invent batch endpoints or permissions.

For narrow screens choose by task: retain horizontal scrolling for genuinely comparative data, prioritize columns, or present accessible cards with the same actions. Do not mechanically shrink the desktop table or assume every table must become cards.

## Overview
Show actionable metrics, exceptions and links to work. Charts and recent activity are appropriate only when backed by real data and decisions. Avoid decorative metric walls.

## Inbox / queue
Keep the pending item and next action obvious. A split panel can preserve list position. Search, selection, keyboard shortcuts, assignment and bulk actions depend on actual workflow requirements. After an action, communicate the result and keep a useful focus position.

## Detail
Identity and status; actions near their target; related data grouped by meaning; edit paths with server validation; return navigation retaining collection state where relevant. Audit/history is domain-owned, not an automatically generated component requirement.

## Form and settings
Visible labels associated with controls, hints/errors connected by identifiers, required indicators, safe defaults, server validation, preserved input on failure, primary submit plus safe cancel and clear success feedback. Use a dedicated page for long tasks; a modal only when interruption/protected focus is useful. Avoid giant forms when progressive grouping makes the task clearer.

## Dialog and asynchronous state
Use dialog semantics, an accessible name, initial focus, appropriate focus containment, safe Escape behavior and focus restoration. HTMX updates must retain coherent Alpine lifecycle, announcements and recovery. Prevent duplicate writes where needed; the server remains authoritative. Do not introduce optimistic or offline behavior without a defined failure/conflict policy.

## Tokens and component catalog
Define semantic roles through existing tokens: canvas/surface/text/muted/border/accent, success/warning/error, focus/disabled/selected, spacing/type/radius/layers. Preserve approved theme values. A real template-rendered showcase can document component states without adding a frontend framework.
