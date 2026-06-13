from __future__ import annotations

from apps.matches.constants import MatchStatus
from apps.matches.models import Match


def advance_winner(match: Match):
    """Advance a finished knockout winner or loser into the configured next slot."""
    winner = get_winner(match)
    if winner is None:
        return None

    if not hasattr(match, "knockout") or not match.knockout.next_match:
        return winner

    target = match.knockout.next_match.match
    slot = match.knockout.next_slot
    fields: list[str] = []
    if slot == "home" and target.home_team_id != winner.id:
        target.home_team = winner
        fields.append("home_team")
    elif slot == "away" and target.away_team_id != winner.id:
        target.away_team = winner
        fields.append("away_team")
    if fields:
        target.save(update_fields=fields)
        target.knockout.home_team = target.home_team
        target.knockout.away_team = target.away_team
        target.knockout.save(update_fields=["home_team", "away_team"])
    return winner


def get_winner(match: Match):
    if match.status != MatchStatus.FINISHED or not match.home_team_id or not match.away_team_id:
        return None
    home_value = match.penalty_home_score
    away_value = match.penalty_away_score
    if home_value is None or away_value is None:
        home_value = match.extra_time_home_score
        away_value = match.extra_time_away_score
    if home_value is None or away_value is None:
        home_value = match.home_score
        away_value = match.away_score
    if home_value is None or away_value is None or home_value == away_value:
        return None
    return match.home_team if home_value > away_value else match.away_team
