# ruff: noqa: RUF001, S106
from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.translation import override
from features.content.models import Page
from PIL import Image


class ArticleWorkflowTests(TestCase):
    def setUp(self):
        self.media = TemporaryDirectory()
        self.addCleanup(self.media.cleanup)
        self.settings_override = override_settings(MEDIA_ROOT=self.media.name)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.author = get_user_model().objects.create_superuser(
            username="author", email="author@example.test", password="test-password"
        )
        self.client.force_login(self.author)
        self.city = Page.objects.create(title="City", page_type="city", slug="city", is_published=True)

    def photo(self):
        buffer = BytesIO()
        Image.new("RGB", (20, 20), "green").save(buffer, format="PNG")
        return SimpleUploadedFile("cover.png", buffer.getvalue(), content_type="image/png")

    def payload(self, **changes):
        data = {
            "language": "ru",
            "title": "История собора",
            "intro": "Короткое знакомство",
            "body": "Основная история **собора**",
            "city": str(self.city.pk),
            "action": "save",
            "caption": "Вид собора",
            "alt_text": "Собор с площади",
        }
        data.update(changes)
        return data

    def test_manual_draft_preview_publish_edit_and_unpublish(self):
        response = self.client.post(reverse("cabinet:article_create"), self.payload(image=self.photo()))
        self.assertEqual(response.status_code, 302)
        page = Page.objects.get(page_type="story")
        self.assertFalse(page.is_published)
        self.assertEqual(self.client.get(page.absolute_path).status_code, 404)
        preview = reverse("cabinet:article_preview", args=[page.pk])
        response = self.client.get(preview, {"language": "ru"})
        self.assertContains(response, "Основная история")
        self.assertContains(response, "cover")
        self.assertIn("no-store", response.headers["Cache-Control"])
        self.assertIn("noindex", response.headers["X-Robots-Tag"])
        self.client.logout()
        self.assertEqual(self.client.get(preview).status_code, 302)
        self.client.force_login(self.author)
        edit = reverse("cabinet:article_edit", args=[page.pk])
        response = self.client.post(edit, self.payload(action="publish"))
        self.assertEqual(response.status_code, 302)
        page.refresh_from_db()
        self.assertTrue(page.is_published)
        old_path = page.path
        with override("ru"):
            response = self.client.get(page.absolute_path)
        self.assertContains(response, "Основная история")
        self.assertContains(response, "<strong>собора</strong>", html=True)
        response = self.client.post(edit, self.payload(title="Новое название", action="save"))
        self.assertEqual(response.status_code, 302)
        page.refresh_from_db()
        self.assertEqual(page.path, old_path)
        self.assertTrue(page.is_published)
        self.client.post(edit, {"action": "unpublish"})
        page.refresh_from_db()
        self.assertFalse(page.is_published)
        self.assertEqual(self.client.get(page.absolute_path).status_code, 404)

    def test_ordinary_user_cannot_edit_or_preview(self):
        user = get_user_model().objects.create_user(
            username="reader", email="reader@example.test", password="test-password"
        )
        self.client.force_login(user)
        page = Page.objects.create(title="Private", slug="private", page_type="story")
        for name, args in [
            ("article_list", []),
            ("article_create", []),
            ("article_edit", [page.pk]),
            ("article_preview", [page.pk]),
        ]:
            self.assertEqual(self.client.get(reverse("cabinet:" + name, args=args)).status_code, 403)

    def test_publish_requires_body_and_photo_but_draft_does_not(self):
        response = self.client.post(reverse("cabinet:article_create"), self.payload(body="", action="publish"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Page.objects.filter(page_type="story").exists())
        response = self.client.post(reverse("cabinet:article_create"), self.payload(body=""))
        self.assertEqual(response.status_code, 302)

    def test_search_and_city_show_published_stories_only(self):
        public = Page.objects.create(
            title="Visible cathedral", page_type="story", parent=self.city, slug="visible", is_published=True
        )
        Page.objects.create(title="Secret cathedral", page_type="story", parent=self.city, slug="secret")
        self.client.logout()
        response = self.client.get(reverse("places-search"), {"q": "cathedral"})
        self.assertContains(response, public.title)
        self.assertNotContains(response, "Secret cathedral")
        response = self.client.get(self.city.absolute_path)
        self.assertContains(response, public.title)
        self.assertNotContains(response, "Secret cathedral")

    def test_language_urls_keep_the_language(self):
        page = Page.objects.create(title="Story", slug="story", page_type="story", is_published=True)
        with override("de"):
            self.assertEqual(page.absolute_path, "/de/story/")

    def test_editor_opens_existing_language_and_preserves_other_translation(self):
        from features.content.models import PageBlockSlot, RichTextBlock

        page = Page.objects.create(title_en="Existing story", page_type="story", slug="existing")
        body = RichTextBlock.objects.create(body_en="English story")
        PageBlockSlot.objects.create(page=page, content_object=body)
        url = reverse("cabinet:article_edit", args=[page.pk])
        response = self.client.get(url)
        self.assertContains(response, "English story")
        response = self.client.post(url, self.payload(language="ru", city=""))
        self.assertEqual(response.status_code, 302)
        body.refresh_from_db()
        self.assertEqual(body.body_en, "English story")
        self.assertEqual(body.body_ru, "Основная история **собора**")

    def test_shared_text_is_not_changed_on_another_article(self):
        from features.content.models import PageBlockSlot, RichTextBlock

        a = Page.objects.create(title_ru="Первая", page_type="story", slug="first")
        b = Page.objects.create(title_ru="Вторая", page_type="story", slug="second")
        body = RichTextBlock.objects.create(body_ru="Общий исходный текст")
        PageBlockSlot.objects.create(page=a, content_object=body)
        PageBlockSlot.objects.create(page=b, content_object=body)
        self.client.post(reverse("cabinet:article_edit", args=[a.pk]), self.payload(city=""))
        body.refresh_from_db()
        self.assertEqual(body.body_ru, "Общий исходный текст")

    def test_staff_with_editor_permissions_can_use_workflow(self):
        from django.contrib.auth.models import Permission

        author = get_user_model().objects.create_user(username="editor", is_staff=True)
        author.user_permissions.set(
            Permission.objects.filter(
                content_type__app_label="content", codename__in=["view_page", "add_page", "change_page"]
            )
        )
        self.client.force_login(author)
        response = self.client.get(reverse("cabinet:article_list"))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse("cabinet:article_create"), self.payload())
        self.assertEqual(response.status_code, 302)

    def test_invalid_image_and_script_text(self):
        fake = SimpleUploadedFile("photo.png", b"not an image", content_type="image/png")
        response = self.client.post(reverse("cabinet:article_create"), self.payload(image=fake))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Page.objects.filter(page_type="story").exists())
        self.client.post(
            reverse("cabinet:article_create"),
            self.payload(body='<script>alert("x")</script>', image=self.photo(), action="publish"),
        )
        page = Page.objects.get(page_type="story")
        response = self.client.get(page.absolute_path)
        self.assertNotContains(response, '<script>alert("x")</script>')

    def test_sitemap_includes_published_article_not_draft(self):
        Page.objects.create(title_ru="Статья", page_type="story", slug="public-story", is_published=True)
        Page.objects.create(title_ru="Черновик", page_type="story", slug="private-story")
        response = self.client.get("/sitemap.xml")
        self.assertContains(response, "/ru/public-story/")
        self.assertNotContains(response, "/private-story/")

    def test_upload_gallery_without_replacing_cover(self):
        self.client.post(reverse("cabinet:article_create"), self.payload(image=self.photo()))
        page = Page.objects.get(page_type="story")
        from features.content.selectors.articles import article_parts

        cover = article_parts(page)["cover"]
        response = self.client.post(
            reverse("cabinet:article_edit", args=[page.pk]),
            self.payload(additional_images=[self.photo(), self.photo()]),
        )
        self.assertEqual(response.status_code, 302)
        parts = article_parts(page)
        self.assertEqual(parts["cover"].pk, cover.pk)
        self.assertEqual(parts["gallery"].images.count(), 3)

    def test_shared_gallery_is_not_edited_on_another_article(self):
        from features.content.models import GalleryBlock, GalleryImage, PageBlockSlot

        a = Page.objects.create(title_ru="Первая", page_type="story", slug="a")
        b = Page.objects.create(title_ru="Вторая", page_type="story", slug="b")
        gallery = GalleryBlock.objects.create()
        cover = GalleryImage.objects.create(block=gallery, image=self.photo(), caption_ru="Исходная подпись")
        PageBlockSlot.objects.create(page=a, content_object=gallery)
        PageBlockSlot.objects.create(page=b, content_object=gallery)
        self.client.post(reverse("cabinet:article_edit", args=[a.pk]), self.payload(city="", caption="Новая подпись"))
        cover.refresh_from_db()
        self.assertEqual(cover.caption_ru, "Исходная подпись")
