import pickle
import os
import dateutil.parser
from dateutil.relativedelta import relativedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()
from marchmadness.models import School, Game

from math import isnan
import sys

sys.path.append("../")

"""
Hacky script used to populate databases from prevously captured static data
"""


def get_parens_num(prov_str):
    return int(prov_str.split(")")[0].split("(")[1])


def insert_bool(val):
    if isnan(val):
        return False
    return val


def date_from_str(date_str):
    date = dateutil.parser.parse(date_str).date()
    if date.month > 4:
        date -= relativedelta(years=1)
    return date


def parse_score(score):
    score_split = score.split("-")
    return int(score_split[0]), int(score_split[1])


def add_schools():
    with open("../db/school_data.pkl", "rb") as F:
        df = pickle.load(F)

    df = df[~df["Name"].duplicated(keep=False)]

    schools_to_insert = []
    for i, row in df.iterrows():
        school = School(
            name=row["Name"],
            formal_name=row["School"],
            nickname=row["Nickname"],
            home_arena=row["Home arena"],
            conference=row["Conference"],
            tournament_appearances=get_parens_num(row["Tournament appearances"]),
            final_four_appearances=get_parens_num(row["Final Four appearances"]),
            championship_wins=get_parens_num(row["Championship wins"]),
            primary_color=row["Primary Color"],
            secondary_color=row["Secondary Color"],
            location=row["Location"],
            is_private=insert_bool(row["Is Private"]),
        )
        schools_to_insert.append(school)

    School.objects.bulk_create(schools_to_insert)


def add_games():
    with open("../db/2022_2023_games.pkl", "rb") as F:
        games_dict = pickle.load(F)

    games_to_insert = []
    for school, games in games_dict.items():
        for game in games:
            try:
                home_score, away_score = parse_score(game["score"])
            except ValueError:
                continue
            game_model = Game(
                date=date_from_str(game["game_date"]),
                season="2022-2023",
                school_name=school,
                opponent=game["opponent"],
                school_score=home_score,
                opponent_score=away_score,
                win=game["win"]
            )
            games_to_insert.append(game_model)
    Game.objects.bulk_create(games_to_insert)


if __name__ == "__main__":
    pass
