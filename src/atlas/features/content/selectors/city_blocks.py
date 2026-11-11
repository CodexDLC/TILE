from features.content.models import FactsListBlock, PageBlockSlot, RichTextBlock
from features.places.models import City


def get_city_extra_slots(slots: list[PageBlockSlot], city: City | None) -> list[PageBlockSlot]:
    return [
        slot
        for slot in slots
        if slot.block_type != "hero"
        and slot.resolved_block is not None
        and not (city is not None and _is_starter_block(slot.resolved_block, city))
    ]


def _is_starter_block(block: object, city: City) -> bool:
    """Recognize unchanged city placeholders written by the former demo generator."""
    if isinstance(block, RichTextBlock):
        return (
            block.heading_en == f"{city.name_en}, a first city chapter."
            and block.body_en == city.intro_en
            and not any((block.heading_de, block.body_de, block.heading_ru, block.body_ru))
        )
    if not isinstance(block, FactsListBlock) or block.heading_en != "City anchors":
        return False
    if block.intro_en != "A minimal starter layer before the city receives a fuller editorial treatment." or any(
        (block.heading_de, block.intro_de, block.heading_ru, block.intro_ru)
    ):
        return False

    items = list(block.items.all())
    if any(
        item.label_de or item.value_de or item.note_de or item.label_ru or item.value_ru or item.note_ru
        for item in items
    ):
        return False
    return [(item.label_en, item.value_en, item.note_en or "") for item in items] == [
        ("Country", city.region.country.name_en, ""),
        ("Region", city.region.name_en, ""),
        ("Editorial status", "Starter city page", "Places can be expanded from here."),
    ]
