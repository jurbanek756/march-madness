from functools import lru_cache
import requests


@lru_cache
def get_teams_from_api():
    url = (
        "https://site.api.espn.com/apis/site/v2/sports/basketball/"
        "mens-college-basketball/teams?limit=500"
    )
    response = requests.get(url)
    data = response.json()
    teams = data["sports"][0]["leagues"][0]["teams"]
    return [t["team"] for t in teams]
