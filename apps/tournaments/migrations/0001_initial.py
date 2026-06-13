# Generated for the Mundial 2026 fixture project.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("teams", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tournament",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("year", models.PositiveIntegerField()),
                ("slug", models.SlugField(unique=True)),
                ("start_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
            ],
            options={"ordering": ["-year", "name"]},
        ),
        migrations.CreateModel(
            name="Group",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=32)),
                ("tournament", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="groups", to="tournaments.tournament")),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="GroupMembership",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("group", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="tournaments.group")),
                ("team", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="memberships", to="teams.team")),
            ],
            options={"ordering": ["group__name", "team__name"]},
        ),
        migrations.AddField(
            model_name="group",
            name="teams",
            field=models.ManyToManyField(related_name="groups", through="tournaments.GroupMembership", to="teams.team"),
        ),
        migrations.AddConstraint(
            model_name="group",
            constraint=models.UniqueConstraint(fields=("tournament", "name"), name="unique_group_per_tournament"),
        ),
        migrations.AddConstraint(
            model_name="groupmembership",
            constraint=models.UniqueConstraint(fields=("group", "team"), name="unique_team_group_membership"),
        ),
    ]
