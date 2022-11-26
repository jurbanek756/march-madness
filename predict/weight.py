#!/usr/bin/env python3


def lptr(rank1, rank2):
    """
    Linearly Proportional Tournament Ranking
    ----------------------------------------
    Generates probability of each team winning as a ratio of 1. Uses a linear proportional function based on the
    difference in rank between the two teams. Ex.
    1 vs 1 = 0.5, 0.5
    1 vs 16 = 1, 0

    Parameters
    ----------
    rank1: int
    rank2: int

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    diff = abs(rank1 - rank2)
    y = (0.5 / 15) * diff + 0.5
    if rank1 < rank2:
        return y, 1 - y
    else:
        return 1 - y, y
