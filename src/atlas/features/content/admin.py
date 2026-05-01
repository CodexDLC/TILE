from typing import Any, ClassVar

from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline
from system.admin.translation import UnfoldTabbedTranslationAdmin, UnfoldTranslationTabularInline

from .models import (
    CardGridBlock,
    CardItem,
    CtaStripBlock,
    FactItem,
    FactsListBlock,
    GalleryBlock,
    GalleryImage,
    HeroBlock,
    Page,
    PageBlockSlot,
    PullQuoteBlock,
    RelatedPlacesBlock,
    RichTextBlock,
    TabItem,
    TabsBlock,
)


CONTENT_BLOCK_MODELS = (
    HeroBlock,
    RichTextBlock,
    PullQuoteBlock,
    FactsListBlock,
    GalleryBlock,
    CtaStripBlock,
    CardGridBlock,
    RelatedPlacesBlock,
    TabsBlock,
)

Page._meta.get_field("order").verbose_name = _("Порядок")
PageBlockSlot._meta.get_field("order").verbose_name = _("Порядок")


class HiddenFromAdminIndexMixin:
    """Keep technical models editable by direct link/inlines, but out of app indexes."""

    def get_model_perms(self, request: Any) -> dict[str, bool]:
        return {}


class PageBlockSlotInline(TabularInline):
    model = PageBlockSlot
    extra = 0
    fields = ("order", "content_type", "object_id", "display_variant")
    ordering = ("order",)

    def formfield_for_foreignkey(self, db_field: Any, request: Any, **kwargs: Any) -> Any:
        if db_field.name == "content_type":
            content_types = ContentType.objects.get_for_models(*CONTENT_BLOCK_MODELS).values()
            kwargs["queryset"] = ContentType.objects.filter(pk__in=[content_type.pk for content_type in content_types])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Page)
class PageAdmin(UnfoldTabbedTranslationAdmin):
    list_display = ("title", "page_type", "path", "is_published", "order", "published_at")
    list_editable = ("order",)
    list_filter = ("page_type", "is_published")
    search_fields = ("title", "path", "slug", "seo_title", "seo_description")
    prepopulated_fields: ClassVar[dict[str, tuple[str, ...]]] = {"slug": ("title",)}
    inlines = (PageBlockSlotInline,)
    fieldsets = (
        (None, {"fields": ("parent", "page_type", "title", "slug", "intro", "template_hint")}),
        (_("Публикация"), {"fields": ("is_published", "order", "published_at")}),
        (_("SEO"), {"fields": ("seo_title", "seo_description", "seo_image")}),
        (_("Системный роутинг"), {"fields": ("path",), "classes": ("collapse",)}),
    )
    readonly_fields = ("path",)


@admin.register(PageBlockSlot)
class PageBlockSlotAdmin(HiddenFromAdminIndexMixin, admin.ModelAdmin):
    list_display = ("page", "content_type", "object_id", "order", "display_variant")
    list_filter = ("content_type",)
    ordering = ("page", "order")


class FactItemInline(UnfoldTranslationTabularInline):
    model = FactItem
    extra = 0


class GalleryImageInline(UnfoldTranslationTabularInline):
    model = GalleryImage
    extra = 0


class CardItemInline(UnfoldTranslationTabularInline):
    model = CardItem
    extra = 0


class TabItemInline(UnfoldTranslationTabularInline):
    model = TabItem
    extra = 0


@admin.register(HeroBlock)
class HeroBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("title", "eyebrow", "alignment")
    search_fields = ("title", "subtitle")


@admin.register(RichTextBlock)
class RichTextBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    search_fields = ("heading", "body")


@admin.register(PullQuoteBlock)
class PullQuoteBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("quote", "attribution")


@admin.register(FactsListBlock)
class FactsListBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    inlines = (FactItemInline,)


@admin.register(GalleryBlock)
class GalleryBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    inlines = (GalleryImageInline,)


@admin.register(CtaStripBlock)
class CtaStripBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("title", "cta_label", "cta_url")


@admin.register(CardGridBlock)
class CardGridBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    inlines = (CardItemInline,)


@admin.register(RelatedPlacesBlock)
class RelatedPlacesBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    filter_horizontal = ("places",)


@admin.register(TabsBlock)
class TabsBlockAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("heading",)
    inlines = (TabItemInline,)


@admin.register(FactItem)
class FactItemAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("label", "value", "block", "order")


@admin.register(GalleryImage)
class GalleryImageAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("caption", "block", "order")


@admin.register(CardItem)
class CardItemAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("title", "block", "order")


@admin.register(TabItem)
class TabItemAdmin(HiddenFromAdminIndexMixin, UnfoldTabbedTranslationAdmin):
    list_display = ("label", "block", "order")
