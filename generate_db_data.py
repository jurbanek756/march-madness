#!/usr/bin/env python3

import argparse
from datetime import datetime
import logging
from pathlib import Path
import pickle

from data.games import get_regular_season_games
from data.schools import (
    get_all_d1_schools,
    add_names_to_schools,
    add_ap_rankings_to_dataframe,
    add_location_and_is_private_to_dataframe,
    add_rivals_to_dataframe,
    add_team_colors_to_dataframe,
)

logging.basicConfig(
    encoding="UTF-8",
    level="INFO",
    handlers=[
        logging.StreamHandler(),
    ],
    format="%(message)s",
)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-g",
    "--generate-games-db",
    action="store_true",
    default=False,
    help="Generates DB of games for the current season",
)
parser.add_argument(
    "-s",
    "--generate-schools-db",
    action="store_true",
    default=False,
    help="Generates DB of static data related to schools",
)
args = parser.parse_args()

if not args.generate_games_db and not args.generate_schools_db:
    logging.info("No db generation requested; run with --help to see options")
    exit(0)

Path("db").mkdir(exist_ok=True)

if args.generate_games_db:
    logging.info("Getting games data")
    current_year = datetime.now().year
    games = get_regular_season_games()
    logging.info("Saving to db")
    with open(f"db/{current_year-1}_{current_year}_games.pkl", "wb") as F:
        pickle.dump(games, F)

if args.generate_schools_db:
    logging.info("Getting school data")
    df = get_all_d1_schools()
    logging.info("Adding short names to schools")
    add_names_to_schools(df)
    logging.info("Adding AP rankings")
    add_ap_rankings_to_dataframe(df)
    logging.info("Adding team colors")
    add_team_colors_to_dataframe(df)
    logging.info("Adding location and is_private info")
    add_location_and_is_private_to_dataframe(df)
    logging.info("Adding rivalries")
    add_rivals_to_dataframe(df)
    logging.info("Saving to db")
    df.to_pickle("db/school_data.pkl")
