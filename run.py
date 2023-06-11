#!/usr/bin/env python

import logging
import pickle
import os

from helpers.group_dict import generate_full_region_dict
from helpers.random_number_seeding import seed_via_random_api
from models.tournament import Tournament


logging.basicConfig(
    encoding="UTF-8",
    level="INFO",
    handlers=[
        logging.FileHandler("NCAA_Tournament_Results.log"),
        logging.StreamHandler(),
    ],
    format="%(message)s",
)


# ----------------Vars to change----------------------------------
USE_CACHED_GAMES = True
GAMES_CACHE = "2022_2023_games.pkl"
LOG_RESULTS = True
from tournament_rankings.r2023 import west, east, south, midwest  # noqa
from evaluate.select_team import user_evaluation as prediction_method  # noqa

# -----------------------------------------------------------------


if random_api_key := os.getenv("RANDOM_API_KEY"):
    seed = seed_via_random_api(0, 10_000, random_api_key)
    print(f"Seeded with {seed}")


all_teams = set()
for region in west, east, south, midwest:
    for k, team in region.items():
        if k != "play_in_rank":
            all_teams.add(team)

if len(all_teams) != 68:
    print(len(all_teams))
    raise ValueError("Duplicate team found in source dict")

with open(f"db/{GAMES_CACHE}", "rb") as F:
    regular_season_games = pickle.load(F)

with open("db/school_data.pkl", "rb") as F:
    db = pickle.load(F).to_dict(orient="records")

west_play_in_rank = west.pop("play_in_rank")
west_teams = generate_full_region_dict(db, regular_season_games, west)

east_play_in_rank = east.pop("play_in_rank")
east_teams = generate_full_region_dict(db, regular_season_games, east)

south_play_in_rank = south.pop("play_in_rank")
south_teams = generate_full_region_dict(db, regular_season_games, south)

midwest_play_in_rank = midwest.pop("play_in_rank")
midwest_teams = generate_full_region_dict(db, regular_season_games, midwest)

tournament = Tournament(
    south_teams,
    east_teams,
    midwest_teams,
    west_teams,
    "South",
    "East",
    "Midwest",
    "West",
    south_play_in_rank,
    east_play_in_rank,
    midwest_play_in_rank,
    west_play_in_rank,
    prediction_method=prediction_method,
    log_results=LOG_RESULTS,
)

tournament.run()
