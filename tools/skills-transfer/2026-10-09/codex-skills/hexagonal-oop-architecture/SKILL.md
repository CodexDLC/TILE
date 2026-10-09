---
name: hexagonal-oop-architecture
description: Keep domain logic, orchestration, ports, and adapters separate in non-trivial code; use for generators, pipelines, handlers, architecture work, and god-object refactors.
---

# Hexagonal OOP Architecture

Use distributed OOP for non-trivial code: small cohesive classes/modules with explicit responsibilities. Keep domain models, rules and algorithms independent of UI, server, renderer, storage and third-party adapters. Application use cases coordinate domain operations; ports define required external capabilities; adapters implement them. A pipeline orchestrates ordered stages and passes context, but does not implement stage algorithms inline.

Do not grow a god object: when a class or module takes on unrelated responsibilities, split them across clear owners. UI/server code may parse controls, call use cases, and render results; domain semantics belong in the domain/application layers. Before editing, identify the new responsibility, its owner, the affected boundary, and how to test it. If ownership is unclear, state intended boundaries first.

For multi-stage generators, Studio/UI separation, and concrete class layouts, read [references/boundaries.md](references/boundaries.md).
