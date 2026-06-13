from django.contrib import admin

from apps.matches.models import Match, Stadium


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ("city", "name", "country", "capacity", "timezone")
    search_fields = ("city", "name", "country")
    list_filter = ("country",)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "match_number",
        "phase",
        "group",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
        "status",
        "date",
        "time_text",
    )
    list_editable = ("home_score", "away_score", "status")
    list_filter = ("phase", "status", "group")
    search_fields = ("home_team__name", "away_team__name", "home_source", "away_source", "ground")
    autocomplete_fields = ("home_team", "away_team", "group", "stadium", "tournament")
    ordering = ("match_number",)
