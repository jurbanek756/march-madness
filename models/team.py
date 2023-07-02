"""
Team class. Contains the following attributes:
    name: School shortname, ex. Kansas, UCLA
    nickname: School nickname, ex. Jayhawks, Bruins
    location: School location, ex. Lawrence, Los Angeles
    primary_color: School primary color, ex. blue
    secondary_color: School secondary color, ex. red
    conference: School conference, ex. Big 12, Pac-12
    is_private: Whether or not the school is private
    tournament_rank: The school's seed in the tournament
    ap_rank: The school's AP ranking, None if not ranked
    rivalries: List of school's rivalries
    games: List of school's games
    record: The school's regular season record
    recent_record: The school's record over the last n games
    game_results: The school's game results
    other_info: other school info
"""


class Team:
    __slots__ = (
        "name",
        "nickname",
        "location",
        "primary_color",
        "secondary_color",
        "conference",
        "is_private",
        "tournament_rank",
        "ap_rank",
        "rivalries",
        "games",
    )

    def __init__(self, record, tournament_ranking, games):
        self.name = record["Name"]
        self.nickname = record["Nickname"]
        self.location = record["Location"]
        self.primary_color = record["Primary Color"]
        self.secondary_color = record["Secondary Color"]
        self.conference = record["Conference"]
        self.is_private = record["Is Private"]
        self.tournament_rank = tournament_ranking
        self.ap_rank = record.get("AP Ranking")
        self.rivalries = record["Rivals"] if isinstance(record["Rivals"], list) else []
        self.games = games

    @property
    def record(self):
        total_games = len(self.games)
        wins = len(list(filter(lambda x: x["win"], self.games)))
        losses = total_games - wins
        return f"{wins}-{losses}"

    def recent_record(self, n):
        games = self.games[-n:]
        wins = len(list(filter(lambda x: x["win"], games)))
        losses = n - wins
        return f"{wins}-{losses}"

    @property
    def tournament_repr(self):
        r = list()
        r.append(f"{self.tournament_rank}. {self.name}")
        if self.ap_rank:
            r.append(f"AP Rank: {self.ap_rank}")
        r.append(f"Conference: {self.conference}")
        r.append(f"Record: {self.record}  ({self.recent_record(10)} in last 10 games)")
        return r

    @property
    def game_results(self):
        results = []
        for game in self.games:
            result = "Win" if game["win"] else "Loss"
            results.append(f"{result} {game['score']} vs. {game['opponent']}")
        return results

    @property
    def other_info(self):
        r = list()
        r.append(f"Nickname: {self.nickname}")
        r.append(f"Location: {self.location}")
        r.append(f"Colors: {self.primary_color}, {self.secondary_color}")
        is_private_str = "yes" if self.is_private else "no"
        r.append(f"Private: {is_private_str}")
        return r

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
