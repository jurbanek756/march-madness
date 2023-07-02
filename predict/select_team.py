"""
Module for making predictions
"""

import random

from weight.lptr import lptr
from weight.sigmodal import sigmodal


def random_selection(team_a, team_b, **kwargs):
    """
    Randomly selects a team

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Team
    """
    return random.choice([team_a, team_b])


def weighted_random_selection_lptr(team_a, team_b, **kwargs):
    return random.choices(
        population=[team_a, team_b],
        k=1,
        weights=lptr(team_a, team_b, ap_rank_weight=kwargs.get("ap_rank_weight", 0.75)),
    )[0]


def weighted_random_selection_sigmodal(team_a, team_b, **kwargs):
    return random.choices(
        population=[team_a, team_b],
        k=1,
        weights=sigmodal(
            team_a,
            team_b,
            ap_rank_weight=kwargs.get("ap_rank_weight", 0.75),
            k=kwargs.get("k", 0.33),
        ),
    )[0]


def ranked_selection(team_a, team_b, **kwargs):
    """
    Selects the team with the highest rank in the tournament. If ranks are the same,
    use AP Ranking. If both teams are unranked by the AP, select randomly.

    Avoiding calling ap_selection to prevent a circular use case

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Teamm_
    """
    if team_a.tournament_rank < team_b.tournament_rank:
        return team_a
    elif team_b.tournament_rank < team_a.tournament_rank:
        return team_b
    else:
        if team_a.ap_rank and team_b.ap_rank:
            if team_a.ap_rank < team_b.ap_rank:
                return team_a
            else:
                return team_b
        else:
            return random_selection(team_a, team_b)


def ap_selection(team_a, team_b, **kwargs):
    """
    Selects the team with the highest AP rank in the tournament. If both teams are
    unranked by the AP, use the tournament ranking. If tournament ranks are the same,
    select randomly.

    Avoiding calling ranked_selection to prevent a circular use case

    Parameters
    ----------
    team_a: Team
    team_b: Team
    kwargs: dict
        Unused


    Returns
    -------
    Team
    """
    if team_a.ap_rank and team_b.ap_rank:
        if team_a.ap_rank < team_b.ap_rank:
            return team_a
        else:
            return team_b
    else:
        if team_a.tournament_rank < team_b.tournament_rank:
            return team_a
        elif team_b.tournament_rank < team_a.tournament_rank:
            return team_b
        else:
            return random_selection(team_a, team_b)
