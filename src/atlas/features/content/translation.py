from modeltranslation.translator import TranslationOptions, register

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
    PullQuoteBlock,
    RelatedPlacesBlock,
    RichTextBlock,
    TabItem,
    TabsBlock,
)


@register(Page)
class PageTranslationOptions(TranslationOptions):
    fields = ("title", "intro", "seo_title", "seo_description")


@register(HeroBlock)
class HeroBlockTranslationOptions(TranslationOptions):
    fields = ("eyebrow", "title", "subtitle", "cta_label", "secondary_cta_label")


@register(RichTextBlock)
class RichTextBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "body")


@register(PullQuoteBlock)
class PullQuoteBlockTranslationOptions(TranslationOptions):
    fields = ("quote", "attribution")


@register(FactsListBlock)
class FactsListBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "intro")


@register(FactItem)
class FactItemTranslationOptions(TranslationOptions):
    fields = ("label", "value", "note")


@register(GalleryBlock)
class GalleryBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "intro")


@register(GalleryImage)
class GalleryImageTranslationOptions(TranslationOptions):
    fields = ("caption", "alt_text")


@register(CtaStripBlock)
class CtaStripBlockTranslationOptions(TranslationOptions):
    fields = ("eyebrow", "title", "text", "cta_label")


@register(CardGridBlock)
class CardGridBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "intro")


@register(CardItem)
class CardItemTranslationOptions(TranslationOptions):
    fields = ("eyebrow", "title", "text")


@register(RelatedPlacesBlock)
class RelatedPlacesBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "intro")


@register(TabsBlock)
class TabsBlockTranslationOptions(TranslationOptions):
    fields = ("heading", "intro")


@register(TabItem)
class TabItemTranslationOptions(TranslationOptions):
    fields = ("label", "heading", "body")
