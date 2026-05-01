from django.views.generic import TemplateView


class ImpressumView(TemplateView):
    template_name = "contacts/impressum.html"


class PrivacyView(TemplateView):
    template_name = "contacts/privacy.html"
