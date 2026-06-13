# Generated for the Mundial 2026 fixture project.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Team",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True)),
                ("code", models.CharField(blank=True, max_length=12)),
                ("fifa_code", models.CharField(blank=True, max_length=12)),
                ("flag_url", models.URLField(blank=True)),
                ("flag_icon", models.CharField(blank=True, max_length=16)),
                ("flag_unicode", models.CharField(blank=True, max_length=64)),
                ("confederation", models.CharField(blank=True, max_length=32)),
                ("continent", models.CharField(blank=True, max_length=64)),
                ("normalised_name", models.CharField(blank=True, max_length=120)),
            ],
            options={"ordering": ["name"]},
        ),
    ]
