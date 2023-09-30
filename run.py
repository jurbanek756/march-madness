#!/usr/bin/env python

import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument(
    "-y",
    "--year",
    type=int,
    default=2023,
    help="Year of tournament; must be 2022 or later",
)
parser.add_argument(
    "-e",
    "--evaluate",
    action="store_true",
    default=False,
    help="Run evaluation mode where user manually selects teams to win",
)
parser.add_argument(
    "-p",
    "--predict",
    help="Runs prediction mode where teams are automatically selected using a "
    "prediction method. One of: ["
    "'random', "
    "'lptr', "
    "'sigmodal', "
    "'ranked', "
    "'ap', "
    "'nickname'"
    "]",
    default=None,
)
parser.add_argument(
    "-a",
    "--ap-rank-weight",
    type=float,
    default=0.75,
    help="Weight for AP rank in weighted predictions",
)
parser.add_argument(
    "-k",
    "--sigmodal-k",
    type=float,
    help="k value; for sigmodal prediction method only",
)
args = parser.parse_args()

if args.year == 2023:
    from tournament_rankings.r2023 import west, east, south, midwest

    GAMES_CACHE = "2022_2023_games.pkl"
elif args.year == 2022:
    from tournament_rankings.r2022 import west, east, south, midwest

    GAMES_CACHE = None
else:
    raise ValueError("Unhandled year provided")
if args.evaluate:
    from evaluate.select_team import user_evaluation as prediction_method

    if args.predict:
        raise ValueError("Cannot evaluate and predict at the same time")
elif args.predict:
    if args.predict.casefold() == "random":
        from predict.select_team import random_selection as prediction_method
    elif args.predict.casefold() == "lptr":
        from predict.select_team import (
            weighted_random_selection_lptr as prediction_method,
        )
    elif args.predict.casefold() == "sigmodal":
        from predict.select_team import (
            weighted_random_selection_sigmodal as prediction_method,
        )

        if not args.sigmodal_k:
            pass
    elif args.predict.casefold() == "ranked":
        from predict.select_team import ranked_selection as prediction_method
    elif args.predict.casefold() == "ap":
        from predict.select_team import ap_selection as prediction_method
    elif args.predict.casefold() == "nickname":
        from predict.sentiment_analysis import nickname_sentiment as prediction_method
else:
    from evaluate.select_team import user_evaluation as prediction_method

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

try:
    with open(f"db/{GAMES_CACHE}", "rb") as F:
        regular_season_games = pickle.load(F)
except FileNotFoundError:
    if args.evaluate:
        print(
            "Games not found. If before 2022, this is expected, "
            "else run generate_db_data.py script"
        )
        input("Press any key to continue")
    else:  # Currently prediction methods do not use games, so no need to warn
        pass
    regular_season_games = []

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
    prediction_method_kwargs={
        "ap_rank_weight": args.ap_rank_weight,
        "k": args.sigmodal_k,
    },
    log_results=True,
)

tournament.run()
