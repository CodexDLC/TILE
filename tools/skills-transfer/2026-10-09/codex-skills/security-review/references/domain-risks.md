# Domain-specific review prompts

## Browser game

Treat the browser as attacker controlled. Identify authoritative state for scores, rewards, inventory, match results, and purchases; review replay, timing, forged events, race conditions, and abuse limits. Assess websocket/session authorization and whether one player can affect another's state. Rank client tampering by actual economic or competitive effect, not by its mere possibility.

## Multi-tenant CRM

Trace tenant identity from authentication through queries, background jobs, exports, search, attachments, caches, and admin tools. Check whether object IDs, filters, bulk operations, and indirect relationships can cross tenant boundaries. Include invited users, role changes, support impersonation, and webhook/integration credentials. A successful login alone does not establish permission to a record.

## Payments and webhooks

For incoming payment webhooks, verify the provider signature over the exact raw body using the provider's documented method, with appropriate secret rotation and replay controls. Authenticate event type and object/account identity before changing state. Persist event processing or business-transition keys so duplicate, delayed, reordered, or concurrent deliveries cannot charge, fulfill, credit, or refund twice. Confirm amounts, currencies, and order ownership against server-side records; do not trust browser success pages as payment proof. Use provider sandbox or local fixtures for validation unless live tests are explicitly authorized.

Primary guidance:

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP Webhook Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Webhook_Security_Cheat_Sheet.html)
