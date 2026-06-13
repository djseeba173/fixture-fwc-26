# Generated for the Mundial 2026 fixture project.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("matches", "0001_initial"),
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="KnockoutMatch",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("match_number", models.PositiveIntegerField()),
                ("phase", models.CharField(max_length=32)),
                ("home_source", models.CharField(blank=True, max_length=40)),
                ("away_source", models.CharField(blank=True, max_length=40)),
                ("home_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("away_score", models.PositiveSmallIntegerField(blank=True, null=True)),
                ("away_team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="knockout_away_matches", to="teams.team")),
                ("home_team", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="knockout_home_matches", to="teams.team")),
                ("match", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="knockout", to="matches.match")),
                ("next_match", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="previous_matches", to="brackets.knockoutmatch")),
                ("next_slot", models.CharField(blank=True, max_length=8)),
            ],
            options={"ordering": ["match_number"]},
        ),
    ]
