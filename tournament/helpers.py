from models.team import Team


def generate_full_region_dict(db, regular_season_games, region):
    region_teams = list()
    for rank, name in region.items():
        try:
            record = next(filter(lambda x: x["Name"] == name, db))
        except StopIteration:
            raise RuntimeError(f"Failed at {name}")
        if name not in regular_season_games:
            print(f"Games not found for {name}")
            games = None
        else:
            games = regular_season_games[name]
        region_teams.append(Team(record, rank, games))
    data = dict()
    for t in region_teams:
        data[t.tournament_rank] = t
    return data
