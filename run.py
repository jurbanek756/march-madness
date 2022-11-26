#!/usr/bin/env python

import pandas as pd

from predict.select_team import weighted_random_selection
from team.dataframe import (
    add_tournament_rankings_to_dataframe_from_csv,
    filter_none_values,
)
from team.team import Team

df = pd.read_pickle("saved_static_data/school_data_dataframe.pkl")
add_tournament_rankings_to_dataframe_from_csv(df, "test/data/elite8.csv")
df = filter_none_values(df, "Tournament Ranking")

teams = [Team(record) for record in df.to_dict(orient="records")]

# Format is <conference>_<expected seeds in each game>, ex. east_116 will be the first and 16th seed playing in the
#   east conference, west_81 is the game in the western conference where the 8 and 1 seed are most likely to play
#   but could actually be the 9 and 1 seed
north_12 = [[teams[0], teams[1]]]
south_12 = [[teams[2], teams[3]]]
east_12 = [[teams[4], teams[5]]]
west_12 = [[teams[6], teams[7]]]


print(f"{north_12[0][0]} vs {north_12[0][1]} prediction:", end=" ")
north = weighted_random_selection(north_12[0][0], north_12[0][1])
print(north)

print(f"{south_12[0][0]} vs {south_12[0][1]} prediction:", end=" ")
south = weighted_random_selection(south_12[0][0], south_12[0][1])
print(south)

print(f"{east_12[0][0]} vs {east_12[0][1]} prediction:", end=" ")
east = weighted_random_selection(east_12[0][0], east_12[0][1])
print(east)

print(f"{west_12[0][0]} vs {west_12[0][1]} prediction:", end=" ")
west = weighted_random_selection(west_12[0][0], west_12[0][1])
print(west)

print(f"{north} vs {south} prediction:", end=" ")
ns = weighted_random_selection(north, south)
print(ns)

print(f"{east} vs {west} prediction:", end=" ")
ew = weighted_random_selection(east, west)
print(ew)

print(f"Championship Game between {ns} and {ew}")
champion = weighted_random_selection(ns, ew)
print(f"Champion: {champion}")
