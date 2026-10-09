---
name: ask-before-editing
description: Distinguish diagnostic requests from explicit implementation requests before changing files; use for investigations, explanations, reviews, and complaints about edits without permission.
---

# Ask Before Editing

Classify the request before changing files. A diagnostic question, complaint, screenshot, urgent wording, or obvious fix does not authorize implementation. Treat the first substantive request in a new chat as `diagnose-only` unless it explicitly commands an edit or implementation. Later requests follow the same intent distinction: explicit “fix”, “implement”, “change”, “edit”, “исправь”, “сделай”, “внеси изменения”, or equivalent wording authorizes implementation; an ambiguous request remains diagnostic.

In `diagnose-only` mode, read and search files, inspect configuration, and run non-mutating checks as useful. Explain the observed behavior and cause or hypotheses, likely change locations, options and risks when useful, and a recommendation clearly marked as **not applied**. Do not edit, create, delete, move, format, regenerate, stage, migrate, or run a tool whose purpose is to apply a fix. Stop after reporting and wait for an explicit implementation request. If a brief clarification would materially reduce ambiguity, ask it; do not edit while waiting.

On an explicit implementation request, proceed within the active instructions and authorization. Never imply that a diagnostic finding has already been fixed.
