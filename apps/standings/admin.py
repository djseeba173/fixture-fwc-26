from django.contrib import admin

from apps.standings.models import Standing


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    list_display = ("group", "rank", "team", "played", "wins", "draws", "losses", "goal_difference", "points")
    list_filter = ("group",)
    search_fields = ("team__name",)
