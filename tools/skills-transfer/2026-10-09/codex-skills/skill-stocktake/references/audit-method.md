# Focused skill audit

For each selected skill check:

| Dimension | Evidence to inspect |
|---|---|
| Trigger | Does the description identify a real task and avoid attracting unrelated work? |
| Scope | Does the skill preserve intent, authorization and project ownership? |
| Unique value | Which concrete decisions does it improve beyond native tools and other skills? |
| Progressive disclosure | Are critical constraints in the main file and conditional detail routed explicitly? |
| Currency | Are paths, tools and API assumptions valid? Verify unstable technical claims with primary sources when needed. |
| Consistency | Does another skill contradict it or duplicate the same rule? Which source should own that rule? |
| Usage | Is there actual observed invocation evidence? A catalog entry, timestamp or mention is not execution. |
| Maintenance | Do references resolve, scripts have validation and mirrors have a clear source? |

Verdicts:
- **Keep:** unique and current; state the useful responsibility.
- **Improve:** name the defective section and a concrete correction.
- **Merge into X:** name the canonical destination and what must move; inspect callers before removal.
- **Retire:** name the defect and the replacement, including any capability lost.

Report `skill | verdict | evidence | proposed change | validation/rollback`. Keep the report concise and make uncertainty explicit. For a quick audit, compare content hashes where a trustworthy previous inventory exists; modification time alone does not establish a content change.

Do not impose a line-count quota. Shorten by removing repetition or moving genuinely conditional detail, not by hiding unconditional constraints in references. Preserve explicit user policy even when it is expensive; propose policy changes separately.
