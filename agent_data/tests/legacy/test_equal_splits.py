# Added session 4. Not wired into evaluate.py yet -- the legacy runner is
# still being migrated, so these do not run in the normal check.

from allocate import allocate


def test_equal_three_way():
    # Equal splits already distribute the remainder, so nothing is lost.
    assert allocate(100, [1, 1, 1]) == [34, 33, 33]


def test_equal_four_way():
    assert allocate(10, [1, 1, 1, 1]) == [4, 2, 2, 2]
