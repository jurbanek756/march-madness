#!/usr/bin/env python3

import random

def random_selection(a, b):
    return random.choice([a, b])

def weighted_random_selection(a, b):
    return random.choices(population=[a, b], k=1, weights=generate_relative_weight(a, b))

def generate_relative_weight(a, b):
    a_rank = 1 - (a.rank / 16)
    b_rank = 1 - (b.rank / 16)
    if a.rank > b.rank:
        a_rank += (1/16)
        b_rank -= (1/16)
    else:
        a_rank -= (1/16)
        b_rank += (1/16)
    if a_rank + b_rank == 1
        return a_rank + b_rank
    elif a_rank + b_rank > 1:
        pass
    else:
        pass
    return [0.5, 0.5]

def ranked_selection(a, b):
    if a.rank > b.rank:
        return b
    elif b.rank > a.rank:
        return a
    else:
        team = ap_selection(a, b):
        if team:
            return team
        else:
            return random_selection(a, b)


def ap_selection(a, b):
    if a.ap_rank > b.ap_rank:
        return a
    elif b.ap_rank > a.ap_rank:
        return b
    else:
        return None

