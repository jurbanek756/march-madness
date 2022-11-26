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

north = [[teams[0], teams[1]]]
south = [[teams[2], teams[3]]]
east = [[teams[4], teams[5]]]
west = [[teams[6], teams[7]]]


print(f"{north[0][0]} vs {north[0][1]} prediction:", end=" ")
north = weighted_random_selection(north[0][0], north[0][1])
print(north)

print(f"{south[0][0]} vs {south[0][1]} prediction:", end=" ")
south = weighted_random_selection(south[0][0], south[0][1])
print(south)

print(f"{east[0][0]} vs {east[0][1]} prediction:", end=" ")
east = weighted_random_selection(east[0][0], east[0][1])
print(east)

print(f"{west[0][0]} vs {west[0][1]} prediction:", end=" ")
west = weighted_random_selection(west[0][0], west[0][1])
print(west)
