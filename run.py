#!/usr/bin/env python

import json
import os

from data.games import get_regular_season_games
from tournament.helpers import generate_full_region_dict
from helpers.random_number_seeding import seed_via_random_api
from tournament.tournament import Tournament


# ----------------Vars to change----------------------------------
USE_CACHED_GAMES = True
GAMES_CACHE = "db/2022_2023_games.json"
LOG_RESULTS = True
from tournament_rankings.r2023 import west, east, south, midwest
from predict.select_team import weighted_random_selection as prediction_method

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

with open("db/school_data.json") as F:
    db = json.load(F)

if USE_CACHED_GAMES:
    with open(GAMES_CACHE) as F:
        regular_season_games = json.load(F)
else:
    regular_season_games = get_regular_season_games()

west_play_in_rank = west.pop("play_in_rank")
west_teams = generate_full_region_dict(db, regular_season_games, west)

east_play_in_rank = east.pop("play_in_rank")
east_teams = generate_full_region_dict(db, regular_season_games, east)

south_play_in_rank = south.pop("play_in_rank")
south_teams = generate_full_region_dict(db, regular_season_games, south)

midwest_play_in_rank = midwest.pop("play_in_rank")
midwest_teams = generate_full_region_dict(db, regular_season_games, midwest)
breakpoint()
tournament = Tournament(
    south_teams,
    east_teams,
    midwest_teams,
    west_teams,
    south_play_in_rank,
    east_play_in_rank,
    midwest_play_in_rank,
    west_play_in_rank,
    prediction_method=prediction_method,
    log_results=LOG_RESULTS,
)

tournament.run()
