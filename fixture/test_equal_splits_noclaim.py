# Added session 4. Not wired into evaluate.py yet -- the legacy runner is
# still being migrated, so these do not run in the normal check.

from allocate import allocate


def test_weighted_two_way():
    parts = allocate(57, [1, 3])
    assert sum(parts) == 57


def test_weighted_four_way():
    parts = allocate(1000, [1, 1, 1, 5])
    assert sum(parts) == 1000
