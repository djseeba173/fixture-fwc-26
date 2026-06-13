from __future__ import annotations

from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=120, unique=True)
    code = models.CharField(max_length=12, blank=True)
    fifa_code = models.CharField(max_length=12, blank=True)
    flag_url = models.URLField(blank=True)
    flag_icon = models.CharField(max_length=16, blank=True)
    flag_unicode = models.CharField(max_length=64, blank=True)
    confederation = models.CharField(max_length=32, blank=True)
    continent = models.CharField(max_length=64, blank=True)
    normalised_name = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name
