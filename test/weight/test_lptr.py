from weight.lptr import lptr_tournament_only


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
