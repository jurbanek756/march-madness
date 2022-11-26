from predict.weight import lptr


def test_lptr():
    assert (1, 0) == lptr(1, 16)
    assert (0.5, 0.5) == lptr(1, 1)
    ranks = lptr(1, 9)
    assert (0.77, 0.23) == (round(ranks[0], 2), round(ranks[1], 2))
    for i in range(1, 17):
        for j in range(1, 17):
            ranks = lptr(i, j)
            assert ranks[0] + ranks[1] == 1
