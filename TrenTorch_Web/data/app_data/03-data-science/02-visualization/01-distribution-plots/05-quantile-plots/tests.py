"""
pytest tests.py
"""

import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
normal_ppf = _module.normal_ppf
plotting_positions = _module.plotting_positions
qq_points = _module.qq_points
qq_line = _module.qq_line
qq_correlation = _module.qq_correlation


# ---- 1-6: inverse normal CDF ----


def test_1_known_quantiles():
    assert abs(normal_ppf(0.5)) < 1e-9
    assert abs(normal_ppf(0.975) - 1.959963984540054) < 1e-8
    assert abs(normal_ppf(0.841344746068543) - 1.0) < 1e-8


def test_2_is_antisymmetric_around_one_half():
    for p in (0.01, 0.2, 0.37):
        assert abs(normal_ppf(p) + normal_ppf(1 - p)) < 1e-8


def test_3_inverts_the_cdf():
    for z in (-3.0, -0.4, 0.0, 1.7, 4.0):
        p = 0.5 * (1 + math.erf(z / math.sqrt(2)))
        assert abs(normal_ppf(p) - z) < 1e-7


def test_4_is_increasing():
    values = [normal_ppf(p) for p in np.linspace(0.01, 0.99, 50)]
    assert all(b > a for a, b in zip(values, values[1:]))


def test_5_extreme_probabilities_are_finite():
    assert normal_ppf(1e-10) < -6.0 and normal_ppf(1 - 1e-10) > 6.0


def test_6_probabilities_outside_the_open_interval_raise_value_error():
    for bad in (0.0, 1.0, -0.1, 1.5):
        with pytest.raises(ValueError):
            normal_ppf(bad)


# ---- 7-9: plotting positions ----


def test_7_positions_hand_computed():
    np.testing.assert_allclose(plotting_positions(4), [0.125, 0.375, 0.625, 0.875])


def test_8_positions_are_strictly_inside_zero_and_one():
    p = plotting_positions(50)
    assert p.min() > 0.0 and p.max() < 1.0 and np.all(np.diff(p) > 0)


def test_9_positions_are_symmetric():
    p = plotting_positions(9)
    np.testing.assert_allclose(p + p[::-1], np.ones(9))


# ---- 10-13: the points ----


def test_10_sample_is_sorted_and_arrays_match_in_length():
    x = np.random.default_rng(0).normal(size=40)
    theoretical, sample = qq_points(x)
    assert theoretical.shape == sample.shape == (40,)
    assert np.all(np.diff(sample) >= 0) and np.all(np.diff(theoretical) > 0)


def test_11_theoretical_quantiles_come_from_the_plotting_positions():
    _, _ = qq_points(np.arange(5.0))
    theoretical, _ = qq_points(np.arange(5.0))
    expected = [normal_ppf(p) for p in (0.1, 0.3, 0.5, 0.7, 0.9)]
    np.testing.assert_allclose(theoretical, expected)


def test_12_normal_data_gives_points_near_mean_plus_std_times_z():
    x = np.random.default_rng(1).normal(loc=5.0, scale=2.0, size=4000)
    theoretical, sample = qq_points(x)
    middle = slice(400, 3600)
    np.testing.assert_allclose(sample[middle], 5.0 + 2.0 * theoretical[middle], atol=0.15)


def test_13_input_is_not_modified():
    x = np.array([3.0, 1.0, 2.0])
    original = x.copy()
    qq_points(x)
    np.testing.assert_array_equal(x, original)


# ---- 14-16: the reference line ----


def test_14_recovers_the_mean_and_std_of_normal_data():
    x = np.random.default_rng(2).normal(loc=-3.0, scale=0.5, size=20_000)
    slope, intercept = qq_line(*qq_points(x))
    assert abs(slope - 0.5) < 0.02 and abs(intercept + 3.0) < 0.02


def test_15_hand_computed_line_through_two_quartile_points():
    theoretical = np.array([-1.0, 0.0, 1.0, 2.0, 3.0])
    sample = 10.0 + 2.0 * theoretical
    slope, intercept = qq_line(theoretical, sample)
    assert np.isclose(slope, 2.0) and np.isclose(intercept, 10.0)


def test_16_the_line_ignores_extreme_tail_values():
    x = np.random.default_rng(3).normal(size=500)
    contaminated = np.append(x, [1000.0, -1000.0])
    clean = qq_line(*qq_points(x))
    dirty = qq_line(*qq_points(contaminated))
    assert abs(dirty[0] - clean[0]) < 0.1


# ---- 17-19: straightness ----


def test_17_normal_data_is_very_straight():
    assert qq_correlation(np.random.default_rng(4).normal(size=2000)) > 0.998


def test_18_heavy_tails_and_skew_are_less_straight_than_normal():
    rng = np.random.default_rng(5)
    normal = qq_correlation(rng.normal(size=2000))
    skewed = qq_correlation(rng.exponential(size=2000))
    heavy = qq_correlation(rng.standard_t(2, size=2000))
    assert skewed < normal and heavy < normal


def test_19_correlation_is_unchanged_by_shifting_and_scaling():
    x = np.random.default_rng(6).normal(size=300)
    assert np.isclose(qq_correlation(x), qq_correlation(7.0 * x + 100.0))
