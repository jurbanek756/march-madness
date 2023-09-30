import logging

from bs4 import BeautifulSoup
from requests_ratelimiter import LimiterSession
from tqdm import tqdm

from data.espn import get_teams_from_api, get_name
from models.game import Game

session = LimiterSession(per_second=1)
session.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) "
        "Gecko/20100101 Firefox/115.0"
    }
)

logger = logging.getLogger(__name__)


def get_regular_season_games(season_year=2023):
    teams = get_teams_from_api(session)
    games = dict()
    for team in tqdm(teams):
        team_name = get_name(team["shortDisplayName"])
        logger.info("Parsing games data for %s", team_name)
        team_games = list()
        schedule_link = next(filter(lambda x: x["text"] == "Schedule", team["links"]))[
            "href"
        ]
        link_with_year = f"{schedule_link}/season/{season_year}"
        schedule_soup = BeautifulSoup(
            session.get(link_with_year).text, features="html.parser"
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
            elif "T" in score:
                win = None
            else:
                raise ValueError("Invalid win-loss character detected: %s", score[0])
            team_games.append(
                Game(
                    game_date=game_date,
                    opponent=get_name(opponent),
                    score=score,
                    win=win,
                ).to_dict()
            )
        games[team_name] = team_games
    return games
