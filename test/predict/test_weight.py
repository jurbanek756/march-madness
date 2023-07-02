from predict.weight import lptr, sigmodal, sigmodal_k


def test_lptr():
    assert (1, 0) == lptr(1, 16)
    assert (0.5, 0.5) == lptr(1, 1)
    ranks = lptr(1, 9)
    assert (0.77, 0.23) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = lptr(i, j)
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
    assert (1, 0) == sigmodal(1, 16)
    assert (0.5, 0.5) == sigmodal(1, 1)
    ranks = sigmodal(1, 9)
    assert (0.89, 0.11) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal(4, 5)
    assert (0.5, 0.5) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal(2, 11)
    assert (0.9, 0.1) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal(i, j)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i - j < -1:
                assert ranks[0] > ranks[1]
            elif i - j > 1:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_default():
    assert (1, 0) == sigmodal_k(1, 16)
    assert (0.5, 0.5) == sigmodal_k(1, 1)
    ranks = sigmodal_k(1, 9)
    assert (0.93, 0.07) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k(4, 5)
    assert (0.58, 0.42) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k(i, j)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_low():
    assert (1, 0) == sigmodal_k(1, 16, k=0.1)
    assert (0.5, 0.5) == sigmodal_k(1, 1, k=0.1)
    ranks = sigmodal_k(1, 9, k=0.1)
    assert (0.69, 0.31) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k(4, 5, k=0.1)
    assert (0.52, 0.48) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k(i, j, k=0.1)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]


def test_sigmodal_k_high():
    assert (1, 0) == sigmodal_k(1, 16, k=3)
    assert (0.5, 0.5) == sigmodal_k(1, 1, k=3)
    ranks = sigmodal_k(1, 9, k=3)
    assert (1, 0) == (round(ranks[0], 2), round(ranks[1], 2))
    ranks = sigmodal_k(4, 5, k=3)
    assert (0.95, 0.05) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = sigmodal_k(i, j, k=3)
            assert (
                ranks[0] + ranks[1] == 1
            )  # may eventually need to code in tolerance because float math
            if i < j:
                assert ranks[0] > ranks[1]
            elif i > j:
                assert ranks[0] < ranks[1]
            else:
                assert ranks[0] == ranks[1]
