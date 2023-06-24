#!/usr/bin/env python3

"""
Module for determining weights in probability of team winning
"""

import matplotlib.pyplot as plt
from weight.lptr import lptr_tournament_only
from weight.sigmodal import sigmodal_tournament_only, sigmodal_k_tournament_only


def visualize_weight_functions():
    """
    Allows for visual comparison of how weight functions operate on rankings.

    Resources:
    ----------
    * https://chat.openai.com/share/875338f1-ca29-4637-a9a6-4722d29dfd75

    Returns
    -------
    None
    """
    rankings = list(range(1, 17))
    # Calculate probabilities using the two algorithms
    lptr_probs = [lptr_tournament_only(rank1, 17 - rank1)[0] for rank1 in rankings]
    sigmodal_probs = [
        sigmodal_tournament_only(rank1, 17 - rank1)[0] for rank1 in rankings
    ]
    sigmodal_k_probs_default = [
        sigmodal_k_tournament_only(rank1, 17 - rank1)[0] for rank1 in rankings
    ]
    sigmodal_k_probs_mod = [
        sigmodal_k_tournament_only(rank1, 17 - rank1, k=1)[0] for rank1 in rankings
    ]

    print(f"lptr: {lptr_probs}")
    print(f"sigmodal: {sigmodal_probs}")
    print(f"sigmodal_k: {sigmodal_k_probs_default}")
    print(f"sigmodal_k_mod: {sigmodal_k_probs_mod}")
    # Plotting the probabilities
    plt.plot(rankings, sigmodal_probs, label="sigmodal")
    plt.plot(rankings, lptr_probs, label="lptr")
    plt.plot(rankings, sigmodal_k_probs_default, label="sigmodal_k (default)")
    plt.plot(rankings, sigmodal_k_probs_mod, label="sigmodal_k (k=1)")
    plt.xlabel("Ranking")
    plt.ylabel("Probability")
    plt.title("Probabilities of Winning by Ranking")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    visualize_weight_functions()
