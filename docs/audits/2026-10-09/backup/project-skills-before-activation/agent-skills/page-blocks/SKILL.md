---
name: atlas-page-blocks
description: Load this skill when adding or changing Atlas Page + typed block content-platform models, selectors, services, admin, fixtures, or templates.
---

Atlas uses Variant C content composition:

- `Page` owns hierarchy, slug/path routing, page type, SEO, locale-aware text,
  and publication state.
- `PageBlockSlot` links a page to one concrete typed block through
  `content_type`, `object_id`, and `GenericForeignKey`.
- Slot order controls body rendering. Blocks are rendered by a dispatcher that
  receives the slot and passes a single `block` context variable to each partial.
- Concrete block models stay typed and admin-editable. Do not collapse block
  fields into one JSON blob unless a future migration explicitly chooses that.
- Reads go through `features.content.selectors`.
- Writes and ordering mutations go through `features.content.services`.
