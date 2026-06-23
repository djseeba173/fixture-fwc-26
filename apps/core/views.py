from __future__ import annotations

import json
from collections import defaultdict

from django.contrib import messages
from django.db.models import F, Q, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.matches.constants import MatchStatus, Phase
from apps.matches.models import Match
from apps.tournaments.models import Group, Tournament


def _tournament() -> Tournament | None:
    return Tournament.objects.order_by("-year").first()


def home(request: HttpRequest) -> HttpResponse:
    tournament = _tournament()
    upcoming = Match.objects.filter(status=MatchStatus.SCHEDULED).select_related("home_team", "away_team", "stadium")[:8]
    results = Match.objects.filter(status=MatchStatus.FINISHED).select_related("home_team", "away_team").order_by("-date_time")[:8]
    groups = Group.objects.select_related("tournament").prefetch_related("teams").filter(tournament=tournament)
    return render(request, "core/home.html", {"tournament": tournament, "upcoming": upcoming, "results": results, "groups": groups})


def group_list(request: HttpRequest) -> HttpResponse:
    groups = Group.objects.select_related("tournament").prefetch_related("teams", "standings__team")
    return render(request, "groups/list.html", {"groups": groups})


def group_detail(request: HttpRequest, name: str) -> HttpResponse:
    group_name = name if name.startswith("Group ") else f"Group {name.upper()}"
    group = get_object_or_404(
        Group.objects.prefetch_related("teams", "standings__team", "matches__home_team", "matches__away_team"),
        name=group_name,
    )
    return render(request, "groups/detail.html", {"group": group})


def fixture_list(request: HttpRequest) -> HttpResponse:
    matches = Match.objects.select_related("home_team", "away_team", "group", "stadium").order_by("date_time", "match_number")
    return render(request, "matches/list.html", {"matches": matches})


def match_detail(request: HttpRequest, pk: int) -> HttpResponse:
    match = get_object_or_404(Match.objects.select_related("home_team", "away_team", "group", "stadium"), pk=pk)
    return render(request, "matches/detail.html", {"match": match})


def save_result(request: HttpRequest, pk: int) -> HttpResponse:
    match = get_object_or_404(Match, pk=pk)
    if request.method == "POST":
        match.home_score = _nullable_int(request.POST.get("home_score"))
        match.away_score = _nullable_int(request.POST.get("away_score"))
        match.extra_time_home_score = _nullable_int(request.POST.get("extra_time_home_score"))
        match.extra_time_away_score = _nullable_int(request.POST.get("extra_time_away_score"))
        match.penalty_home_score = _nullable_int(request.POST.get("penalty_home_score"))
        match.penalty_away_score = _nullable_int(request.POST.get("penalty_away_score"))
        match.status = request.POST.get("status", MatchStatus.FINISHED)
        match.save()
        messages.success(request, "Resultado guardado.")
    if getattr(request, "htmx", False) and match.group_id:
        return render(request, "groups/_standings.html", {"group": match.group})
    return redirect("match_detail", pk=match.pk)


def bracket(request: HttpRequest) -> HttpResponse:
    matches = Match.objects.filter(~Q(phase="GROUP")).select_related("home_team", "away_team", "knockout").order_by("match_number")
    by_phase: dict[str, list[Match]] = {}
    for match in matches:
        by_phase.setdefault(match.phase, []).append(match)
    return render(request, "brackets/detail.html", {"by_phase": by_phase})


