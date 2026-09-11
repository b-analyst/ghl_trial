from allocate import allocate


def test_weighted_three_way():
    assert sum(allocate(100, [1, 1, 4])) == 100


def test_weighted_uneven():
    assert sum(allocate(100, [2, 3, 7])) == 100


def test_weighted_two_way():
    assert sum(allocate(57, [1, 3])) == 57


def test_weighted_four_way():
    assert sum(allocate(1000, [1, 1, 1, 5])) == 1000


def test_equal_three_way_split():
    assert allocate(100, [1, 1, 1]) == [33, 33, 33]
