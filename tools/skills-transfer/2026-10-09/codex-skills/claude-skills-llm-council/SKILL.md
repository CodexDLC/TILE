---
name: llm-council
description: Five-perspective advice with anonymous peer review for consequential decisions. Use on explicit council, war room, pressure-test or debate requests, or real high-cost tradeoffs; skip factual lookups, ordinary bugs and minor choices.
---

# LLM Council

Use five independent perspectives and anonymous peer review to examine consequential uncertainty. This is decision support, not permission to implement the verdict.

1. Frame a neutral decision with the user's constraints, stakes and relevant evidence. Read only pertinent authorized context; do not sweep memory or unrelated projects. Clarify a missing fact only when it materially blocks analysis.
2. Read [protocol.md](references/protocol.md) for the council stages and [advisor-lenses.md](references/advisor-lenses.md) for the five perspectives. Use available agents and the existing delegation policy. Run independent advisors and peer reviewers in parallel when budget and available concurrency support it; use isolated batches when constrained. No helper may delegate further.
3. Collect independent advice, anonymize and randomize responses A–E for peer review, then synthesize agreement, disagreement, blind spots, a justified recommendation and one concrete next step. Read [prompts.md](references/prompts.md) when preparing dispatches.
4. Present the verdict in chat. Save a transcript only when authorized, to the agreed location; do not generate reports or project files by default.

Preserve uncertainty: agreement is not proof, peer review is not factual validation, and a strong dissent can outweigh a majority. Never claim independent agents, anonymous review or a completed council when those stages did not run. Report partial execution and unavailable capabilities. Collect every dispatched result and stop unfinished workers before completing; do not invent a cleanup tool or leave fire-and-forget work.

Read references only after deciding the council is warranted. Do not invoke the council merely because ordinary work mentions architecture or asks for validation without a meaningful tradeoff.
