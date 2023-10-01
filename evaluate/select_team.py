import sys

from helpers.print_helpers import print_in_two_columns
from predict.select_team import random_selection


def user_evaluation(a, b, group_name=None, round_name=None, **kwargs):
    if group_name and round_name:
        print(f"{group_name} {round_name}")
    elif group_name:
        print(group_name)
    elif round_name:
        print(round_name)
    print_in_two_columns(a.tournament_repr, b.tournament_repr, "Team 1", "Team 2")
    # rivalry = False
    # if a.rivalries:
    #    rivalry = b.name in a.rivalries
    # if b.rivalries and not rivalry:
    #    rivalry = a.name in b.rivalries
    # if rivalry:
    #    print("RIVALRY GAME")
    games_printed = False
    school_info_printed = False
    try:
        prompt = "Select 1, 2, m, or r (more info, random): "
        while True:
            choice = input(prompt)
            if choice == "1":
                print()
                return a
            elif choice == "2":
                print()
                return b
            elif choice == "r":
                print()
                return random_selection(a, b)
            elif choice == "m":
                if not games_printed:
                    print_in_two_columns(
                        a.game_results,
                        b.game_results,
                        f"{a.school_name} Games",
                        f"{b.school_name} Games",
                    )
                    games_printed = True
                elif not school_info_printed:
                    print_in_two_columns(
                        a.school_info,
                        b.school_info,
                        f"Additional {a.school_name} Info",
                        f"Additional {b.school_name} Info",
                    )
                    school_info_printed = True
                else:
                    print_in_two_columns(
                        a.tournament_repr, b.tournament_repr, "Team 1", "Team 2"
                    )
                    # if rivalry:
                    #    print("RIVALRY GAME")
                    print_in_two_columns(
                        a.game_results,
                        b.game_results,
                        f"{a.name} Games",
                        f"{b.name} Games",
                    )
                    print_in_two_columns(
                        a.school_info,
                        b.school_info,
                        f"Additional {a.name} Info",
                        f"Additional {b.name} Info",
                    )
                print()
            elif choice == "q":
                confirm_quit = input("About to quit; are you sure? ")
                if "y" in confirm_quit or "q" in confirm_quit:
                    sys.exit()
                else:
                    print("Invalid choice selected; try again or select 'q' to exit")
            else:
                print()
                print("Invalid choice selected; try again or select 'q' to exit")
            if not school_info_printed:
                prompt = "Select 1, 2, m, or r (see even more info, random): "
            else:
                prompt = "All info displayed. Select 1, 2, or r (random): "
    except KeyboardInterrupt:
        sys.exit()
