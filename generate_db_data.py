"""
Hacky script used to populate databases from previously captured static data
"""

# Regular Imports
import argparse
import datetime
import logging
from math import isnan
import os

from bs4 import BeautifulSoup
import dateutil.parser
from dateutil.relativedelta import relativedelta
import requests

from data.games import get_regular_season_games
from data.schools import (
    get_all_d1_schools,
    add_names_to_schools,
    add_location_and_is_private_to_dataframe,
    add_team_colors_to_dataframe,
)

# Django setup to use models
import sys

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()

from marchmadness.models import School, Game, APRanking, TournamentRanking

# Constants
AP_RANKINGS = "https://www.ncaa.com/rankings/basketball-men/d1/associated-press"

logging.basicConfig(
    encoding="UTF-8",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
    format="%(message)s",
)


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
    logging.info("Getting school data")
    df = get_all_d1_schools()
    logging.info("Adding short names to schools")
    add_names_to_schools(df)
    logging.info("Adding team colors")
    add_team_colors_to_dataframe(df)
    logging.info("Adding location and is_private info")
    add_location_and_is_private_to_dataframe(df)
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


def add_games(year):
    previous_year = year - 1
    games_dict = get_regular_season_games(year)
    games_to_insert = []
    for school, games in games_dict.items():
        for game in games:
            try:
                home_score, away_score = parse_score(game["score"])
            except ValueError:
                continue
            game_model = Game(
                date=date_from_str(game["game_date"]),
                season=f"{previous_year}-{year}",
                school_name=school,
                opponent=game["opponent"],
                school_score=home_score,
                opponent_score=away_score,
                home_game=game["home_game"],
                win=game["win"],
            )
            games_to_insert.append(game_model)
    Game.objects.bulk_create(games_to_insert)


def add_ap_ranking():
    data = requests.get(AP_RANKINGS).content
    ap_ranks = BeautifulSoup(data, "html.parser")
    schools_to_insert = list()
    for d in ap_ranks.find("table").find_all("tr")[1:]:
        td = d.find_all("td")
        name = td[1].string.split("(")[0].strip()
        ap_replacement_dict = {"San Diego State": "SDSU"}
        if name in ap_replacement_dict:
            name = ap_replacement_dict[name]
        ranking = int(td[0].string)
        school = APRanking(school_name=name, ranking=ranking, year=2023)
        schools_to_insert.append(school)
    APRanking.objects.bulk_create(schools_to_insert)


def add_tournament_rankings_helper(data, conference_name, year):
    schools = []
    play_in_rank = data.pop("play_in_rank")
    for rank, school_name in data.items():
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


def add_tournament_rankings(year):
    schools = []
    if year == 2022:
        import tournament_rankings.r2022 as ranking_year
    elif year == 2023:
        import tournament_rankings.r2023 as ranking_year
    else:
        logging.error("Unhandled year provided")
        return
    schools.extend(add_tournament_rankings_helper(ranking_year.west, "West", year))
    schools.extend(add_tournament_rankings_helper(ranking_year.east, "East", year))
    schools.extend(add_tournament_rankings_helper(ranking_year.south, "South", year))
    schools.extend(
        add_tournament_rankings_helper(ranking_year.midwest, "Midwest", year)
    )
    TournamentRanking.objects.bulk_create(schools)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--schools",
        action="store_true",
        default=False,
        help="If set, will add schools data to database",
    )
    parser.add_argument("-y", "--year", type=int, required=True)
    args = parser.parse_args()
    if args.schools:
        logging.info("Adding schools data")
        add_schools()
    add_games(args.year)
    if args.year == datetime.datetime.now().year:
        add_ap_ranking()
    else:
        logging.warning("Unable to add AP rankings for previous years")
    add_tournament_rankings(args.year)
