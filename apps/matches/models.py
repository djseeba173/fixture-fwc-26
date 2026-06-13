from __future__ import annotations

from django.db import models

from apps.matches.constants import MatchStatus, Phase


class Stadium(models.Model):
    name = models.CharField(max_length=160)
    city = models.CharField(max_length=160, unique=True)
    country = models.CharField(max_length=80, blank=True)
    country_code = models.CharField(max_length=8, blank=True)
    timezone = models.CharField(max_length=32, blank=True)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    coords = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["city"]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"


class Match(models.Model):
    tournament = models.ForeignKey("tournaments.Tournament", on_delete=models.CASCADE, related_name="matches")
    match_number = models.PositiveIntegerField()
    phase = models.CharField(max_length=32, choices=Phase.choices, default=Phase.GROUP)
    round_name = models.CharField(max_length=80, blank=True)
    group = models.ForeignKey(
        "tournaments.Group",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matches",
    )
    stadium = models.ForeignKey(Stadium, on_delete=models.SET_NULL, null=True, blank=True, related_name="matches")
    ground = models.CharField(max_length=160, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    time_text = models.CharField(max_length=40, blank=True)
    home_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_matches",
    )
    away_team = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="away_matches",
    )
    home_source = models.CharField(max_length=40, blank=True)
    away_source = models.CharField(max_length=40, blank=True)
    home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    extra_time_home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    extra_time_away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    penalty_home_score = models.PositiveSmallIntegerField(null=True, blank=True)
    penalty_away_score = models.PositiveSmallIntegerField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=MatchStatus.choices, default=MatchStatus.SCHEDULED)

    class Meta:
        ordering = ["date_time", "match_number"]
        constraints = [
            models.UniqueConstraint(fields=["tournament", "match_number"], name="unique_match_number_per_tournament"),
        ]

    def __str__(self) -> str:
        left = self.home_team.name if self.home_team else self.home_source
        right = self.away_team.name if self.away_team else self.away_source
        return f"#{self.match_number} {left} vs {right}"

    def save(self, *args: object, **kwargs: object) -> None:
        super().save(*args, **kwargs)
        if self.status == MatchStatus.FINISHED:
            if self.phase == Phase.GROUP and self.group_id:
                from services.standings import recalculate_group_standings, update_group_qualifications

                recalculate_group_standings(self.group)
                update_group_qualifications(self.tournament)
            elif self.phase != Phase.GROUP:
                from services.brackets import advance_winner

                advance_winner(self)
