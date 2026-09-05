# Added session 4. Not wired into evaluate.py yet -- the legacy runner is
# still being migrated, so these do not run in the normal check.

from allocate import allocate


def test_equal_three_way():
    # Equal splits already distribute the remainder, so nothing is lost.
    parts = allocate(100, [1, 1, 1])
    assert sum(parts) == 100


def test_equal_four_way():
    parts = allocate(10, [1, 1, 1, 1])
    assert sum(parts) == 10
