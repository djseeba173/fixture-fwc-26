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
            name="Stadium",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("city", models.CharField(max_length=160, unique=True)),
                ("country", models.CharField(blank=True, max_length=80)),
                ("country_code", models.CharField(blank=True, max_length=8)),
                ("timezone", models.CharField(blank=True, max_length=32)),
                ("capacity", models.PositiveIntegerField(blank=True, null=True)),
                ("coords", models.CharField(blank=True, max_length=80)),
            ],
            options={"ordering": ["city"]},
        ),
        migrations.CreateModel(
            name="Match",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("match_number", models.PositiveIntegerField()),
                ("phase", models.CharField(choices=[("GROUP", "Group"), ("ROUND_OF_32", "Round of 32"), ("ROUND_OF_16", "Round of 16"), ("QUARTER_FINAL", "Quarter-final"), ("SEMI_FINAL", "Semi-final"), ("THIRD_PLACE", "Match for third place"), ("FINAL", "Final")], default="GROUP", max_length=32)),
                ("round_name", models.CharField(blank=True, max_length=80)),
                ("ground", models.CharField(blank=True, max_length=160)),
                ("date_time", models.DateTimeField(blank=True, null=True)),
                ("date", models.DateField(blank=True, null=True)),
                ("time_text", models.CharField(blank=True, max_length=40)),
                ("home_source", models.CharField(blank=True, max_length=40)),
                ("away_source", models.CharField(blank=True, max_length=40)),
                ("home_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("away_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("extra_time_home_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("extra_time_away_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("penalty_home_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("penalty_away_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("status", models.CharField(choices=[("scheduled", "Scheduled"), ("live", "Live"), ("finished", "Finished")], default="scheduled", max_length=16)),
                ("away_team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="away_matches", to="teams.team")),
                ("group", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="matches", to="tournaments.group")),
                ("home_team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="home_matches", to="teams.team")),
                ("stadium", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="matches", to="matches.stadium")),
                ("tournament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="matches", to="tournaments.tournament")),
            ],
            options={"ordering": ["date_time", "match_number"]},
        ),
        migrations.AddConstraint(
            model_name="match",
            constraint=models.UniqueConstraint(fields=("tournament", "match_number"), name="unique_match_number_per_tournament"),
        ),
    ]
