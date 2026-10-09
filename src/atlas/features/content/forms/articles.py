from django import forms
from django.utils.translation import gettext_lazy as _

from features.content.models import Page
from features.content.selectors.articles import article_parts, editor_initial

LANGUAGES = (("ru", "Русский"), ("de", "Deutsch"), ("en", "English"))


class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


def validate_photo(image):
    if image.size > 10 * 1024 * 1024:
        raise forms.ValidationError(_("Choose an image smaller than 10 MB."))
    if image.image.format not in {"JPEG", "PNG", "WEBP"}:
        raise forms.ValidationError(_("JPEG, PNG, and WebP are supported."))
    return image


class MultipleImageField(forms.ImageField):
    widget = MultipleImageInput

    def clean(self, data, initial=None):
        if not data:
            return []
        images = data if isinstance(data, (list, tuple)) else [data]
        if len(images) > 10:
            raise forms.ValidationError(_("You can add up to 10 photographs at once."))
        return [validate_photo(super(MultipleImageField, self).clean(image, initial)) for image in images]


class ArticleForm(forms.Form):
    language = forms.ChoiceField(label=_("Article language"), choices=LANGUAGES, widget=forms.HiddenInput)
    title = forms.CharField(label=_("Article title"), max_length=255)
    city = forms.ModelChoiceField(
        label=_("City"), queryset=Page.objects.none(), required=False, empty_label=_("No city assigned")
    )
    intro = forms.CharField(label=_("Short introduction"), required=False, widget=forms.Textarea(attrs={"rows": 3}))
    body = forms.CharField(
        label=_("Article text"),
        required=False,
        widget=forms.Textarea(attrs={"rows": 18}),
        help_text=_("Write in paragraphs. Markdown is supported: ## headings, **emphasis**, and lists."),
    )
    image = forms.ImageField(
        label=_("Photograph"),
        required=False,
        help_text=_("JPEG, PNG, or WebP, up to 10 MB. A new file replaces the cover; other photos are kept."),
    )
    additional_images = MultipleImageField(
        label=_("Additional photographs"),
        required=False,
        help_text=_("You can select several files. They appear after the article text."),
    )
    caption = forms.CharField(label=_("Photograph caption"), required=False, max_length=255)
    alt_text = forms.CharField(
        label=_("Photograph description for screen-reader users"), required=False, max_length=255
    )
    seo_title = forms.CharField(label=_("Search-engine title"), required=False, max_length=255)
    seo_description = forms.CharField(
        label=_("Search-engine description"), required=False, widget=forms.Textarea(attrs={"rows": 3})
    )

    def __init__(self, *args, page=None, language="ru", **kwargs):
        self.page = page
        kwargs.setdefault("initial", editor_initial(page, language))
        super().__init__(*args, **kwargs)
        self.fields["city"].queryset = Page.objects.filter(page_type="city", is_published=True).order_by("title")
        if page is not None:
            # Keep published addresses and existing geographic relationships stable.
            self.fields["city"].disabled = True
            if page.parent_id:
                self.fields["city"].queryset = Page.objects.filter(page_type="city")
            self.fields["city"].help_text = _("The city is fixed after creation to keep the article address stable.")
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["image"].widget.attrs["accept"] = "image/jpeg,image/png,image/webp"

    def clean_image(self):
        image = self.cleaned_data.get("image")
        return validate_photo(image) if image else image

    def clean(self):
        data = super().clean()
        action = self.data.get("action", "save")
        if action not in {"save", "publish", "preview"}:
            raise forms.ValidationError(_("Unknown action."))
        if action == "publish" or (self.page and self.page.is_published):
            if not (data.get("body") or "").strip():
                self.add_error("body", _("Add article text before publishing."))
            parts = article_parts(self.page)
            place = getattr(self.page, "place", None) if self.page else None
            if not (data.get("image") or parts["cover"] or (place and place.hero_image)):
                self.add_error("image", _("Add a photograph before publishing."))
        return data


