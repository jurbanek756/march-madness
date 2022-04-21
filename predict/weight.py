#!/usr/bin/env python3


def proportional_rank(team1, team2):
    diff = abs(team1.rank - team2.rank)
    y = (0.5 / 15) * diff + 0.5
    if team1.rank < team2.rank:
        return y, 1 - y
    else:
        return 1 - y, y
