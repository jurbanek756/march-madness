from bs4 import BeautifulSoup
import requests
from data.espn import get_teams_from_api


def get_recent_performance(game_limit=None):
    teams = get_teams_from_api()
    games = list()
    for team in teams:
        team_games = list()
        schedule_link = next(filter(lambda x: x["text"] == "Schedule", team["links"]))["href"]
        schedule_soup = BeautifulSoup(requests.get(schedule_link).text, features="html.parser")
        schedule_table = schedule_soup.find("tbody", {"class", "Table__TBODY"})
        rows = [r for r in schedule_table.find_all("tr", {"class": "Table__TR"})][2:]
        if game_limit:
            rows = rows[-game_limit:]
        for row in rows:
            game_date = row[0].text.strip()
            opponent = row[1].text.replace("vs ", "").strip()
            score = row[2].text.strip()
            if score[0] == "W":
                win = True
            elif score[0] == "L":
                win = False
            else:
                raise ValueError("Invalid win-loss character detected")
            team_games.append({
                "date": game_date,
                "opponent": opponent,
                "score": score[1:],
                "win": win
            })
        games.append(team_games)
    return games
