import dateutil.parser
from dateutil.relativedelta import relativedelta

class Game:
    __slots__ = (
        "date",
        "opponent",
        "score",
        "win"
    )
    def __init__(self, game_date, opponent, score, win):
        self.date = dateutil.parser.parse(game_date).date()
        if self.date.month > 4:
            self.date -= relativedelta(years=1)
        self.opponent = opponent
        self.score = score
        self.win = win
