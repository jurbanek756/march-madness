"""
Team class
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
        self.rivalries = record["Rivals"]
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
        r = f"{self.name}\n"
        r += f"Tournament Rank: {self.tournament_rank}\n"
        r += f"AP Rank: {self.ap_rank}\n"
        r += f"Conference: {self.conference}"
        r += f"Record: {self.record}\n"
        r += f"Recent Record: {self.recent_record(10)}"
        return r

    @property
    def game_results(self):
        results = []
        for game in self.games:
            result = "Win" if game["win"] else "Loss"
            results.append(f"{result} {game['score']} vs. {game['opponent']}")
        return results

    def other_info(self):
        r = f"Nickname: {self.nickname}\n"
        r += f"Location: {self.location}\n"
        r += f"Colors: {self.primary_color}, {self.secondary_color}\n"
        is_private_str = "yes" if self.is_private else "no / status unknown"
        r += f"Private: {is_private_str}\n"
        return r

    def __str__(self):
        return self.name

    def __le__(self, other):
        return self.tournament_rank <= other.tournament_rank
