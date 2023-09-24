# Generated by Django 4.2.5 on 2023-09-24 17:57

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                ("game_id", models.IntegerField(primary_key=True, serialize=False)),
                ("date", models.DateField()),
                ("season", models.CharField(max_length=9)),
                ("home_team", models.CharField(max_length=58)),
                ("away_team", models.CharField(max_length=58)),
                ("home_score", models.IntegerField()),
                ("away_score", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Rivalry",
            fields=[
                ("rivalry_id", models.IntegerField(primary_key=True, serialize=False)),
                ("team1", models.CharField(max_length=58)),
                ("team2", models.CharField(max_length=58)),
            ],
        ),
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "name",
                    models.CharField(max_length=58, primary_key=True, serialize=False),
                ),
                ("formal_name", models.CharField(max_length=69)),
                ("nickname", models.CharField(max_length=30)),
                ("home_arena", models.CharField(max_length=60)),
                ("conference", models.CharField(max_length=30)),
                ("tournament_appearances", models.IntegerField()),
                ("primary_color", models.CharField(max_length=20)),
                ("secondary_color", models.CharField(max_length=20)),
                ("location", models.CharField(max_length=50)),
                ("is_private", models.BooleanField()),
            ],
        ),
    ]
