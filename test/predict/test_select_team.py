import pytest
from models.team import Team
from predict.select_team import (
    ranked_selection,
    ap_selection,
    random_selection,
    weighted_random_selection_lptr,
    weighted_random_selection_sigmodal,
)


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


def test_random_selection(duke, unc):
    assert random_selection(duke, unc) in [duke, unc]


def test_weighted_random_selection_lptr(duke, wake_forest):
    # Duke is ranked 1, Wake Forest is ranked 16, so Duke will always be selected
    assert weighted_random_selection_lptr(duke, wake_forest) == duke


def test_weighted_random_selection_sigmodal(duke, wake_forest):
    # Duke is ranked 1, Wake Forest is ranked 16, so Duke will always be selected
    assert weighted_random_selection_sigmodal(duke, wake_forest) == duke


def test_ranked_selection(duke, unc, nc_state, wake_forest, virginia):
    # Duke is ranked 1 and no other team is ranked 1, so Duke will always be selected
    assert ranked_selection(duke, unc) == duke
    assert ranked_selection(duke, nc_state) == duke
    assert ranked_selection(duke, wake_forest) == duke
    # Virginia is ranked 1, but Duke has a higher AP ranking, so Duke will be selected
    assert ranked_selection(duke, virginia) == duke
    # All other selections are based solely on tournament ranking
    assert ranked_selection(unc, nc_state) == unc
    assert ranked_selection(unc, wake_forest) == unc
    assert ranked_selection(nc_state, wake_forest) == nc_state


def test_ap_selection(duke, unc, nc_state, wake_forest, virginia):
    # Duke has a higher AP ranking, so Duke will always be selected
    assert ap_selection(duke, unc) == duke
    assert ap_selection(duke, nc_state) == duke
    assert ap_selection(duke, wake_forest) == duke
    assert ap_selection(duke, virginia) == duke
    # All other selections are based solely on AP Ranking. UNC is 5, Virginia 15, and
    #    all others are None which defers back to tournament ranking
    assert ap_selection(unc, nc_state) == unc
    assert ap_selection(unc, wake_forest) == unc
    assert ap_selection(unc, virginia) == unc
    assert ap_selection(virginia, nc_state) == virginia
    assert ap_selection(virginia, wake_forest) == virginia
    assert ap_selection(nc_state, wake_forest) == nc_state
