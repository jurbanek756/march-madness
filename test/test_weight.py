from team.Team import Team
from predict.weight import lptr


def test_lptr():
    t1, t2 = Team(), Team()
    t1.tournament_rank = 1
    t2.tournament_rank = 16
    assert (1, 0) == lptr(t1, t2)
    t2.tournament_rank = 1
    assert (0.5, 0.5) == lptr(t1, t2)
    t2.tournament_rank = 9
    ranks = lptr(t1, t2)
    assert (0.77, 0.23) == (round(ranks[0], 2), round(ranks[1], 2))
