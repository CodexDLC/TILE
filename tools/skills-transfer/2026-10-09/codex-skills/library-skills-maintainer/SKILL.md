---
name: library-skills-maintainer
description: Create or maintain usage skills shipped with the canonical source of a reusable library. Use for authorized library skill work, not for editing installed copies in consumer projects.
---

# Library Skills Maintainer

Maintain a library usage skill as a versioned part of the library's own source and release. Apply this workflow only after establishing that the current workspace is the canonical source that publishes the library, and the requested skill is owned there. An editable install, a monorepo checkout, or a dependency source tree inside an application does not establish that authority. If ownership is unclear, inspect package metadata, release/build configuration, source history, and the user's stated scope before editing.

For an audit, report findings without changing files. For authorized creation or repair, inspect the current public API, supported installed version, package documentation, existing examples, and the skill's actual packaging path. Write instructions for supported consumer use: small executable examples, important constraints, integration seams, and where to find version-specific detail. Keep private customer facts and application policy out of the library skill. Put library-owned detail in focused references and link each from the entrypoint only where it is needed; do not require every reference to be loaded.

Before changing an existing skill, identify generated files, user edits, release ownership, and any maintained mirrors. Preserve user changes with a recoverable backup or a narrow diff when replacement could discard them. Remove a stale instruction only when the source or a reproducible check establishes that it is stale; label uncertain claims for review. Keep the skill aligned with the API that actually ships, rather than a planned API.

An installed library skill in a consumer project is managed content. Do not edit it locally, or alter its version/hash manifest to accept local changes. A canonical source skill edit and a consumer library upgrade are separate actions; refresh consumer content only through an authorized official update path. The application's own adapters, contracts, and business rules belong in project-owned skill references. See [references/ownership-and-delivery.md](references/ownership-and-delivery.md) for authoring structure, and when packaging, installation, or consumer verification is involved.

Validate the skill structure and relevant examples. When changing delivery, verify the built artifact and an isolated consumer install; exercise install/update/delete/status behavior only when that lifecycle is affected. Report the checks actually run and any remaining uncertainty. Do not publish a release, update dependencies, change an installer, or modify runtime, MCP, or configuration code unless those actions are separately in scope.
