from django.core.management.base import BaseCommand
from django.db import transaction

from features.content.models import CtaStripBlock, HeroBlock, Page, RichTextBlock
from features.content.services.pages import attach_block, publish_page


class Command(BaseCommand):
    help = "Load baseline Atlas content fixtures."

    @transaction.atomic
    def handle(self, *args, **options):
        page, _created = Page.objects.update_or_create(
            page_type=Page.PageType.HOME,
            path="",
            defaults={
                "title": "Atlas",
                "intro": "Editorial travel notes, structured by country, region, city, and place.",
                "slug": "",
                "is_published": True,
            },
        )
        publish_page(page)

        if page.block_slots.exists():
            self.stdout.write(self.style.SUCCESS("Homepage already has content blocks."))
            return

        hero = HeroBlock.objects.create(
            eyebrow="Editorial travel guide",
            title="Atlas",
            subtitle="A warm, structured guide to places worth slowing down for.",
            cta_label="Start exploring",
            cta_url="/",
        )
        rich_text = RichTextBlock.objects.create(
            heading="Travel, with a little more context",
            body=(
                "Atlas combines practical destination structure with short editorial notes. "
                "Countries, regions, cities, and places share one flexible page model."
            ),
        )
        cta = CtaStripBlock.objects.create(
            eyebrow="Planning layer",
            title="The guide foundation is live",
            text="Content editors can now assemble pages from typed reusable sections.",
            cta_label="Contact Atlas",
            cta_url="/contacts/",
        )

        attach_block(page, hero, order=0)
        attach_block(page, rich_text, order=1)
        attach_block(page, cta, order=2)
        self.stdout.write(self.style.SUCCESS("Loaded homepage content fixture."))
