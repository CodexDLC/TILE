from django import template
from django.utils.safestring import mark_safe
from markdown_it import MarkdownIt

register = template.Library()
_markdown = MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": True})


@register.filter
def markdown(value: str) -> str:
    return mark_safe(_markdown.render(value or ""))  # noqa: S308
