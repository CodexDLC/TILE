from features.content.models import PageBlockSlot


def get_slot_block(slot: PageBlockSlot) -> object | None:
    return getattr(slot, "resolved_block", None) or slot.content_object
