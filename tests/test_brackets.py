import pytest

from apps.brackets.models import KnockoutMatch
from apps.matches.constants import MatchStatus, Phase
from apps.matches.models import Match
from apps.teams.models import Team
from apps.tournaments.models import Tournament


@pytest.mark.django_db
def test_finished_knockout_advances_winner_to_next_slot():
    tournament = Tournament.objects.create(name="World Cup 2026", year=2026, slug="world-cup-2026")
    home = Team.objects.create(name="Home")
    away = Team.objects.create(name="Away")
    semi = Match.objects.create(tournament=tournament, match_number=101, phase=Phase.SEMI_FINAL, home_team=home, away_team=away, home_source="W97", away_source="W98")
    final = Match.objects.create(tournament=tournament, match_number=104, phase=Phase.FINAL, home_source="W101", away_source="W102")
    semi_ko = KnockoutMatch.objects.create(match=semi, match_number=101, phase=semi.phase, home_source=semi.home_source, away_source=semi.away_source)
    KnockoutMatch.objects.create(match=final, match_number=104, phase=final.phase, home_source=final.home_source, away_source=final.away_source)
    semi_ko.next_match = final.knockout
    semi_ko.next_slot = "home"
    semi_ko.save()

    semi.home_score = 3
    semi.away_score = 1
    semi.status = MatchStatus.FINISHED
    semi.save()

    final.refresh_from_db()
    assert final.home_team == home
