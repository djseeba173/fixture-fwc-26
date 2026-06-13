from __future__ import annotations

from rest_framework import serializers, status, viewsets
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView

from apps.brackets.models import KnockoutMatch
from apps.matches.constants import MatchStatus
from apps.matches.models import Match
from apps.standings.models import Standing
from apps.teams.models import Team
from apps.tournaments.models import Group


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ("id", "name", "code", "fifa_code", "flag_icon", "confederation", "continent")


class GroupSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ("id", "name", "teams")


class MatchSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    group = serializers.StringRelatedField()
    stadium = serializers.StringRelatedField()

    class Meta:
        model = Match
        fields = (
            "id",
            "match_number",
            "phase",
            "round_name",
            "group",
            "stadium",
            "ground",
            "date_time",
            "date",
            "time_text",
            "home_team",
            "away_team",
            "home_source",
            "away_source",
            "home_score",
            "away_score",
            "extra_time_home_score",
            "extra_time_away_score",
            "penalty_home_score",
            "penalty_away_score",
            "status",
        )


class StandingSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    group = serializers.StringRelatedField()

    class Meta:
        model = Standing
        fields = ("id", "group", "rank", "team", "played", "wins", "draws", "losses", "goals_for", "goals_against", "goal_difference", "points")


class KnockoutMatchSerializer(serializers.ModelSerializer):
    match = MatchSerializer(read_only=True)

    class Meta:
        model = KnockoutMatch
        fields = ("id", "match_number", "phase", "home_source", "away_source", "match", "next_match", "next_slot")


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.prefetch_related("teams").order_by("name")
    serializer_class = GroupSerializer


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Match.objects.select_related("home_team", "away_team", "group", "stadium").order_by("match_number")
    serializer_class = MatchSerializer


class StandingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Standing.objects.select_related("team", "group").order_by("group__name", "rank")
    serializer_class = StandingSerializer


class BracketViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = KnockoutMatch.objects.select_related("match", "home_team", "away_team", "next_match").order_by("match_number")
    serializer_class = KnockoutMatchSerializer


class MatchResultView(APIView):
    def post(self, request, pk: int):
        match = Match.objects.get(pk=pk)
        for field in (
            "home_score",
            "away_score",
            "extra_time_home_score",
            "extra_time_away_score",
            "penalty_home_score",
            "penalty_away_score",
        ):
            if field in request.data:
                setattr(match, field, request.data[field])
        match.status = request.data.get("status", MatchStatus.FINISHED)
        match.save()
        return Response(MatchSerializer(match).data, status=status.HTTP_200_OK)


router = DefaultRouter()
router.register("groups", GroupViewSet)
router.register("teams", TeamViewSet)
router.register("matches", MatchViewSet)
router.register("standings", StandingViewSet)
router.register("bracket", BracketViewSet)
