"""
Hacky script used to populate databases from previously captured static data
"""

from math import isnan
import os
import pickle

import dateutil.parser
from dateutil.relativedelta import relativedelta

import sys

sys.path.append("../")
from tournament_rankings import r2022, r2023

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()
from marchmadness.models import School, Game, APRanking, TournamentRanking


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
                win=game["win"],
            )
            games_to_insert.append(game_model)
    Game.objects.bulk_create(games_to_insert)


def add_ap_ranking():
    with open("../db/school_data.pkl", "rb") as F:
        df = pickle.load(F)

    df = df[~df["Name"].duplicated(keep=False)]

    schools_to_insert = []
    for i, row in df.iterrows():
        if ap_ranking := row["AP Ranking"]:
            school = APRanking(school_name=row["Name"], ranking=ap_ranking, year=2023)
            schools_to_insert.append(school)
    APRanking.objects.bulk_create(schools_to_insert)


def add_tournament_rankings_helper(data, conference_name, year):
    schools = []
    play_in_rank = data.pop("play_in_rank")
    for rank, school_name in r2022.west.items():
        play_in = False
        if rank == play_in_rank or rank == "play_in":
            play_in = True
            rank = play_in_rank
        school = TournamentRanking(
            school_name=school_name,
            ranking=rank,
            conference=conference_name,
            play_in=play_in,
            year=year,
        )
        schools.append(school)
    return schools


def add_past_tournament_rankings():
    schools = []
    schools.extend(add_tournament_rankings_helper(r2022.west, "West", 2022))
    schools.extend(add_tournament_rankings_helper(r2022.east, "East", 2022))
    schools.extend(add_tournament_rankings_helper(r2022.south, "South", 2022))
    schools.extend(add_tournament_rankings_helper(r2022.midwest, "Midwest", 2022))
    schools.extend(add_tournament_rankings_helper(r2023.west, "West", 2023))
    schools.extend(add_tournament_rankings_helper(r2023.east, "East", 2023))
    schools.extend(add_tournament_rankings_helper(r2023.south, "South", 2023))
    schools.extend(add_tournament_rankings_helper(r2023.midwest, "Midwest", 2023))
    TournamentRanking.objects.bulk_create(schools)


if __name__ == "__main__":
    pass
