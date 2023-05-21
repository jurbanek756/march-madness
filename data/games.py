import logging

from bs4 import BeautifulSoup
from requests_ratelimiter import LimiterSession
from tqdm import tqdm

from data.espn import get_teams_from_api
from models.game import Game

session = LimiterSession(per_second=3)
logger = logging.getLogger(__name__)

def get_regular_season_games():
    teams = get_teams_from_api()
    games = dict()
    for team in tqdm(teams):
        team_name = get_name(team["shortDisplayName"])
        logger.info("Parsing games data for %s", team_name)
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
            opponent = (
                row[1]
                .text.lstrip("0123456789")
                .replace("vs ", "")
                .replace("*", "")
                .replace("@", "")
                .strip()
            )
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
                raise ValueError("Invalid win-loss character detected: %s", score[0])
            team_games.append(
                Game(game_date=game_date, opponent=get_name(opponent), score=score, win=win).to_dict()
            )
        games[team_name] = team_games
    return games


def get_name(name):
    if name in ESPN_NAMES:
        return ESPN_NAMES[name]
    if name[-3:] == " St":
        name = f"{name[:-3]} State"
    if name[0:2] == "N ":
        name = f"North {name[2:]}"
    if name[0:2] == "S ":
        name = f"South {name[2:]}"
    if name[0:2] == "E ":
        name = f"East {name[2:]}"
    if name[0:2] == "W ":
        name = f"West {name[2:]}"
    if name[0:2] == "C ":
        name = f"Central {name[2:]}"
    if name[-5:] == " Univ":
        name = f"{name[:-5]} University"
    return name


ESPN_NAMES = {  # espn name: local name
    "Saint Mary's": "St. Mary's",
    "Fullerton": "CSUF",
    "New Mexico St": "NM State",
    "North Carolina": "UNC",
    "Colorado St": "CSU",
    "San Diego St": "SDSU",
    "S Dakota St": "South Dakota State",
    "Jacksonville": "Jacksonville State",
    "Texas A&M-CC": "AMCC",
    "Lafayette": "Louisiana-Lafayette",
    "Fair Dickinson": "Fairleigh Dickinson",
    "SE Missouri St": "Southeast Missouri State",
    "N Kentucky": "Northern Kentucky"
}
