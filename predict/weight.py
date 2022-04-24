#!/usr/bin/env python3


def lptr(team1, team2):
    """
    Linearly Proportional Tournament Ranking
    ----------------------------------------
    Generates probability of each team winning as a ratio of 1. Uses a linear proportional function based on the
    difference in rank between the two teams. Ex.
    1 vs 1 = 0.5, 0.5
    1 vs 16 = 1, 0

    Parameters
    ----------
    team1: Team
    team2: Team

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    diff = abs(team1.rank - team2.rank)
    y = (0.5 / 15) * diff + 0.5
    if team1.rank < team2.rank:
        return y, 1 - y
    else:
        return 1 - y, y
