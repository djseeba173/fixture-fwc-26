# Generated for the Mundial 2026 fixture project.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("teams", "0001_initial"),
        ("tournaments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Standing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("played", models.PositiveSmallIntegerField(default=0)),
                ("wins", models.PositiveSmallIntegerField(default=0)),
                ("draws", models.PositiveSmallIntegerField(default=0)),
                ("losses", models.PositiveSmallIntegerField(default=0)),
                ("goals_for", models.PositiveSmallIntegerField(default=0)),
                ("goals_against", models.PositiveSmallIntegerField(default=0)),
                ("goal_difference", models.IntegerField(default=0)),
                ("points", models.PositiveSmallIntegerField(default=0)),
                ("rank", models.PositiveSmallIntegerField(default=0)),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="standings", to="tournaments.group")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="standings", to="teams.team")),
            ],
            options={"ordering": ["group__name", "rank", "-points", "-goal_difference", "-goals_for", "team__name"]},
        ),
        migrations.AddConstraint(
            model_name="standing",
            constraint=models.UniqueConstraint(fields=("group", "team"), name="unique_group_team_standing"),
        ),
    ]
