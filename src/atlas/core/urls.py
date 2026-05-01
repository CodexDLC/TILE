from typing import Any

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from core.sitemaps import sitemaps

# Error Handlers
handler404 = "system.views.errors.handler404"
handler500 = "system.views.errors.handler500"
handler403 = "system.views.errors.handler403"
handler400 = "system.views.errors.handler400"

# Non-prefixed patterns (API, technical files)
urlpatterns: list[Any] = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path("llms_de.txt", TemplateView.as_view(template_name="llms_de.txt", content_type="text/plain")),
    path("llms_en.txt", TemplateView.as_view(template_name="llms_en.txt", content_type="text/plain")),
]
urlpatterns += [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("cabinet/", include("cabinet.urls")),
    path("system/", include("system.urls")),
    path("showcase/", include("codex_django.showcase.urls")),
    path("messaging/", include("features.messaging.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path("contacts/", include("features.contacts.urls")),
    path("places/", include("features.places.urls")),
    path("", include("features.content.urls")),
    prefix_default_language=False,
)
