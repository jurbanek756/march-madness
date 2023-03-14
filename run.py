#!/usr/bin/env python

import json

from predict.select_team import weighted_random_selection

from team.team import Team
from rankings.r2022 import west, east, south, midwest
from tournament.tournament import Tournament


def generate_full_region_dict(db, region):
    region_teams = list()
    for rank, name in region.items():
        try:
            record = next(filter(lambda x: x["Name"] == name, db))
        except StopIteration:
            raise RuntimeError(f"Failed at {name}")
        region_teams.append(Team(record, rank))
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

with open("db/school_data.json") as F:
    db = json.load(F)

west_play_in_rank = west.pop("play_in_rank")
west_teams = generate_full_region_dict(db, west)

east_play_in_rank = east.pop("play_in_rank")
east_teams = generate_full_region_dict(db, east)

south_play_in_rank = south.pop("play_in_rank")
south_teams = generate_full_region_dict(db, south)

midwest_play_in_rank = midwest.pop("play_in_rank")
midwest_teams = generate_full_region_dict(db, midwest)

tournament = Tournament(
    south_teams,
    east_teams,
    midwest_teams,
    west_teams,
    south_play_in_rank,
    east_play_in_rank,
    midwest_play_in_rank,
    west_play_in_rank,
    prediction_method=weighted_random_selection,
    log_results=True,
)


tournament.run()
