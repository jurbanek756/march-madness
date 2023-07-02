"""
Module for making predictions
"""

import random
from transformers import pipeline

from weight.lptr import lptr as weight_function

# from weight.sigmodal import sigmodal as weight_function

SENTIMENT_CLASSIFIER = pipeline("sentiment-analysis")


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


def weighted_random_selection(
    team_a, team_b, weight_function=weight_function, **kwargs
):
    return random.choices(
        population=[team_a, team_b],
        k=1,
        weights=weight_function(team_a, team_b),
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


def nickname_sentiment(team_a, team_b, **kwargs):
    """
    Uses the huggingface library to compare the sentiment of each team's nickname.
    Returns the team with the higher positive sentiment for its nickname.

    Parameters
    ----------
    team_a: Team
    team_b: Team

    Returns
    -------
    Team
    """
    a_sentiment = SENTIMENT_CLASSIFIER(team_a.nickname)[0]
    b_sentiment = SENTIMENT_CLASSIFIER(team_b.nickname)[0]
    a_score = a_sentiment["score"] * (1 if a_sentiment["label"] == "POSITIVE" else -1)
    b_score = b_sentiment["score"] * (1 if b_sentiment["label"] == "POSITIVE" else -1)
    if a_score > b_score:
        return team_a
    else:
        return team_b
