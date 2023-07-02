#!/usr/bin/env python3

"""
Module for determining weights in probability of team winning
"""


import numpy as np
import matplotlib.pyplot as plt

from weight.lptr import lptr_tournament_only, lptr_with_ap
from weight.sigmodal import sigmodal_tournament_only, sigmodal_k_tournament_only


def visualize_2d_weight_functions():
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


def visualize_3d_weight_functions():
    """
    Allows for visual comparison of how weight functions operate on rankings that
    consider both tournament and AP rankings.

    Resources
    ---------
    * https://chat.openai.com/share/33d48396-192d-4237-b55c-60124783a1eb

    Returns
    -------
    None
    """
    rankings = np.arange(1, 16)
    ap_rankings = np.arange(1, 26)
    rankings, ap_rankings = np.meshgrid(rankings, ap_rankings)
    # Calculate probabilities using lptr function
    probabilities = np.zeros_like(rankings, dtype=float)
    for i in range(rankings.shape[0]):
        for j in range(rankings.shape[1]):
            res = lptr_with_ap(
                rankings[i, j],
                17 - rankings[i, j],
                ap_rankings[i, j],
                27 - ap_rankings[i, j],
            )
            probabilities[i, j] = res[0]
    print(probabilities)
    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")

    # Plot the surface
    ax.plot_surface(rankings, ap_rankings, probabilities, cmap="viridis")

    # Set labels and title
    ax.set_xlabel("Tournament Ranking")
    ax.set_ylabel("AP Ranking")
    ax.set_zlabel("Probability")
    ax.set_title("Probability of Team 1 Winning")

    # Show the plot
    plt.show()


if __name__ == "__main__":
    visualize_2d_weight_functions()
    visualize_3d_weight_functions()
