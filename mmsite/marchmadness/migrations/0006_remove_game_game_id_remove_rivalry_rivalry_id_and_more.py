# Generated by Django 4.2.5 on 2023-09-24 19:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marchmadness", "0005_apranking_year_tournamentranking_year"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="game",
            name="game_id",
        ),
        migrations.RemoveField(
            model_name="rivalry",
            name="rivalry_id",
        ),
        migrations.AddField(
            model_name="game",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=None,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="rivalry",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=None,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
    ]