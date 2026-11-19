from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_examples():
    assert solve([3, 2, 1, 5, 6, 4], 2) == 5
    assert solve([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4


def test_k_equals_one_is_the_maximum():
    assert solve([7, 2, 9, 4], 1) == 9


def test_k_equals_length_is_the_minimum():
    assert solve([7, 2, 9, 4], 4) == 2


def test_single_element():
    assert solve([5], 1) == 5


def test_duplicates_count_separately():
    assert solve([2, 2, 2, 2], 3) == 2
    assert solve([5, 5, 4], 2) == 5


def test_negative_values():
    assert solve([-1, -5, -3, 0], 2) == -1


def test_does_not_modify_input():
    nums = [3, 1, 2]
    solve(nums, 2)
    assert nums == [3, 1, 2]


def test_large_input():
    nums = list(range(200_000, 0, -1))
    assert solve(nums, 10) == 199_991
