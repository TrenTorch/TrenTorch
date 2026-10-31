from _load import load_solution

_module = load_solution(__file__)
solve = _module.solve


def test_found_in_middle():
    assert solve([1, 3, 5, 7, 9], 5) == 2


def test_found_at_ends():
    assert solve([1, 3, 5, 7, 9], 1) == 0
    assert solve([1, 3, 5, 7, 9], 9) == 4


def test_not_found():
    assert solve([1, 3, 5, 7, 9], 4) == -1
    assert solve([1, 3, 5, 7, 9], 0) == -1
    assert solve([1, 3, 5, 7, 9], 10) == -1


def test_empty_and_single():
    assert solve([], 3) == -1
    assert solve([3], 3) == 0
    assert solve([3], 2) == -1


def test_negative_values():
    assert solve([-9, -4, -1, 0, 6], -4) == 1


def test_large_input():
    arr = list(range(0, 2_000_000, 2))
    assert solve(arr, 1_999_998) == 999_999
    assert solve(arr, 1_999_999) == -1
