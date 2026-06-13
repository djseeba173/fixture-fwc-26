from django.db import models


class Phase(models.TextChoices):
    GROUP = "GROUP", "Group"
    ROUND_OF_32 = "ROUND_OF_32", "Round of 32"
    ROUND_OF_16 = "ROUND_OF_16", "Round of 16"
    QUARTER_FINAL = "QUARTER_FINAL", "Quarter-final"
    SEMI_FINAL = "SEMI_FINAL", "Semi-final"
    THIRD_PLACE = "THIRD_PLACE", "Match for third place"
    FINAL = "FINAL", "Final"


class MatchStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Scheduled"
    LIVE = "live", "Live"
    FINISHED = "finished", "Finished"


ROUND_TO_PHASE = {
    "Round of 32": Phase.ROUND_OF_32,
    "Round of 16": Phase.ROUND_OF_16,
    "Quarter-final": Phase.QUARTER_FINAL,
    "Semi-final": Phase.SEMI_FINAL,
    "Match for third place": Phase.THIRD_PLACE,
    "Final": Phase.FINAL,
}
