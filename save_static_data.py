#!/usr/bin/env python3

from team.dataframe import get_all_d1_schools, add_ap_rankings_to_dataframe, add_team_colors_to_dataframe

df = get_all_d1_schools()
add_ap_rankings_to_dataframe(df)
add_team_colors_to_dataframe(df)
df.to_pickle("saved_static_data/school_data_dataframe.pkl")
df.to_json("saved_static_data/school_data_dataframe.json")

