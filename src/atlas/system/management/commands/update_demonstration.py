from django.conf import settings
from django.core.management.base import BaseCommand

from system.services.demonstration import load_demonstration_content, reset_demonstration_content


class Command(BaseCommand):
    help = "Load Atlas demonstration content from system/fixtures/demonstration."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Accepted for update_all_content compatibility.")
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing Atlas content-platform pages and places before loading starter content.",
        )

    def handle(self, *args, **options):
        fixture_dir = settings.BASE_DIR / "system" / "fixtures" / "demonstration"
        if options["reset"]:
            reset_demonstration_content()
            self.stdout.write(self.style.WARNING("Reset existing Atlas content-platform pages and places."))
        summary = load_demonstration_content(fixture_dir)
        self.stdout.write(
            self.style.SUCCESS(
                "Loaded Atlas demonstration content: "
                f"{summary['countries']} countries, "
                f"{summary['regions']} regions, "
                f"{summary['cities']} cities, "
                f"{summary['places']} places, "
                f"{summary['pages']} pages."
            )
        )
