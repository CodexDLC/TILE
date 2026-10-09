from urllib.parse import urlsplit
from xml.etree import ElementTree

from django.test import TestCase, override_settings
from django.urls import resolve


class SitemapTests(TestCase):
    @override_settings(CANONICAL_DOMAIN="https://atlas.example.com")
    def test_sitemap_contains_resolvable_absolute_urls(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        root = ElementTree.fromstring(response.content)  # noqa: S314
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = [node.text for node in root.findall("s:url/s:loc", ns)]
        self.assertIn("https://atlas.example.com/contacts/privacy/", urls)
        for url in urls:
            self.assertEqual(urlsplit(url).netloc, "atlas.example.com")
            resolve(urlsplit(url).path)
        for link in root.iter("{http://www.w3.org/1999/xhtml}link"):
            self.assertEqual(urlsplit(link.attrib["href"]).netloc, "atlas.example.com")
            resolve(urlsplit(link.attrib["href"]).path)

    @override_settings(CANONICAL_DOMAIN="", SITE_BASE_URL="http://localhost:8000/")
    def test_sitemap_uses_site_base_url_when_canonical_domain_is_empty(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://localhost:8000/contacts/privacy/")
        self.assertNotContains(response, "https:///")
