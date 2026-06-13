from __future__ import annotations

from django.contrib import messages
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from apps.matches.constants import MatchStatus
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


def _nullable_int(value: str | None) -> int | None:
    if value in {None, ""}:
        return None
    return int(value)
