from __future__ import annotations

from django.db import models


class KnockoutMatch(models.Model):
    match = models.OneToOneField("matches.Match", on_delete=models.CASCADE, related_name="knockout")
    match_number = models.PositiveIntegerField()
    phase = models.CharField(max_length=32)
    home_source = models.CharField(max_length=40, blank=True)
    away_source = models.CharField(max_length=40, blank=True)
    home_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="knockout_home_matches",
    )
    away_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="knockout_away_matches",
    )
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    next_match = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="previous_matches",
    )
    next_slot = models.CharField(max_length=8, blank=True)

    class Meta:
        ordering = ["match_number"]

    def __str__(self) -> str:
        return f"KO #{self.match_number}"
