from django.contrib import admin

from apps.brackets.models import KnockoutMatch


@admin.register(KnockoutMatch)
class KnockoutMatchAdmin(admin.ModelAdmin):
    list_display = ("match_number", "phase", "home_source", "home_team", "away_source", "away_team", "next_match", "next_slot")
    list_filter = ("phase",)
    search_fields = ("match_number", "home_source", "away_source", "home_team__name", "away_team__name")
    autocomplete_fields = ("match", "home_team", "away_team", "next_match")
