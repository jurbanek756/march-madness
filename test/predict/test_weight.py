from weight.lptr import lptr_tournament_only
from weight.sigmodal import sigmodal_tournament_only, sigmodal_k_tournament_only


def test_lptr():
    assert (1, 0) == lptr_tournament_only(1, 16)
    assert (0.5, 0.5) == lptr_tournament_only(1, 1)
    ranks = lptr_tournament_only(1, 9)
    assert (0.77, 0.23) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = lptr_tournament_only(i, j)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal():
    assert (1, 0) == sigmodal_tournament_only(1, 16)
    assert (0.5, 0.5) == sigmodal_tournament_only(1, 1)
    ranks = sigmodal_tournament_only(1, 9)
    assert (0.89, 0.11) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_tournament_only(4, 5)
    assert (0.5, 0.5) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_tournament_only(2, 11)
    assert (0.9, 0.1) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_tournament_only(i, j)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i - j < -1:
                assert ranks[0] > ranks[1]
            elif i - j > 1:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_tournament_only_default():
    assert (1, 0) == sigmodal_k_tournament_only(1, 16)
    assert (0.5, 0.5) == sigmodal_k_tournament_only(1, 1)
    ranks = sigmodal_k_tournament_only(1, 9)
    assert (0.93, 0.07) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k_tournament_only(4, 5)
    assert (0.58, 0.42) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k_tournament_only(i, j)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_tournament_only_low():
    assert (1, 0) == sigmodal_k_tournament_only(1, 16, k=0.1)
    assert (0.5, 0.5) == sigmodal_k_tournament_only(1, 1, k=0.1)
    ranks = sigmodal_k_tournament_only(1, 9, k=0.1)
    assert (0.69, 0.31) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k_tournament_only(4, 5, k=0.1)
    assert (0.52, 0.48) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k_tournament_only(i, j, k=0.1)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_tournament_only_high():
    assert (1, 0) == sigmodal_k_tournament_only(1, 16, k=3)
    assert (0.5, 0.5) == sigmodal_k_tournament_only(1, 1, k=3)
    ranks = sigmodal_k_tournament_only(1, 9, k=3)
    assert (1, 0) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k_tournament_only(4, 5, k=3)
    assert (0.95, 0.05) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k_tournament_only(i, j, k=3)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]
