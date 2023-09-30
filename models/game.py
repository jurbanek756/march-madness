class Game:
    __slots__ = ("date", "opponent", "score", "home_game", "win")

    def __init__(self, game_date, opponent, score, home_game, win):
        self.date = game_date
        self.opponent = opponent
        self.score = score
        self.home_game = home_game
        self.win = win

    def to_dict(self):
        return {
            "game_date": self.date,
            "opponent": self.opponent,
            "score": self.score,
            "home_game": self.home_game,
            "win": self.win,
        }
