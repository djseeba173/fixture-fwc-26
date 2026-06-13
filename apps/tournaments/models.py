from __future__ import annotations

from django.db import models


class Tournament(models.Model):
    name = models.CharField(max_length=120)
    year = models.PositiveIntegerField()
    slug = models.SlugField(unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-year", "name"]

    def __str__(self) -> str:
        return self.name


class Group(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=32)
    teams = models.ManyToManyField("teams.Team", through="GroupMembership", related_name="groups")

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=["tournament", "name"], name="unique_group_per_tournament"),
        ]

    @property
    def short_name(self) -> str:
        return self.name.replace("Group ", "")

    def __str__(self) -> str:
        return self.name


class GroupMembership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="memberships")
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, related_name="memberships")

    class Meta:
        ordering = ["group__name", "team__name"]
        constraints = [
            models.UniqueConstraint(fields=["group", "team"], name="unique_team_group_membership"),
        ]

    def __str__(self) -> str:
        return f"{self.team} in {self.group}"
