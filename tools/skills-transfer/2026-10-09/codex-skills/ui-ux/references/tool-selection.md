# Tool and Component Selection: Server Templates

Use the project's current server-rendered stack. Inspect its component library before recommending dependencies.

## Foundations
- Django Templates or Jinja2 renders semantic HTML. Native form controls provide the baseline; use the existing CSS and icon families.
- Shared includes/macros/components own reusable markup and behavior contracts. Site-level theme tokens supply brand choices. Page-local rules do not redefine shared primitives.
- HTMX handles authorized server requests, partial rendering and meaningful URL/history updates. Keep canonical validation and permissions on the server. Design loading, failure/retry and success feedback; preserve user input on errors.
- Alpine handles expanded/collapsed state, local tabs, temporary selection and menus. Avoid a parallel client domain store or speculative offline sync.
- Tables use server-side queries, filters, sort and pagination when volume warrants them. Selection and bulk actions are included only when requested and backed by real policies/services. Preserve search state on return to the collection.
- Use the project's existing chart tool. Add a chart only when it helps the user's decision.

## Browser verification
Use available browser tooling or Playwright for desktop/mobile, keyboard operation, focus, HTMX swaps, long translations and recovery. A component showcase rendered by the actual template engine can serve as a catalog; Storybook is not required. Use automated accessibility checks when available; supplement them with interaction evidence.

Do not recommend React, Vue, Next.js, shadcn, TanStack or a stack migration merely to follow an example. If the user explicitly requests a different stack, follow that request and re-evaluate the foundation.
