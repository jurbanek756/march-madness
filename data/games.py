from bs4 import BeautifulSoup
from requests_ratelimiter import LimiterSession
from data.espn import get_teams_from_api
from game.game import Game

session = LimiterSession(per_second=3)


def get_regular_season_games():
    teams = get_teams_from_api()
    games = dict()
    for team in teams:
        team_games = list()
        schedule_link = next(filter(lambda x: x["text"] == "Schedule", team["links"]))[
            "href"
        ]
        schedule_soup = BeautifulSoup(
            session.get(schedule_link).text, features="html.parser"
        )
        schedule_table = schedule_soup.find("tbody", {"class", "Table__TBODY"})
        rows = [r for r in schedule_table.find_all("tr", {"class": "Table__TR"})]
        regular_season_index = [
            idx for idx, s in enumerate(rows) if s.text == "Regular Season"
        ][0]
        rows = rows[regular_season_index + 2 :]
        for row in rows:
            row = [r for r in row]
            game_date = row[0].text.strip()
            opponent = row[1].text.replace("vs ", "").strip()
            score = row[2].text.strip()
            if score[0] == "W":
                win = True
                score = score[1:]
            elif score[0] == "L":
                win = False
                score = score[1:]
            elif score == "Canceled":
                win = None
            elif score == "Postponed":
                win = None
            else:
                raise ValueError("Invalid win-loss character detected")
            team_games.append(
                Game(game_date=game_date, opponent=opponent, score=score, win=win)
            )
        name = team["shortDisplayName"]
        if name[-3:] == " St":
            name = name.replace(" St", "State")
        elif name in ESPN_NAMES:
            name = ESPN_NAMES[name]
        games[name] = team_games
    return games


ESPN_NAMES = {
    "Saint Mary's": "St. Mary's"
}