from __future__ import annotations

from apps.matches.constants import MatchStatus, Phase
from apps.matches.models import Match
from apps.standings.models import Standing
from apps.tournaments.models import Group, Tournament


def recalculate_group_standings(group: Group) -> list[Standing]:
    """Rebuild standings for a group using points, GD and goals for."""
    rows: dict[int, dict[str, int]] = {}
    for team in group.teams.all():
        rows[team.id] = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0,
        }

    matches = Match.objects.filter(group=group, status=MatchStatus.FINISHED).select_related("home_team", "away_team")
    for match in matches:
        if match.home_team_id is None or match.away_team_id is None:
            continue
        if match.home_score is None or match.away_score is None:
            continue
        home = rows[match.home_team_id]
        away = rows[match.away_team_id]
        home["played"] += 1
        away["played"] += 1
        home["goals_for"] += match.home_score
        home["goals_against"] += match.away_score
        away["goals_for"] += match.away_score
        away["goals_against"] += match.home_score
        if match.home_score > match.away_score:
            home["wins"] += 1
            home["points"] += 3
            away["losses"] += 1
        elif match.home_score < match.away_score:
            away["wins"] += 1
            away["points"] += 3
            home["losses"] += 1
        else:
            home["draws"] += 1
            away["draws"] += 1
            home["points"] += 1
            away["points"] += 1

    for values in rows.values():
        values["goal_difference"] = values["goals_for"] - values["goals_against"]

    created: list[Standing] = []
    for team_id, values in rows.items():
        standing, _ = Standing.objects.update_or_create(group=group, team_id=team_id, defaults=values)
        created.append(standing)

    ordered = list(
        Standing.objects.filter(group=group)
        .select_related("team")
        .order_by("-points", "-goal_difference", "-goals_for", "team__name")
    )
    for rank, standing in enumerate(ordered, start=1):
        if standing.rank != rank:
            standing.rank = rank
            standing.save(update_fields=["rank"])
    return ordered


def update_group_qualifications(tournament: Tournament) -> None:
    """Fill Round of 32 slots from current group standings."""
    from apps.matches.models import Match

    standings = _standings_by_group(tournament)
    third_place = _third_place_teams(standings)
    matches = Match.objects.filter(tournament=tournament, phase=Phase.ROUND_OF_32).select_related("home_team", "away_team")
    for match in matches:
        home_team = _resolve_group_source(match.home_source, standings, third_place)
        away_team = _resolve_group_source(match.away_source, standings, third_place)
        changed_fields: list[str] = []
        if home_team and match.home_team_id != home_team.id:
            match.home_team = home_team
            changed_fields.append("home_team")
        if away_team and match.away_team_id != away_team.id:
            match.away_team = away_team
            changed_fields.append("away_team")
        if changed_fields:
            match.save(update_fields=changed_fields)
            if hasattr(match, "knockout"):
                match.knockout.home_team = match.home_team
                match.knockout.away_team = match.away_team
                match.knockout.save(update_fields=["home_team", "away_team"])


def _standings_by_group(tournament: Tournament) -> dict[str, list[Standing]]:
    groups = tournament.groups.prefetch_related("standings__team")
    return {group.short_name: list(group.standings.order_by("rank", "-points", "-goal_difference")) for group in groups}


def _third_place_teams(standings: dict[str, list[Standing]]) -> dict[str, Standing]:
    thirds = [rows[2] for rows in standings.values() if len(rows) >= 3 and rows[2].played > 0]
    ranked = sorted(thirds, key=lambda row: (-row.points, -row.goal_difference, -row.goals_for, row.team.name))
    return {standing.group.short_name: standing for standing in ranked}


def _resolve_group_source(
    source: str,
    standings: dict[str, list[Standing]],
    third_place: dict[str, Standing],
):
    if not source:
        return None
    if len(source) == 2 and source[0] in {"1", "2"}:
        rank = int(source[0]) - 1
        rows = standings.get(source[1], [])
        return rows[rank].team if len(rows) > rank else None
    if source.startswith("3"):
        for group_name in source[1:].split("/"):
            standing = third_place.get(group_name)
            if standing:
                return standing.team
    return None
