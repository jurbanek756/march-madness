from functools import lru_cache


@lru_cache
def get_teams_from_api(session, limit=500):
    url = (
        "https://site.api.espn.com/apis/site/v2/sports/basketball/"
        f"mens-college-basketball/teams?limit={limit}"
    )
    response = session.get(url)
    data = response.json()
    teams = data["sports"][0]["leagues"][0]["teams"]
    return [t["team"] for t in teams]


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
    "N Kentucky": "Northern Kentucky",
}
