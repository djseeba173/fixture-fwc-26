from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from django.db import transaction
from django.template.defaultfilters import slugify

from apps.brackets.models import KnockoutMatch
from apps.matches.constants import MatchStatus, Phase, ROUND_TO_PHASE
from apps.matches.models import Match, Stadium
from apps.teams.models import Team
from apps.tournaments.models import Group, GroupMembership, Tournament

COUNTRY_BY_CC = {"ca": "Canada", "mx": "Mexico", "us": "United States"}


@dataclass(frozen=True)
class ImportSummary:
    tournaments: int
    teams: int
    groups: int
    stadiums: int
    matches: int
    knockout_matches: int


def import_worldcup_data(data_dir: Path) -> ImportSummary:
    """Import the 2026 JSON files idempotently."""
    worldcup = _load_json(data_dir / "worldcup.json")
    teams_data = _ensure_list(_load_json(data_dir / "worldcup.teams.json"), "teams")
    groups_data = _ensure_list(_load_json(data_dir / "worldcup.groups.json"), "groups")
    stadiums_data = _ensure_list(_load_json(data_dir / "worldcup.stadiums.json"), "stadiums")
    matches_data = worldcup.get("matches", [])

    dates = [_parse_date(match.get("date")) for match in matches_data if match.get("date")]
    tournament, _ = Tournament.objects.update_or_create(
        slug=slugify(worldcup.get("name", "World Cup 2026")),
        defaults={
            "name": worldcup.get("name", "World Cup 2026"),
            "year": 2026,
            "start_date": min(dates) if dates else None,
            "end_date": max(dates) if dates else None,
        },
    )

    with transaction.atomic():
        teams = _import_teams(teams_data)
        groups = _import_groups(tournament, groups_data, teams)
        stadiums = _import_stadiums(stadiums_data)
        _import_matches(tournament, matches_data, teams, groups, stadiums)
        _link_knockout_matches(tournament)

    return ImportSummary(
        tournaments=1,
        teams=Team.objects.count(),
        groups=tournament.groups.count(),
        stadiums=Stadium.objects.count(),
        matches=tournament.matches.count(),
        knockout_matches=KnockoutMatch.objects.count(),
    )


def _load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def _ensure_list(payload: Any, key: str) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    return payload.get(key, [])


def _import_teams(teams_data: list[dict[str, Any]]) -> dict[str, Team]:
    teams: dict[str, Team] = {}
    for item in teams_data:
        team, _ = Team.objects.update_or_create(
            name=item["name"],
            defaults={
                "code": item.get("fifa_code", ""),
                "fifa_code": item.get("fifa_code", ""),
                "flag_icon": item.get("flag_icon", ""),
                "flag_unicode": item.get("flag_unicode", ""),
                "confederation": item.get("confed", ""),
                "continent": item.get("continent", ""),
                "normalised_name": item.get("name_normalised", ""),
            },
        )
        teams[team.name] = team
    return teams


def _import_groups(
    tournament: Tournament,
    groups_data: list[dict[str, Any]],
    teams: dict[str, Team],
) -> dict[str, Group]:
    groups: dict[str, Group] = {}
    for item in groups_data:
        group, _ = Group.objects.update_or_create(tournament=tournament, name=item["name"])
        groups[group.name] = group
        groups[group.short_name] = group
        for team_name in item.get("teams", []):
            team = teams.get(team_name)
            if team:
                GroupMembership.objects.update_or_create(group=group, team=team)
    return groups


def _import_stadiums(stadiums_data: list[dict[str, Any]]) -> dict[str, Stadium]:
    stadiums: dict[str, Stadium] = {}
    for item in stadiums_data:
        stadium, _ = Stadium.objects.update_or_create(
            city=item["city"],
            defaults={
                "name": item.get("name", item["city"]),
                "country": COUNTRY_BY_CC.get(item.get("cc", ""), ""),
                "country_code": item.get("cc", ""),
                "timezone": item.get("timezone", ""),
                "capacity": item.get("capacity"),
                "coords": item.get("coords", ""),
            },
        )
        stadiums[stadium.city] = stadium
    return stadiums


