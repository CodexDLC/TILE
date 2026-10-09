# Candidate review

A candidate should contain:

- **Problem and trigger:** the recurring task or failure and when the instruction should apply.
- **Evidence:** dated task/session identifiers or repository references, observed outcomes and explicit user corrections. Distinguish independent repetitions from retries of one incident.
- **Counterevidence:** exceptions, alternative causes and conditions where the proposed rule would be wrong.
- **Scope and owner:** global capability, domain practice or project fact; existing skill to amend, if any.
- **Proposed instruction:** minimum actionable change, critical boundaries and any conditional references.
- **Cost and conflicts:** added metadata/body size, competing triggers and rules it might contradict.
- **Validation:** realistic activating and non-activating requests, an authorization boundary and expected observable behavior.
- **Disposition:** proposed, accepted, rejected or superseded, with reviewer evidence when known. Do not infer acceptance.

Reject generic advice already supplied by the runtime, temporary environment failures presented as universal rules, unverified workarounds and candidates without an actual use case. Repetition is supporting evidence, not truth or authorization.

For an authorized saved proposal, use an agreed review folder outside `.agents/skills` and `.codex/skills`; otherwise keep it inline. Link to canonical evidence instead of copying raw transcripts. Promotion to active instructions requires human review of the exact scope and text. After approval, validate metadata, local links, retained safety boundaries and positive/negative behavior. Keep a pre-change snapshot and state a rollback path.
