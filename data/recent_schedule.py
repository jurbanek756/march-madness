from bs4 import BeautifulSoup
from requests_ratelimiter import LimiterSession
from data.espn import get_teams_from_api

session = LimiterSession(per_second=3)


def get_recent_performance(game_limit=None):
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
        if game_limit:
            rows = rows[-game_limit:]
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
                breakpoint()
                raise ValueError("Invalid win-loss character detected")
            team_games.append(
                {
                    "date": game_date,
                    "opponent": opponent,
                    "score": score[1:],
                    "win": win,
                }
            )
        games[team["shortDisplayName"]] = team_games
    return games
