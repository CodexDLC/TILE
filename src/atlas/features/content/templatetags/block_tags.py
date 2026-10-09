from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from features.content.selectors.blocks import get_slot_block

register = template.Library()


@register.simple_tag(takes_context=True)
def render_block(context, slot) -> str:
    block = get_slot_block(slot)
    if block is None:
        return ""
    template_name = f"content/blocks/_{slot.block_type}.html"
    return mark_safe(  # noqa: S308
        render_to_string(
            template_name,
            {
                "block": block,
                "page": context.get("page"),
                "slot": slot,
                "request": context.get("request"),
            },
        )
    )


@register.simple_tag
def article_cover(page):
    from features.content.selectors.articles import article_parts

    cover = article_parts(page)["cover"]
    if cover:
        return cover.image.url
    place = getattr(page, "place", None)
    return place.hero_image.url if place and place.hero_image else ""
