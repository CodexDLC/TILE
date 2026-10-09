# Dispatch templates

Use tool names and model identifiers actually available in this harness. These are prompt templates, not executable API calls.

## Advisor

```text
Analyze the decision below independently through the [lens] perspective.
Decision, evidence, constraints and unknowns: [neutral packet]
Focus: [lens description]
Give concrete arguments in roughly 150–300 words. Distinguish facts from assumptions and do not invent certainty. You have no access to other advisors' outputs. Do not delegate, change files or take external actions.
```

## Peer reviewer

```text
Review these anonymized responses to the same decision.
Decision and evidence: [neutral packet]
Responses A–E: [anonymized advice]
In under 200 words identify the strongest response and why, the response with the largest blind spot, and what all five missed. Refer to letters, judge reasoning and evidence, and do not guess advisor identities. Do not delegate or take external actions.
```

## Chair

```text
Synthesize the original decision and evidence, the five advisor responses and the five anonymous reviews. Present agreement, disagreements and their assumptions, caught blind spots, a supported recommendation and one first step. A majority is not proof; prefer the strongest evidence. Disclose missing stages and unresolved uncertainty. Do not execute the recommendation or save files without authorization.
```
