from modeltranslation.admin import TabbedTranslationAdmin, TranslationTabularInline
from unfold.admin import ModelAdmin, TabularInline


class UnfoldTabbedTranslationAdmin(TabbedTranslationAdmin, ModelAdmin):
    """Tabbed modeltranslation admin rendered with Unfold form styling."""


class UnfoldTranslationTabularInline(TranslationTabularInline, TabularInline):
    """Translation-aware tabular inline rendered with Unfold form styling."""

