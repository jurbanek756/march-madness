"""
Sigmodal Ranking Probabilities
------------------------------

Generates the probability of each team winning as a ratio of 1. Uses a sigmodal
function based on the difference in rank between the two teams. Ex.
1 vs 1 = 0.5, 0.5
1 vs 16 = 0.9375, 0.0625

The probabilities gradually transition from low to high values as the ranking
difference increases, favoring highly ranked teams more than lptr.

The sigmoidal curve exhibits a rounded shape, resulting in a more gradual change in
probabilities for smaller ranking differences and a steeper change for larger
differences. In this way, it favors highly ranked teams more than lptr. The curve
ensures that the probabilities are bounded between 0 and 1.

Two implementations are provided, a default sigma function and a k-sigma function.
The k-sigma function accepts a scaling factor k while ensuring that the team with the
higher ranking always has a higher probability of winning.

As k increases, the curve becomes steeper, resulting in a more rapid change in
probabilities for smaller ranking, essentially becoming a step function. As k
decreases, the curve becomes more rounded, resulting in a more gradual probability
change for smaller ranking differences. A value of k~=0.17 functions nearly
identically to lptr.

By default, k=0.33 is used, which closely emulates the behavior of the original
sigmodal function, but with the ability to give the 8 seed in an 8-9 matchup a
higher probability as opposed to 0.5.
"""

import math


def sigmodal(team1, team2, use_ap_ranks=True, k=None):
    """
    Main function for sigmodal ranking probabilities.

    Parameters
    ----------
    team1: Team
    team2: Team
    use_ap_ranks: bool
    k: float

    Returns
    -------
    tuple
        Team 1 probability, Team 2 probability
    """
    if use_ap_ranks:
        if k:
            return sigmodal_k_with_ap(
                team1.tournament_rank,
                team2.tournament_rank,
                team1.ap_rank,
                team2.ap_rank,
                k=k,
            )
        else:
            return sigmodal_with_ap(
                team1.tournament_rank,
                team2.tournament_rank,
                team1.ap_rank,
                team2.ap_rank,
            )
    else:
        if k:
            return sigmodal_k_tournament_only(
                team1.tournament_rank, team2.tournament_rank, k=k
            )
        else:
            return sigmodal_tournament_only(
                team1.tournament_rank, team2.tournament_rank
            )


def sigmodal_tournament_only(rank1, rank2):
    """
    Sigmodal ranking probabilities that only considers tournament rankings.

    Notes
    -----
    For 8 v. 9 matchups, the probability of each team winning is 0.5. Because this is
    used for an entropic prediction, this is acceptable, and in some ways preferred, but
    can be avoided by using the sigmoid_k function with the default value of k, which
    essentially acts as an improved version of this function.

    Resources:
    ----------
    * https://chat.openai.com/share/875338f1-ca29-4637-a9a6-4722d29dfd75

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
    if diff == 15:
        if rank1 < rank2:
            return 1, 0
        else:
            return 0, 1
    elif diff == 0:
        return 0.5, 0.5
    y = abs(diff) / (1 + abs(diff))
    if rank1 < rank2:
        return y, 1 - y
    else:
        return 1 - y, y


def sigmodal_with_ap(
    tourn_rank_1, tourn_rank_2, ap_rank_1, ap_rank_2, tourn_weight=0.75
):
    if tourn_rank_1 > 16 or tourn_rank_2 > 16:
        raise ValueError("Invalid tournament ranking provided")
    if not ap_rank_1:
        ap_rank_1 = 26
    if not ap_rank_2:
        ap_rank_2 = 26
    if ap_rank_1 > 26 or ap_rank_2 > 26:
        raise ValueError("Invalid AP ranking provided")
    if tourn_weight > 1 or tourn_weight < 0:
        raise ValueError("Invalid tournament weight provided")
    ap_weight = 1 - tourn_weight
    tourn_diff = abs(tourn_rank_1 - tourn_rank_2)
    if tourn_diff == 15:
        if tourn_rank_1 < tourn_rank_2:
            return 1, 0
        else:
            return 0, 1
    tourn_y = abs(tourn_diff) / (1 + abs(tourn_diff))
    ap_diff = abs(ap_rank_1 - ap_rank_2)
    ap_y = abs(ap_diff) / (1 + abs(ap_diff))
    y = (tourn_weight * tourn_y) + (ap_weight * ap_y)
    if tourn_rank_1 < tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return y, 1 - y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 > ap_rank_2:
        return 1 - y, y
    elif tourn_rank_1 < tourn_rank_2 and ap_rank_1 > ap_rank_2:
        return y, 1 - y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return 1 - y, y
    else:
        return 0.5, 0.5


def sigmodal_k_tournament_only(rank1, rank2, k=0.33):
    """
    Sigmodal-k ranking probabilities that only considers tournament rankings.

    Parameters:
    -----------
    rank1 : int
        The ranking of the first team.
    rank2 : int
        The ranking of the second team.
    k : float, optional
        The scaling factor controlling the steepness of the sigmoidal curve.
        Default is 1.

    Resources:
    ----------
    * https://chat.openai.com/share/875338f1-ca29-4637-a9a6-4722d29dfd75

    Returns:
    --------
    tuple
    """
    diff = abs(rank1 - rank2)
    if diff == 15:
        if rank1 < rank2:
            return 1, 0
        else:
            return 0, 1
    elif diff == 0:
        return 0.5, 0.5
    y = 1 / (1 + math.exp(-k * diff))
    if rank1 < rank2:
        return y, 1 - y
    else:
        return 1 - y, y


def sigmodal_k_with_ap(
    tourn_rank_1, tourn_rank_2, ap_rank_1, ap_rank_2, k=0.33, tourn_weight=0.75
):
    if tourn_rank_1 > 16 or tourn_rank_2 > 16:
        raise ValueError("Invalid tournament ranking provided")
    if not ap_rank_1:
        ap_rank_1 = 26
    if not ap_rank_2:
        ap_rank_2 = 26
    if ap_rank_1 > 26 or ap_rank_2 > 26:
        raise ValueError("Invalid AP ranking provided")
    if tourn_weight > 1 or tourn_weight < 0:
        raise ValueError("Invalid tournament weight provided")
    ap_weight = 1 - tourn_weight
    tourn_diff = abs(tourn_rank_1 - tourn_rank_2)
    if tourn_diff == 15:
        if tourn_rank_1 < tourn_rank_2:
            return 1, 0
        else:
            return 0, 1
    tourn_y = 1 / (1 + math.exp(-k * tourn_diff))
    ap_diff = abs(ap_rank_1 - ap_rank_2)
    ap_y = 1 / (1 + math.exp(-k * ap_diff))
    y = (tourn_weight * tourn_y) + (ap_weight * ap_y)
    if tourn_rank_1 < tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return y, 1 - y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 > ap_rank_2:
        return 1 - y, y
    elif tourn_rank_1 < tourn_rank_2 and ap_rank_1 > ap_rank_2:
        return y, 1 - y
    elif tourn_rank_1 > tourn_rank_2 and ap_rank_1 < ap_rank_2:
        return 1 - y, y
    else:
        return 0.5, 0.5
