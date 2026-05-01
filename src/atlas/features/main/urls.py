from django.urls import path

from .views import ContactsView, HomeView

# Deprecated transitional routes. Public rendering is now owned by
# features.content and features.contacts; keep this only for legacy imports.
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]
