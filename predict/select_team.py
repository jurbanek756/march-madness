"""
Module for making predictions
"""

import random
from weight.lptr import lptr as weight_function

# from weight.sigmodal import sigmodal as weight_function


def random_selection(a, b, **kwargs):
    """
    Randomly selects a team

    Parameters
    ----------
    a: Team
    b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Team
    """
    return random.choice([a, b])


def weighted_random_selection(a, b, weight_function=weight_function, **kwargs):
    return random.choices(
        population=[a, b],
        k=1,
        weights=weight_function(a, b),
    )[0]


def ranked_selection(a, b, **kwargs):
    """
    Selects the team with the highest rank in the tournament. If ranks are the same,
    use AP Ranking. If both teams are unranked by the AP, select randomly.

    Avoiding calling ap_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Team
    """
    if a.tournament_rank > b.tournament_rank:
        return b
    elif b.tournament_rank > a.tournament_rank:
        return a
    else:
        if a.ap_rank and b.ap_rank:
            if a.ap_rank > b.ap_rank:
                return a
            else:
                return b
        else:
            return random_selection(a, b)


def ap_selection(a, b, **kwargs):
    """
    Selects the team with the highest AP rank in the tournament. If both teams are
    unranked by the AP, use the tournament ranking. If tournament ranks are the same,
    select randomly.

    Avoiding calling ranked_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team
    kwargs: dict
        Unused

    Returns
    -------
    Team
    """
    if a.ap_rank and b.ap_rank:
        if a.ap_rank > b.ap_rank:
            return a
        else:
            return b
    else:
        if a.tournament_rank > b.tournament_rank:
            return a
        else:
            return b
