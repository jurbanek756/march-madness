"""
Linearly Proportional Tournament Ranking
----------------------------------------

Generates probability of each team winning as a ratio of 1. Uses a linear
proportional function based on the difference in rank between the two teams. Ex.
1 vs 1 = 0.5, 0.5
1 vs 16 = 1, 0

While easy to implement and understand, it does have significant drawbacks in that
it weighs all ranking differences the same. For example, a 1 vs. 3 seed will have
the same weight as a 14 vs. 16 seed.

If AP rankings are considered, Tournament rankings are weighted at .75, AP rankings
are weighted at .25.

Resources
---------
* https://chat.openai.com/c/d00ba596-f435-46fe-8e96-721df48078fa
"""

import os
import sys

sys.path.append("mmsite/")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mmsite.settings")
import django

django.setup()

from marchmadness.models import APRanking


def lptr(team1, team2, ap_rank_weight=0.75):
    """
    Main function for linearly proportional tournament ranking.

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    if ap_rank_weight == 0:
        return lptr_tournament_only(team1.ranking, team2.ranking)
    else:
        ap_rank_1 = APRanking.objects.filter(school_name=team1.school_name)
        if ap_rank_1:
            ap_rank_1 = ap_rank_1.first().ranking
        ap_rank_2 = APRanking.objects.filter(school_name=team1.school_name)
        if ap_rank_2:
            ap_rank_2 = ap_rank_2.first().ranking
        return lptr_with_ap(
            team1.ranking, team2.ranking, ap_rank_1, ap_rank_2, ap_rank_weight
        )


def lptr_tournament_only(rank1: int, rank2: int):
    """
    LPTR that only considers tournament rankings.

    Parameters
    ----------
    rank1: int
    rank2: int

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    if rank1 > 16 or rank2 > 16:
        raise ValueError("Invalid tournament ranking provided")
    diff = abs(rank1 - rank2)
    y = (0.5 / 15) * diff + 0.5
    if rank1 < rank2:
        return y, 1 - y
    else:
        return 1 - y, y


def lptr_with_ap(tourn_rank_1, tourn_rank_2, ap_rank_1, ap_rank_2, ap_weight=0.75):
    """
    LPTR that considers both tournament and AP rankings.

    Notes
    -----
    - If a team is unranked by the AP, it is given a rank of 26.
    - If neither team is ranked by the AP, lptr_tournament_only is used

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    if not ap_rank_1 and not ap_rank_2:
        return lptr_tournament_only(tourn_rank_1, tourn_rank_2)
    if tourn_rank_1 > 16 or tourn_rank_2 > 16:
        raise ValueError("Invalid tournament ranking provided")
    if not ap_rank_1:
        ap_rank_1 = 26
    if not ap_rank_2:
        ap_rank_2 = 26
    if ap_rank_1 > 26 or ap_rank_2 > 26:
        raise ValueError("Invalid AP ranking provided")
    if ap_weight > 1 or ap_weight < 0:
        raise ValueError("Invalid AP weight provided")
    tourn_weight = 1 - ap_weight
    tourn_diff = abs(tourn_rank_1 - tourn_rank_2)
    y_tourn = (0.5 / 15) * tourn_diff + 0.5
    ap_diff = abs(ap_rank_1 - ap_rank_2)
    y_ap = (0.5 / 25) * ap_diff + 0.5
    y = tourn_weight * y_tourn + ap_weight * y_ap
    if tourn_rank_1 < tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return y, 1 - y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 > ap_rank_2:
        return 1 - y, y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return 1 - y, y
    else:
        return 0.5, 0.5