def _import_matches(
    tournament: Tournament,
    matches_data: list[dict[str, Any]],
    teams: dict[str, Team],
    groups: dict[str, Group],
    stadiums: dict[str, Stadium],
) -> None:
    for index, item in enumerate(matches_data, start=1):
        match_number = item.get("num") or index
        score = _normalise_score(item.get("score"))
        group = groups.get(item.get("group", ""))
        phase = ROUND_TO_PHASE.get(item.get("round", ""), Phase.GROUP)
        date_value = _parse_date(item.get("date"))
        home_team = teams.get(item.get("team1", ""))
        away_team = teams.get(item.get("team2", ""))
        home_source = "" if home_team else item.get("team1", "")
        away_source = "" if away_team else item.get("team2", "")

        defaults = {
            "phase": phase,
            "round_name": item.get("round", ""),
            "group": group,
            "stadium": stadiums.get(item.get("ground", "")),
            "ground": item.get("ground", ""),
            "date": date_value,
            "time_text": item.get("time", ""),
            "date_time": _parse_datetime(date_value, item.get("time", "")),
            "home_team": home_team,
            "away_team": away_team,
            "home_source": home_source,
            "away_source": away_source,
        }

        existing = Match.objects.filter(tournament=tournament, match_number=match_number).first()
        # El marcador solo se toca si el JSON lo trae, o si el partido aun no tiene resultado.
        # Asi los resultados cargados a mano (web o seed_results) sobreviven a cada re-deploy
        # en vez de ser reseteados a SCHEDULED por la reimportacion del fixture base.
        if score:
            defaults.update({
                "home_score": score.get("ft", (None, None))[0],
                "away_score": score.get("ft", (None, None))[1],
                "extra_time_home_score": score.get("et", (None, None))[0],
                "extra_time_away_score": score.get("et", (None, None))[1],
                "penalty_home_score": score.get("p", (None, None))[0],
                "penalty_away_score": score.get("p", (None, None))[1],
                "status": MatchStatus.FINISHED,
            })
        elif existing is None or existing.status != MatchStatus.FINISHED:
            defaults.update({
                "home_score": None,
                "away_score": None,
                "extra_time_home_score": None,
                "extra_time_away_score": None,
                "penalty_home_score": None,
                "penalty_away_score": None,
                "status": MatchStatus.SCHEDULED,
            })
        # else: el partido ya tiene resultado y el JSON no trae nada -> se preserva intacto.

        match, _ = Match.objects.update_or_create(
            tournament=tournament,
            match_number=match_number,
            defaults=defaults,
        )
        if phase != Phase.GROUP:
            KnockoutMatch.objects.update_or_create(
                match=match,
                defaults={
                    "match_number": match.match_number,
                    "phase": match.phase,
                    "home_source": match.home_source,
                    "away_source": match.away_source,
                    "home_team": match.home_team,
                    "away_team": match.away_team,
                    "home_score": match.home_score,
                    "away_score": match.away_score,
                },
            )


def _link_knockout_matches(tournament: Tournament) -> None:
    knockouts = {ko.match_number: ko for ko in KnockoutMatch.objects.select_related("match")}
    for ko in knockouts.values():
        next_match = None
        next_slot = ""
        winner_token = f"W{ko.match_number}"
        loser_token = f"L{ko.match_number}"
        for candidate in knockouts.values():
            if candidate.home_source == winner_token or candidate.home_source == loser_token:
                next_match = candidate
                next_slot = "home"
                break
            if candidate.away_source == winner_token or candidate.away_source == loser_token:
                next_match = candidate
                next_slot = "away"
                break
        if ko.next_match_id != (next_match.id if next_match else None) or ko.next_slot != next_slot:
            ko.next_match = next_match
            ko.next_slot = next_slot
            ko.save(update_fields=["next_match", "next_slot"])


def _normalise_score(score: Any) -> dict[str, tuple[int | None, int | None]]:
    if not score:
        return {}
    if isinstance(score, list):
        return {"ft": tuple(score)}  # type: ignore[return-value]
    return {key: tuple(value) for key, value in score.items() if isinstance(value, list)}


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


def _parse_datetime(date_value: date | None, time_value: str) -> datetime | None:
    if not date_value or not time_value:
        return None
    match = re.match(r"(?P<hour>\d{1,2}):(?P<minute>\d{2})(?:\s+UTC(?P<offset>[+-]\d+))?", time_value)
    if not match:
        return datetime.combine(date_value, datetime.min.time(), tzinfo=timezone.utc)
    hour = int(match.group("hour"))
    minute = int(match.group("minute"))
    offset = match.group("offset")
    tz = timezone(timedelta(hours=int(offset))) if offset else timezone.utc
    return datetime(date_value.year, date_value.month, date_value.day, hour, minute, tzinfo=tz).astimezone(timezone.utc)
