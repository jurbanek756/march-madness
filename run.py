#!/usr/bin/env python

import pandas as pd

from predict.select_team import weighted_random_selection
from team.dataframe import (
    filter_none_values,
    add_data_to_dataframe,
)
from team.team import Team
from test.data.rankings_2022 import west, east, south, midwest
from tournament.tournament import Tournament


def generate_full_region_dict(all_schools_df, region):
    tuple_list = list()
    for k, v in region.items():
        tuple_list.append((v, k))
    region_df = add_data_to_dataframe(all_schools_df, tuple_list, "Tournament Ranking")
    region_df = filter_none_values(region_df, "Tournament Ranking")
    region_teams = [Team(record) for record in region_df.to_dict(orient="records")]
    data = dict()
    for t in region_teams:
        data[t.tournament_rank] = t
    return data


all_teams = set()
for region in west, east, south, midwest:
    for k, team in region.items():
        if k != "play_in_rank":
            all_teams.add(team)

if len(all_teams) != 68:
    print(len(all_teams))
    raise ValueError("Duplicate team found in source dict")


df = pd.read_pickle("saved_static_data/school_data_dataframe.pkl")

west_play_in_rank = west.pop("play_in_rank")
west_teams = generate_full_region_dict(df, west)

east_play_in_rank = east.pop("play_in_rank")
east_teams = generate_full_region_dict(df, east)

south_play_in_rank = south.pop("play_in_rank")
south_teams = generate_full_region_dict(df, south)

midwest_play_in_rank = midwest.pop("play_in_rank")
midwest_teams = generate_full_region_dict(df, midwest)

tournament_2022 = Tournament(
    west_teams,
    east_teams,
    south_teams,
    midwest_teams,
    west_play_in_rank,
    east_play_in_rank,
    south_play_in_rank,
    midwest_play_in_rank,
    prediction_method=weighted_random_selection,
    log_results=True,
)

tournament_2022.run()
