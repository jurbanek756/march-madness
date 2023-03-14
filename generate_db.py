#!/usr/bin/env python3

from pathlib import Path

from team.dataframe import (
    get_all_d1_schools,
    filter_schools_without_tournament_appearance,
    add_names_to_schools,
    add_ap_rankings_to_dataframe,
    add_location_and_is_private_to_dataframe,
    add_rivals_to_dataframe,
    add_team_colors_to_dataframe,
)

Path("db").mkdir(exist_ok=True)

TOURNAMENT_RANKINGS_AVAILABLE = False

df = get_all_d1_schools()
df = filter_schools_without_tournament_appearance(df)
add_names_to_schools(df)
add_ap_rankings_to_dataframe(df)
add_team_colors_to_dataframe(df)
add_location_and_is_private_to_dataframe(df)
add_rivals_to_dataframe(df)

df.to_pickle("saved_static_data/school_data_dataframe.pkl")
df.to_json("db/school_data.json", orient="records")
