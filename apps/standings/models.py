from __future__ import annotations

from django.db import models


class Standing(models.Model):
    group = models.ForeignKey("tournaments.Group", on_delete=models.CASCADE, related_name="standings")
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="standings")
    played = models.PositiveSmallIntegerField(default=0)
    wins = models.PositiveSmallIntegerField(default=0)
    draws = models.PositiveSmallIntegerField(default=0)
    losses = models.PositiveSmallIntegerField(default=0)
    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    rank = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["group__name", "rank", "-points", "-goal_difference", "-goals_for", "team__name"]
        constraints = [
            models.UniqueConstraint(fields=["group", "team"], name="unique_group_team_standing"),
        ]

    def __str__(self) -> str:
        return f"{self.group} - {self.team}"
