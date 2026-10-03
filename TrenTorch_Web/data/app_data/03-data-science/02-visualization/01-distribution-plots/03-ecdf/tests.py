"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
ecdf = _module.ecdf
ecdf_at = _module.ecdf_at
ks_distance = _module.ks_distance


# ---- 1-5: the staircase ----


def test_1_hand_computed_points():
    values, probabilities = ecdf(np.array([3.0, 1.0, 2.0]))
    np.testing.assert_array_equal(values, [1.0, 2.0, 3.0])
    np.testing.assert_allclose(probabilities, [1 / 3, 2 / 3, 1.0])


def test_2_last_probability_is_exactly_one_and_steps_are_equal():
    _, probabilities = ecdf(np.random.default_rng(0).normal(size=37))
    assert probabilities[-1] == 1.0
    np.testing.assert_allclose(np.diff(probabilities), 1 / 37)


def test_3_repeated_values_each_get_an_entry():
    values, probabilities = ecdf(np.array([2.0, 2.0, 5.0]))
    assert len(values) == 3 and probabilities[0] < probabilities[1]


def test_4_values_are_sorted_and_input_is_not_modified():
    x = np.array([5.0, 1.0, 3.0])
    original = x.copy()
    values, _ = ecdf(x)
    assert np.all(np.diff(values) >= 0)
    np.testing.assert_array_equal(x, original)


def test_5_single_value():
    values, probabilities = ecdf(np.array([4.0]))
    assert values[0] == 4.0 and probabilities[0] == 1.0


# ---- 6-11: evaluating anywhere ----


def test_6_evaluates_at_and_between_data_points():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    np.testing.assert_allclose(ecdf_at(x, np.array([2.0, 2.5, 4.0])), [0.5, 0.5, 1.0])


def test_7_below_the_minimum_is_zero_and_above_the_maximum_is_one():
    x = np.array([1.0, 2.0, 3.0])
    np.testing.assert_allclose(ecdf_at(x, np.array([-100.0, 100.0])), [0.0, 1.0])


def test_8_ties_count_with_less_than_or_equal():
    assert np.isclose(ecdf_at(np.array([1.0, 2.0, 2.0, 3.0]), np.array([2.0]))[0], 0.75)


def test_9_matches_a_brute_force_count():
    rng = np.random.default_rng(1)
    x, points = rng.normal(size=200), rng.normal(size=25)
    expected = [np.mean(x <= p) for p in points]
    np.testing.assert_allclose(ecdf_at(x, points), expected)


def test_10_is_monotone_non_decreasing():
    x = np.random.default_rng(2).exponential(size=100)
    grid = np.linspace(-1, 10, 200)
    assert np.all(np.diff(ecdf_at(x, grid)) >= 0)


def test_11_agrees_with_the_staircase_points():
    x = np.random.default_rng(3).normal(size=30)
    values, probabilities = ecdf(x)
    np.testing.assert_allclose(ecdf_at(x, values), probabilities)


# ---- 12-17: KS distance ----


def test_12_identical_samples_have_zero_distance():
    x = np.random.default_rng(4).normal(size=100)
    assert ks_distance(x, x.copy()) == 0.0


def test_13_disjoint_samples_have_distance_one():
    assert np.isclose(ks_distance(np.array([1.0, 2.0, 3.0]), np.array([10.0, 11.0])), 1.0)


def test_14_hand_computed_case():
    # F_x steps at 1, 2, 3 (thirds); F_y steps at 2, 4 (halves)
    # at t=1: |1/3 - 0| = 1/3; at t=2: |2/3 - 1/2| = 1/6; at t=3: |1 - 1/2| = 1/2
    assert np.isclose(ks_distance(np.array([1.0, 2.0, 3.0]), np.array([2.0, 4.0])), 0.5)


def test_15_is_symmetric():
    rng = np.random.default_rng(5)
    x, y = rng.normal(size=80), rng.normal(0.5, 1.0, size=60)
    assert np.isclose(ks_distance(x, y), ks_distance(y, x))


def test_16_a_shifted_distribution_is_further_away_than_a_slightly_shifted_one():
    rng = np.random.default_rng(6)
    base = rng.normal(size=1000)
    near = ks_distance(base, rng.normal(0.1, 1.0, size=1000))
    far = ks_distance(base, rng.normal(1.5, 1.0, size=1000))
    assert far > near


def test_17_matches_a_brute_force_search_over_a_fine_grid():
    rng = np.random.default_rng(7)
    x, y = rng.normal(size=70), rng.uniform(-2, 2, size=50)
    grid = np.sort(np.concatenate([x, y]))
    brute = max(abs(np.mean(x <= t) - np.mean(y <= t)) for t in grid)
    assert np.isclose(ks_distance(x, y), brute)
