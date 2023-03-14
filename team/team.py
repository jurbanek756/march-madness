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
    )

    def __init__(
        self,
        record,
            tournament_ranking
    ):
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

    def __str__(self):
        return self.name

    def __le__(self, other):
        return self.tournament_rank <= other.tournament_rank
