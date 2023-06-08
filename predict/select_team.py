"""
Module for making predictions
"""

import random
import sys

from helpers.print_helpers import print_in_two_columns
from predict.weight import lptr


def user_evaluation(a, b):
    print_in_two_columns(a.tournament_repr, b.tournament_repr, "Team 1", "Team 2")
    rivalry = False
    if a.rivalries:
        rivalry = b.name in a.rivalries
    if b.rivalries and not rivalry:
        rivalry = a.name in b.rivalries
    if rivalry:
        print("RIVALRY GAME")
    games_printed = False
    other_info_printed = False
    try:
        prompt = "Select 1, 2, m, or r (more info, random): "
        while True:
            choice = input(prompt)
            if choice == "1":
                return a
            elif choice == "2":
                return b
            elif choice == "r":
                return random_selection(a, b)
            elif choice == "m":
                if not games_printed:
                    print_in_two_columns(
                        a.game_results,
                        b.game_results,
                        f"{a.name} Games",
                        f"{b.name} Games",
                    )
                    games_printed = True
                elif not other_info_printed:
                    print_in_two_columns(
                        a.other_info,
                        b.other_info,
                        f"Additional {a.name} Info",
                        f"Additional {b.name} Info",
                    )
                    other_info_printed = True
                else:
                    print_in_two_columns(
                        a.tournament_repr, b.tournament_repr, "Team 1", "Team 2"
                    )
                    if rivalry:
                        print("RIVALRY GAME")
                    print_in_two_columns(
                        a.game_results,
                        b.game_results,
                        f"{a.name} Games",
                        f"{b.name} Games",
                    )
                    print_in_two_columns(
                        a.other_info,
                        b.other_info,
                        f"Additional {a.name} Info",
                        f"Additional {b.name} Info",
                    )
            elif choice == "q":
                confirm_quit = input("About to quit; are you sure? ")
                if "y" in confirm_quit or "q" in confirm_quit:
                    sys.exit()
                else:
                    print("Invalid choice selected; try again or select 'q' to exit")
            else:
                print("Invalid choice selected; try again or select 'q' to exit")
            if not other_info_printed:
                prompt = "Select 1, 2, m, or r (see even more info, random): "
            else:
                prompt = "All info displayed. Select 1, 2, or r (random): "
    except KeyboardInterrupt:
        sys.exit()


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


def consider_recent_games(a, b, games_dict):
    pass


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
    return random.choices(
        population=[a, b],
        k=1,
        weights=weight_function(a.tournament_rank, b.tournament_rank),
    )[0]


def ranked_selection(a, b):
    """
    Selects the team with the highest rank in the tournament. If ranks are the same,
    use AP Ranking. If both teams are unranked by the AP, select randomly.

    Avoiding calling ap_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team

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


def ap_selection(a, b):
    """
    Selects the team with the highest AP rank in the tournament. If both teams are
    unranked by the AP, use the tournament ranking. If tournament ranks are the same,
    select randomly.

    Avoiding calling ranked_selection to prevent a circular use case

    Parameters
    ----------
    a: Team
    b: Team

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
