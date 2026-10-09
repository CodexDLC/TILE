# ADR format and evidence

Follow the repository's format first. Otherwise use:

```markdown
# ADR-NNNN: Decision title

Date: actual decision date, or explicitly unknown
Status: proposed | accepted | deprecated | superseded by ADR-NNNN
Deciders: confirmed participants, or omit if unknown

## Context
Problem, constraints and evidence that make the decision necessary.

## Decision
Chosen direction, scope and supported contract. Mark an unapproved choice as proposed.

## Alternatives
Real alternatives considered, their relevant tradeoffs and why they were not selected.

## Consequences
Benefits, costs, limitations, risks and any explicit revisit condition.

## Evidence
Relevant files, tests, issues or primary documentation, with observation dates when freshness matters.
```

Keep the record proportional to the decision; omit empty optional sections. If no alternatives were discussed, state that rather than inventing a comparison. An ADR index needs only number, title and status/link. Resolve contradictions against current implementation and later decisions; report unresolved differences. Never treat an accepted ADR as permission to deploy, migrate data or contact others.