def stats(request: HttpRequest) -> HttpResponse:
    finished = Match.objects.filter(status=MatchStatus.FINISHED).select_related("home_team", "away_team", "group")

    total_matches = finished.count()
    agg = finished.aggregate(g=Sum(F("home_score") + F("away_score")))
    total_goals = agg["g"] or 0
    avg_gpm = round(total_goals / total_matches, 2) if total_matches else 0

    home_wins = finished.filter(home_score__gt=F("away_score")).count()
    away_wins = finished.filter(away_score__gt=F("home_score")).count()
    draws = finished.filter(home_score=F("away_score")).count()

    team_scored: dict[str, int] = defaultdict(int)
    team_conceded: dict[str, int] = defaultdict(int)
    team_played: dict[str, int] = defaultdict(int)

    for m in finished:
        if m.home_team and m.home_score is not None and m.away_score is not None:
            team_scored[m.home_team.name] += m.home_score
            team_conceded[m.home_team.name] += m.away_score
            team_played[m.home_team.name] += 1
        if m.away_team and m.home_score is not None and m.away_score is not None:
            team_scored[m.away_team.name] += m.away_score
            team_conceded[m.away_team.name] += m.home_score
            team_played[m.away_team.name] += 1

    top_scored = sorted(team_scored.items(), key=lambda x: -x[1])[:15]
    top_defense = sorted(
        [(k, v) for k, v in team_conceded.items() if team_played[k] >= 2],
        key=lambda x: x[1],
    )[:15]
    gpm_list = sorted(
        [(k, round(team_scored[k] / team_played[k], 2)) for k in team_played if team_played[k] >= 1],
        key=lambda x: -x[1],
    )[:15]

    phase_order = [Phase.GROUP, Phase.ROUND_OF_32, Phase.ROUND_OF_16, Phase.QUARTER_FINAL, Phase.SEMI_FINAL, Phase.THIRD_PLACE, Phase.FINAL]
    phase_labels = {
        Phase.GROUP: "Fase de grupos",
        Phase.ROUND_OF_32: "Ronda de 32",
        Phase.ROUND_OF_16: "Octavos",
        Phase.QUARTER_FINAL: "Cuartos",
        Phase.SEMI_FINAL: "Semifinales",
        Phase.THIRD_PLACE: "3er puesto",
        Phase.FINAL: "Final",
    }
    goals_by_phase = []
    for phase in phase_order:
        r = finished.filter(phase=phase).aggregate(g=Sum(F("home_score") + F("away_score")))
        if r["g"]:
            goals_by_phase.append((phase_labels[phase], r["g"]))

    goals_by_group = []
    for group in Group.objects.all():
        r = finished.filter(group=group).aggregate(g=Sum(F("home_score") + F("away_score")))
        if r["g"]:
            goals_by_group.append((group.name.replace("Group ", "G"), r["g"]))
    goals_by_group.sort(key=lambda x: x[0])

    top_matches = sorted(
        [
            {
                "label": f"{(m.home_team.name if m.home_team else m.home_source)} {m.home_score}-{m.away_score} {(m.away_team.name if m.away_team else m.away_source)}",
                "total": m.home_score + m.away_score,
                "pk": m.pk,
            }
            for m in finished
            if m.home_score is not None and m.away_score is not None
        ],
        key=lambda x: -x["total"],
    )[:8]

    cumulative = 0
    goals_over_time = []
    for m in finished.order_by("match_number"):
        if m.home_score is not None and m.away_score is not None:
            cumulative += m.home_score + m.away_score
            goals_over_time.append({"match": m.match_number, "total": cumulative, "goals": m.home_score + m.away_score})

    ctx = {
        "total_matches": total_matches,
        "total_goals": total_goals,
        "avg_gpm": avg_gpm,
        "home_wins": home_wins,
        "away_wins": away_wins,
        "draws": draws,
        "top_matches": top_matches,
        "j_scored": json.dumps({"labels": [x[0] for x in top_scored], "data": [x[1] for x in top_scored]}),
        "j_defense": json.dumps({"labels": [x[0] for x in top_defense], "data": [x[1] for x in top_defense]}),
        "j_gpm": json.dumps({"labels": [x[0] for x in gpm_list], "data": [x[1] for x in gpm_list]}),
        "j_phase": json.dumps({"labels": [x[0] for x in goals_by_phase], "data": [x[1] for x in goals_by_phase]}),
        "j_group": json.dumps({"labels": [x[0] for x in goals_by_group], "data": [x[1] for x in goals_by_group]}),
        "j_results": json.dumps({"data": [home_wins, draws, away_wins]}),
        "j_timeline": json.dumps({
            "labels": [x["match"] for x in goals_over_time],
            "goals": [x["goals"] for x in goals_over_time],
            "cumulative": [x["total"] for x in goals_over_time],
        }),
    }
    return render(request, "stats/dashboard.html", ctx)


def _nullable_int(value: str | None) -> int | None:
    if value in {None, ""}:
        return None
    return int(value)
