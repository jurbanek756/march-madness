#!/usr/bin/env python3

from team.dataframe import (
    get_all_d1_schools,
    add_ap_rankings_to_dataframe,
    add_location_and_is_private_to_dataframe,
    add_tournament_rankings_to_dataframe_from_csv,
    add_team_colors_to_dataframe,
)

TOURNAMENT_RANKINGS_AVAILABLE = False

df = get_all_d1_schools()
add_ap_rankings_to_dataframe(df)
add_team_colors_to_dataframe(df)
add_location_and_is_private_to_dataframe(df)
if TOURNAMENT_RANKINGS_AVAILABLE:
    add_tournament_rankings_to_dataframe_from_csv(df, None)

df.to_pickle("saved_static_data/school_data_dataframe.pkl")
df.to_json("saved_static_data/school_data_dataframe.json", orient="records")
