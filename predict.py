#!/usr/bin/env python

import pandas as pd

from team.dataframe import (
    add_tournament_rankings_to_dataframe_from_csv,
    filter_none_values,
)
from team.team import Team

df = pd.read_pickle("saved_static_data/school_data_dataframe.pkl")
add_tournament_rankings_to_dataframe_from_csv(df, "test/data/elite8.csv")
df = filter_none_values(df, "Tournament Ranking")

teams = [Team(record) for record in df.to_dict(orient="records")]
