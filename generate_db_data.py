#!/usr/bin/env python3

from datetime import datetime
import logging
from pathlib import Path
import pickle

from data.games import get_regular_season_games

from data.schools import (
    get_all_d1_schools,
    filter_schools_without_tournament_appearance,
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

Path("db").mkdir(exist_ok=True)

GENERATE_GAMES_DB = True
GENERATE_SCHOOLS_DB = True

if GENERATE_GAMES_DB:
    logging.info("Getting games data")
    current_year = datetime.now().year
    games = get_regular_season_games()
    logging.info("Saving to db")
    with open(f"db/{current_year-1}_{current_year}_games.pkl", "wb") as F:
        pickle.dump(games, F)

if GENERATE_SCHOOLS_DB:
    logging.info("Getting school data")
    df = get_all_d1_schools()
    logging.info("Filtering schools without a tournament appearance")
    df = filter_schools_without_tournament_appearance(df)
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
