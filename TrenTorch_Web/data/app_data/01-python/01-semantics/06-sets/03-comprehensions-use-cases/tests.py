"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
squared_unique = _module.squared_unique
positive_unique = _module.positive_unique
word_lengths = _module.word_lengths
coordinate_sums = _module.coordinate_sums
find_duplicates = _module.find_duplicates
unique_in_first_seen_order = _module.unique_in_first_seen_order
all_seen_before = _module.all_seen_before
missing_values = _module.missing_values


def test_transformation():
    assert squared_unique([1, 2, 3]) == {1, 4, 9}


def test_duplicate_collapse():
    assert squared_unique([-2, -1, 1, 2]) == {1, 4}


def test_filtering_boundary():
    assert positive_unique([-2, 3, 3, 0, 5, -1]) == {3, 5}
    assert 0 not in positive_unique([-1, 0, 1])


def test_empty_input():
    assert squared_unique([]) == set()
    assert positive_unique([]) == set()
    assert word_lengths([]) == set()
    assert coordinate_sums([]) == set()


def test_comprehensions_preserve_input():
    values = [-2, -1, 1, 2]
    squared_unique(values)
    positive_unique(values)
    assert values == [-2, -1, 1, 2]

    words = ["cat", "dog", "house"]
    assert word_lengths(words) == {3, 5}
    assert words == ["cat", "dog", "house"]

    points = [(1, 2), (3, 4), (0, 3)]
    assert coordinate_sums(points) == {3, 7}
    assert points == [(1, 2), (3, 4), (0, 3)]


def test_duplicate_detection():
    assert find_duplicates([1, 2, 1, 3, 2, 2]) == {1, 2}


def test_first_seen_order():
    assert unique_in_first_seen_order([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_no_duplicates():
    assert find_duplicates([1, 2, 3]) == set()
    assert unique_in_first_seen_order([1, 2, 3]) == [1, 2, 3]


def test_repeated_values():
    assert find_duplicates([5, 5, 5, 5]) == {5}
    assert all_seen_before([1, 2, 1, 2]) is True
    assert all_seen_before([1, 2, 1]) is False


def test_missing_values():
    assert missing_values([1, 3, 3], {1, 2, 3, 4}) == {2, 4}
    assert missing_values([], {1, 2}) == {1, 2}
    assert missing_values([1, 2], {1, 2}) == set()


def test_use_case_functions_preserve_input():
    values = [1, 2, 1, 3]
    expected = {1, 2, 3, 4}
    find_duplicates(values)
    unique_in_first_seen_order(values)
    missing_values(values, expected)
    assert values == [1, 2, 1, 3]
    assert expected == {1, 2, 3, 4}
