from urllib.parse import urlsplit

from codex_django.core.sitemaps import BaseSitemap
from django.conf import settings

# Import other specific sitemaps from features here as needed
# from features.main.sitemaps import CategorySitemap


class StaticSitemap(BaseSitemap):
    """
    Sitemap for static pages that don't depend on models.
    """

    priority = 0.5
    changefreq = "monthly"

    def get_domain(self, site=None) -> str:
        domain = settings.CANONICAL_DOMAIN or settings.SITE_BASE_URL
        return urlsplit(domain if "://" in domain else f"//{domain}").netloc

    def items(self):
        # Configuration for static pages is usually in core/settings/modules/sitemap.py
        # but you can also provide a hardcoded list here.
        return getattr(settings, "SITEMAP_STATIC_PAGES", ["home"])


# Example of how to structure the sitemaps dict for URLs
# You can add feature sitemaps here as well.
class ContentSitemap(StaticSitemap):
    """Only published pages and actual title translations enter the content sitemap."""

    def items(self):
        from features.content.models import Page

        return Page.objects.filter(is_published=True).exclude(page_type="home").order_by("pk")

    def location(self, item):
        return item.absolute_path

    def lastmod(self, item):
        return item.updated_at

    def get_languages_for_item(self, item):
        return [code for code in self.languages if getattr(item, f"title_{code}", "")]

    def build_alternates(self, item, domain=None):
        from django.utils.translation import override

        page = item[0] if isinstance(item, (list, tuple)) else item
        alternates = []
        for code in self.get_languages_for_item(page):
            with override(code):
                alternates.append(
                    {"lang_code": code, "location": f"https://{domain or self.get_domain()}{page.absolute_path}"}
                )
        return alternates


sitemaps = {
    "static": StaticSitemap,
    "content": ContentSitemap,
    # "categories": CategorySitemap,
}
