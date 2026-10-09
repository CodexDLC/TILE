---
name: architecture-decision-records
description: Record or retrieve significant architectural decisions as ADRs. Use when asked to document a decision or explain an existing choice; do not create ADRs for routine implementation details.
---

# Architecture Decision Records

Keep the reason for a consequential choice beside the code, with alternatives and consequences.

1. Find the project's existing decision log and conventions. Read matching records before proposing a new one; an old ADR is evidence, not proof of current behavior.
2. For a new record, read [record-format.md](references/record-format.md). Draft from the actual discussion and repository evidence; distinguish proposed decisions from accepted ones. Do not invent deciders, dates, measurements or rejected alternatives.
3. Show the draft before writing unless the user already authorized recording this concrete decision. A request to understand a decision authorizes reading and explanation only. Creating or changing an ADR does not authorize implementing its decision.
4. Use the existing location and numbering. If none exists, propose `docs/adr/`; create the directory and index only within explicit write authorization. Recheck numbering before writing, preserve existing records, and link superseded decisions rather than silently rewriting history.

Keep one decision per record. Update the existing index only when a record is written. Prefer a short answer when the request is merely a factual lookup.
