from pathlib import Path

import pytest

from apps.brackets.models import KnockoutMatch
from apps.matches.models import Match, Stadium
from apps.teams.models import Team
from apps.tournaments.models import Group, Tournament
from services.importers import import_worldcup_data


@pytest.mark.django_db
def test_import_worldcup_data_is_idempotent(settings):
    summary = import_worldcup_data(Path(settings.BASE_DIR) / "2026")
    import_worldcup_data(Path(settings.BASE_DIR) / "2026")

    assert summary.matches == 104
    assert Tournament.objects.count() == 1
    assert Team.objects.count() == 48
    assert Group.objects.count() == 12
    assert Stadium.objects.count() == 16
    assert Match.objects.count() == 104
    assert KnockoutMatch.objects.count() == 32
    assert Match.objects.get(match_number=73).home_source == "2A"
    assert Match.objects.get(match_number=104).away_source == "W102"
