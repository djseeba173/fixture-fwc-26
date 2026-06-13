import pytest

from apps.matches.constants import MatchStatus, Phase
from apps.matches.models import Match
from apps.teams.models import Team
from apps.tournaments.models import Group, GroupMembership, Tournament
from services.standings import recalculate_group_standings


@pytest.fixture
def group():
    tournament = Tournament.objects.create(name="World Cup 2026", year=2026, slug="world-cup-2026")
    group = Group.objects.create(tournament=tournament, name="Group A")
    teams = [Team.objects.create(name=name) for name in ["Alpha", "Beta", "Gamma"]]
    for team in teams:
        GroupMembership.objects.create(group=group, team=team)
    return group, teams, tournament


@pytest.mark.django_db
def test_recalculate_group_standings_orders_by_points_gd_and_goals_for(group):
    group, teams, tournament = group
    Match.objects.create(tournament=tournament, match_number=1, phase=Phase.GROUP, group=group, home_team=teams[0], away_team=teams[1], home_score=2, away_score=0, status=MatchStatus.FINISHED)
    Match.objects.create(tournament=tournament, match_number=2, phase=Phase.GROUP, group=group, home_team=teams[2], away_team=teams[0], home_score=1, away_score=1, status=MatchStatus.FINISHED)
    Match.objects.create(tournament=tournament, match_number=3, phase=Phase.GROUP, group=group, home_team=teams[1], away_team=teams[2], home_score=0, away_score=3, status=MatchStatus.FINISHED)

    standings = recalculate_group_standings(group)

    assert [row.team.name for row in standings] == ["Gamma", "Alpha", "Beta"]
    assert standings[0].points == 4
    assert standings[0].goal_difference == 3
    assert standings[1].points == 4
    assert standings[1].goal_difference == 2
