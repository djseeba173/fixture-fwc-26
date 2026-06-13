import pytest
from rest_framework.test import APIClient

from apps.matches.constants import Phase
from apps.matches.models import Match
from apps.teams.models import Team
from apps.tournaments.models import Tournament


@pytest.mark.django_db
def test_match_result_endpoint_saves_result():
    tournament = Tournament.objects.create(name="World Cup 2026", year=2026, slug="world-cup-2026")
    home = Team.objects.create(name="Home")
    away = Team.objects.create(name="Away")
    match = Match.objects.create(tournament=tournament, match_number=1, phase=Phase.GROUP, home_team=home, away_team=away)

    response = APIClient().post(f"/api/matches/{match.pk}/result/", {"home_score": 2, "away_score": 1}, format="json")

    match.refresh_from_db()
    assert response.status_code == 200
    assert match.home_score == 2
    assert match.away_score == 1
    assert match.status == "finished"
