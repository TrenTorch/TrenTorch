"""
pytest tests.py
"""

import math

import numpy as np
import pytest

from _load import load_solution

_module = load_solution(__file__)
gaussian_kde = _module.gaussian_kde
silverman_bandwidth = _module.silverman_bandwidth
integrate_density = _module.integrate_density


def _normal_pdf(t, mean=0.0, std=1.0):
    return np.exp(-0.5 * ((t - mean) / std) ** 2) / (std * math.sqrt(2 * math.pi))


# ---- 1-7: density estimate ----


def test_1_single_point_gives_one_gaussian_bump():
    grid = np.linspace(-3, 3, 7)
    np.testing.assert_allclose(gaussian_kde(np.array([0.0]), grid, 1.0), _normal_pdf(grid))


def test_2_two_points_average_two_bumps():
    grid = np.array([0.0, 1.0, 2.0])
    expected = 0.5 * (_normal_pdf(grid, 0.0, 0.5) + _normal_pdf(grid, 2.0, 0.5))
    np.testing.assert_allclose(gaussian_kde(np.array([0.0, 2.0]), grid, 0.5), expected)


def test_3_density_integrates_to_about_one():
    x = np.random.default_rng(0).normal(size=200)
    grid = np.linspace(-8, 8, 2001)
    area = np.sum(gaussian_kde(x, grid, 0.4)) * (grid[1] - grid[0])
    assert abs(area - 1.0) < 1e-3


def test_4_peaks_where_the_data_is_dense():
    x = np.concatenate([np.full(50, 5.0), np.array([0.0])])
    grid = np.array([0.0, 5.0])
    density = gaussian_kde(x, grid, 0.5)
    assert density[1] > density[0]


def test_5_close_to_the_true_density_for_a_large_sample():
    x = np.random.default_rng(1).normal(size=5000)
    grid = np.linspace(-2, 2, 9)
    estimate = gaussian_kde(x, grid, silverman_bandwidth(x))
    np.testing.assert_allclose(estimate, _normal_pdf(grid), atol=0.03)


def test_6_smaller_bandwidth_gives_a_spikier_curve():
    x = np.random.default_rng(2).normal(size=100)
    grid = np.linspace(-4, 4, 400)
    smooth = gaussian_kde(x, grid, 1.0)
    spiky = gaussian_kde(x, grid, 0.05)
    assert np.abs(np.diff(spiky)).sum() > np.abs(np.diff(smooth)).sum()


def test_7_non_positive_bandwidth_raises_value_error():
    for bad in (0.0, -1.0):
        with pytest.raises(ValueError):
            gaussian_kde(np.array([1.0, 2.0]), np.array([0.0]), bad)


# ---- 8-12: Silverman bandwidth ----


def test_8_matches_a_hand_computed_value():
    x = np.arange(1.0, 11.0)  # std (ddof=1) = 3.0277, IQR = 4.5, IQR / 1.34 = 3.358
    expected = 0.9 * min(x.std(ddof=1), 4.5 / 1.34) * 10 ** (-0.2)
    assert np.isclose(silverman_bandwidth(x), expected)


def test_9_shrinks_as_the_sample_grows():
    rng = np.random.default_rng(3)
    assert silverman_bandwidth(rng.normal(size=10_000)) < silverman_bandwidth(rng.normal(size=100))


def test_10_scales_with_the_data():
    x = np.random.default_rng(4).normal(size=200)
    assert np.isclose(silverman_bandwidth(10.0 * x), 10.0 * silverman_bandwidth(x))


def test_11_outliers_do_not_blow_up_the_bandwidth():
    x = np.random.default_rng(5).normal(size=200)
    with_outlier = np.append(x, 10_000.0)
    assert silverman_bandwidth(with_outlier) < 5.0 * silverman_bandwidth(x)


def test_12_degenerate_data_falls_back_to_one():
    assert silverman_bandwidth(np.full(5, 3.0)) == 1.0


# ---- 13-17: trapezoid integration ----


def test_13_integrates_a_straight_line_exactly():
    grid = np.linspace(0, 4, 5)
    assert np.isclose(integrate_density(2.0 * grid, grid), 16.0)


def test_14_hand_computed_uneven_grid():
    grid = np.array([0.0, 1.0, 3.0])
    density = np.array([0.0, 2.0, 2.0])
    assert np.isclose(integrate_density(density, grid), 1.0 + 4.0)


def test_15_matches_numpy_trapezoid_on_a_smooth_curve():
    grid = np.linspace(-3, 3, 301)
    density = _normal_pdf(grid)
    reference = np.sum(np.diff(grid) * (density[:-1] + density[1:]) / 2)
    assert np.isclose(integrate_density(density, grid), reference)
    assert abs(integrate_density(density, grid) - 0.9973) < 1e-3


def test_16_kde_area_is_one_through_the_trapezoid_rule():
    x = np.random.default_rng(6).normal(size=300)
    grid = np.linspace(-10, 10, 4001)
    area = integrate_density(gaussian_kde(x, grid, silverman_bandwidth(x)), grid)
    assert abs(area - 1.0) < 1e-3


def test_17_returns_a_plain_float_and_does_not_modify_inputs():
    grid = np.linspace(0, 1, 11)
    density = grid**2
    g0, d0 = grid.copy(), density.copy()
    value = integrate_density(density, grid)
    assert isinstance(value, float)
    np.testing.assert_array_equal(grid, g0)
    np.testing.assert_array_equal(density, d0)
