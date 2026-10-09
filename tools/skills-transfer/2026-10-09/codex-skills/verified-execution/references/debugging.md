# Debugging

1. Capture the exact failure and reproduction conditions; distinguish observed facts from hypotheses.
2. Search the failing symbol, command, configuration or test. Read its definition and trace the actual runtime path and callers.
3. Form a specific hypothesis and choose the smallest check that can confirm or reject it. If reproduction is unavailable, state the uncertainty rather than claiming a cause.
4. Fix the confirmed cause within authorized scope. Do not stack speculative fixes; revise the plan if the impact grows.
5. Run the reproducer or regression test, then relevant surrounding checks. Record what passed and what remains unverified.

If a required definition or environment is missing, identify it precisely and ask for the information needed to proceed. Do not invent a replacement or assume an incompletely copied project is the current source of truth.
