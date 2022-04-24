#!/usr/bin/env python3

from predict.weight import lptr

import random


def random_selection(a, b):
    """
    Randomly selects a team

    Parameters
    ----------
    a: Team
    b: Team

    Returns
    -------
    Team
    """
    return random.choice([a, b])


def weighted_random_selection(a, b, weight_function=lptr):
    """

    Parameters
    ----------
    a: Team
    b: Team
    weight_function: function
        Function used to weight teams

    Returns
    -------
    Team
    """
    return random.choices(population=[a, b], k=1, weights=weight_function(a, b))


def ranked_selection(a, b):
    """
    Selects the team with the highest rank in the tournament. If ranks are the same, use AP Ranking. If both teams are
    unranked by the AP, select randomly.

    Avoiding calling ap_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team

    Returns
    -------
    Team
    """
    if a.rank > b.rank:
        return b
    elif b.rank > a.rank:
        return a
    else:
        if a.ap_rank > b.ap_rank:
            return a
        elif b.ap_rank > a.ap_rank:
            return b
        else:
            return random_selection(a, b)


def ap_selection(a, b):
    """
    Selects the team with the highest AP rank in the tournament. If both teams are unranked by the AP, use the
    tournament ranking. If tournament ranks are the same, select randomly.

    Avoiding calling ranked_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team

    Returns
    -------
    Team
    """
    if a.ap_rank > b.ap_rank:
        return a
    elif b.ap_rank > a.ap_rank:
        return b
    else:
        if a.rank > b.rank:
            return b
        elif b.rank > a.rank:
            return a
        else:
            return random_selection(a, b)
