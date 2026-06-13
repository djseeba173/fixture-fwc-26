from __future__ import annotations

from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandParser

from services.importers import import_worldcup_data


class Command(BaseCommand):
    help = "Import World Cup 2026 JSON files idempotently."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--data-dir", default=str(settings.BASE_DIR / "2026"))

    def handle(self, *args: object, **options: object) -> None:
        summary = import_worldcup_data(Path(str(options["data_dir"])))
        self.stdout.write(
            self.style.SUCCESS(
                "Imported World Cup data: "
                f"{summary.teams} teams, {summary.groups} groups, "
                f"{summary.stadiums} stadiums, {summary.matches} matches, "
                f"{summary.knockout_matches} knockout matches."
            )
        )
