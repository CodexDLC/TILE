from __future__ import annotations

import re
from typing import Any

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from system.models.mixins import OrderableMixin, TimestampMixin


class PageBlockSlot(TimestampMixin, OrderableMixin):
    page: Any = models.ForeignKey(
        "content.Page", on_delete=models.CASCADE, related_name="block_slots", verbose_name=_("Страница")
    )
    content_type: Any = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_("Тип блока"))
    object_id: Any = models.PositiveIntegerField(_("ID блока"))
    content_object = GenericForeignKey("content_type", "object_id")
    display_variant: Any = models.CharField(_("Вариант отображения"), max_length=64, blank=True)

    class Meta(OrderableMixin.Meta):
        verbose_name = _("Слот блока страницы")
        verbose_name_plural = _("Слоты блоков страницы")
        indexes = (
            models.Index(fields=["page", "order"]),
            models.Index(fields=["content_type", "object_id"]),
        )

    def __str__(self) -> str:
        return f"{self.page} #{self.order}"

    @property
    def block(self) -> Any:
        return self.content_object

    @property
    def block_type(self) -> str:
        model_class = self.content_type.model_class() if getattr(self, "content_type_id", None) else None
        model_name = model_class.__name__ if model_class else ""
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", model_name).lower()
        return name.removesuffix("_block")
