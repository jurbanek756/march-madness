#!/usr/bin/env python

import pandas as pd

from predict.select_team import weighted_random_selection
from team.dataframe import (
    add_tournament_rankings_to_dataframe_from_csv,
    filter_none_values,
    add_data_to_dataframe,
)
from team.team import Team
from test.data.rankings_2022 import west, east, south, midwest


def generate_full_region_dict(all_schools_df, region):
    tuple_list = list()
    for k, v in region.items():
        tuple_list.append((v, k))
    region_df = add_data_to_dataframe(all_schools_df, tuple_list, "Tournament Ranking")
    region_df = filter_none_values(region_df, "Tournament Ranking")
    region_teams = [Team(record) for record in region_df.to_dict(orient="records")]
    data = dict()
    for team in region_teams:
        data[team.tournament_rank] = team
    return data


df = pd.read_pickle("saved_static_data/school_data_dataframe.pkl")

west_play_in_rank = west.pop("play_in_rank")
west_teams = generate_full_region_dict(df, west)
print(west_teams)

east_play_in_rank = east.pop("play_in_rank")
east_teams = generate_full_region_dict(df, east)
print(east_teams)

south_play_in_rank = south.pop("play_in_rank")
south_teams = generate_full_region_dict(df, south)
print(south_teams)

midwest_play_in_rank = midwest.pop("play_in_rank")
midwest_teams = generate_full_region_dict(df, midwest)
print(midwest_teams)
