"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
insertion_points = _module.insertion_points
count_between = _module.count_between
bucketize = _module.bucketize
nearest_value = _module.nearest_value
is_present = _module.is_present

A = np.array([10, 20, 20, 30])


def test_insertion_points_left_and_right():
    np.testing.assert_array_equal(insertion_points(A, np.array([20]), "left"), [1])
    np.testing.assert_array_equal(insertion_points(A, np.array([20]), "right"), [3])


def test_insertion_points_for_values_outside_and_between():
    np.testing.assert_array_equal(insertion_points(A, np.array([5, 25, 99]), "left"), [0, 3, 4])


def test_insertion_keeps_the_array_sorted():
    a = np.sort(np.random.default_rng(0).integers(0, 50, size=40))
    v = np.random.default_rng(1).integers(0, 50, size=10)
    for value, position in zip(v, insertion_points(a, v, "left")):
        out = np.insert(a, position, value)
        assert np.all(np.diff(out) >= 0)


def test_count_between_is_inclusive_at_both_ends():
    assert count_between(A, 20, 30) == 3
    assert count_between(A, 10, 10) == 1
    assert count_between(A, 11, 19) == 0


def test_count_between_matches_a_brute_force_count():
    a = np.sort(np.random.default_rng(2).integers(0, 30, size=60))
    for lo, hi in [(0, 5), (10, 10), (7, 22), (29, 40), (-3, 100)]:
        assert count_between(a, lo, hi) == int(np.sum((a >= lo) & (a <= hi)))


def test_count_between_returns_an_int():
    assert type(count_between(A, 0, 100)) is int


def test_bucketize_known_values():
    edges = np.array([10, 20, 30])
    np.testing.assert_array_equal(bucketize(np.array([5, 10, 15, 20, 29, 30, 99]), edges), [0, 1, 1, 2, 2, 3, 3])


def test_bucketize_matches_digitize():
    edges = np.array([0.0, 1.5, 3.0, 7.0])
    v = np.random.default_rng(3).uniform(-2, 9, size=50)
    np.testing.assert_array_equal(bucketize(v, edges), np.digitize(v, edges))


def test_nearest_value_picks_the_closest_neighbour():
    a = np.array([1, 5, 9, 20])
    np.testing.assert_array_equal(nearest_value(a, np.array([0, 4, 8, 15, 100])), [1, 5, 9, 20, 20])


def test_nearest_value_ties_go_to_the_smaller_value():
    a = np.array([10, 20])
    np.testing.assert_array_equal(nearest_value(a, np.array([15])), [10])


def test_nearest_value_matches_brute_force():
    a = np.sort(np.random.default_rng(4).integers(0, 100, size=25))
    t = np.random.default_rng(5).integers(-10, 110, size=30)
    expected = [a[np.argmin(np.abs(a - x))] for x in t]
    np.testing.assert_array_equal(nearest_value(a, t), expected)


def test_is_present_checks_membership():
    np.testing.assert_array_equal(is_present(A, np.array([10, 15, 30, 31, 5])), [True, False, True, False, False])


def test_is_present_handles_values_beyond_both_ends():
    assert not is_present(np.array([1, 2, 3]), np.array([100])).any()
    assert not is_present(np.array([1, 2, 3]), np.array([-5])).any()
