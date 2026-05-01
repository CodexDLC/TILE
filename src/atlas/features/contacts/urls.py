from django.urls import path

from .views import ContactView, ImpressumView, PrivacyView

urlpatterns = [
    path("", ContactView.as_view(), name="contacts"),
    path("impressum/", ImpressumView.as_view(), name="impressum"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]
