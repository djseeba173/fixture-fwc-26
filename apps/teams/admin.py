from django.contrib import admin

from apps.teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "fifa_code", "confederation", "continent", "flag_icon")
    search_fields = ("name", "fifa_code", "confederation")
    list_filter = ("confederation", "continent")
