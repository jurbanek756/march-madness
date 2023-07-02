import pytest
from models.team import Team
from predict.sentiment_analysis import nickname_sentiment


@pytest.fixture
def duke():
    record = {
        "Name": "Duke",
        "Nickname": "Blue Devils",
        "Location": "Durham, NC",
        "Primary Color": "Blue",
        "Secondary Color": "White",
        "Conference": "ACC",
        "Is Private": True,
        "AP Ranking": 1,
        "Rivals": ["UNC", "Kentucky"],
    }
    return Team(record, 1, [])


@pytest.fixture
def unc():
    record = {
        "Name": "UNC",
        "Nickname": "Tar Heels",
        "Location": "Chapel Hill, NC",
        "Primary Color": "Blue",
        "Secondary Color": "White",
        "Conference": "ACC",
        "Is Private": False,
        "AP Ranking": 5,
        "Rivals": ["Duke", "NC State"],
    }
    return Team(record, 5, [])


@pytest.fixture
def nc_state():
    record = {
        "Name": "NC State",
        "Nickname": "Wolfpack",
        "Location": "Raleigh, NC",
        "Primary Color": "Red",
        "Secondary Color": "White",
        "Conference": "ACC",
        "Is Private": False,
        "AP Ranking": None,
        "Rivals": ["UNC", "Wake Forest"],
    }
    return Team(record, 7, [])


@pytest.fixture
def wake_forest():
    record = {
        "Name": "Wake Forest",
        "Nickname": "Demon Deacons",
        "Location": "Winston-Salem, NC",
        "Primary Color": "Black",
        "Secondary Color": "Gold",
        "Conference": "ACC",
        "Is Private": True,
        "AP Ranking": None,
        "Rivals": ["NC State", "Duke"],
    }
    return Team(record, 16, [])


@pytest.fixture
def virginia():
    record = {
        "Name": "Virginia",
        "Nickname": "Cavaliers",
        "Location": "Charlottesville, VA",
        "Primary Color": "Orange",
        "Secondary Color": "Blue",
        "Conference": "ACC",
        "Is Private": False,
        "AP Ranking": 15,
        "Rivals": ["Virginia Tech"],
    }
    return Team(record, 1, [])


def test_nickname_sentiment(duke, unc, nc_state, wake_forest, virginia):
    # Scores:
    #   Duke: 0.80
    #   UNC:  0.81
    #   NC State: 0.91
    #   Wake Forest: -0.65
    #   Virginia: 0.76
    assert nickname_sentiment(duke, unc) == unc
    assert nickname_sentiment(duke, nc_state) == nc_state
    assert nickname_sentiment(duke, wake_forest) == duke
    assert nickname_sentiment(duke, virginia) == duke
    assert nickname_sentiment(unc, nc_state) == nc_state
    assert nickname_sentiment(unc, wake_forest) == unc
    assert nickname_sentiment(unc, virginia) == unc
    assert nickname_sentiment(nc_state, wake_forest) == nc_state
    assert nickname_sentiment(nc_state, virginia) == nc_state
    assert nickname_sentiment(wake_forest, virginia) == virginia
