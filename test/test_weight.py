from team.Team import Team
from predict.weight import proportional_rank


def test_proportional_rank():
    t1, t2 = Team(), Team()
    t1.rank = 1
    t2.rank = 16
    assert (1, 0) == proportional_rank(t1, t2)
    t2.rank = 1
    assert (0.5, 0.5) == proportional_rank(t1, t2)
