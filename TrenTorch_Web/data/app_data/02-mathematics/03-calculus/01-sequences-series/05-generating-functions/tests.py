"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mgf = _module.mgf
pgf = _module.pgf
mgf_moments = _module.mgf_moments
pgf_mean_variance = _module.pgf_mean_variance
sum_distribution = _module.sum_distribution


def _binomial(n, p):
    return np.array([math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)])


# ---- 1-4: moment generating function ----


def test_1_mgf_matches_a_hand_computed_case():
    # fair coin on {0, 1}: M(t) = (1 + e^t) / 2
    assert math.isclose(mgf([0, 1], [0.5, 0.5], 1.0), (1 + math.e) / 2)


def test_2_mgf_at_zero_is_exactly_one():
    assert mgf([1, 5, -3], [0.2, 0.5, 0.3], 0) == 1.0


def test_3_mgf_accepts_an_array_of_t():
    t = np.array([-1.0, 0.0, 0.5])
    out = mgf([0, 1], [0.5, 0.5], t)
    assert out.shape == (3,)
    np.testing.assert_allclose(out, (1 + np.exp(t)) / 2)


def test_4_mgf_handles_negative_and_non_integer_values():
    values, probs = [-1.5, 0.25, 2.0], [0.3, 0.3, 0.4]
    expected = sum(p * math.exp(0.7 * x) for x, p in zip(values, probs))
    assert math.isclose(mgf(values, probs, 0.7), expected)


# ---- 5-7: probability generating function ----


def test_5_pgf_matches_a_hand_computed_case():
    # P = [0.2, 0.3, 0.5]: G(2) = 0.2 + 0.6 + 2.0
    assert math.isclose(pgf([0.2, 0.3, 0.5], 2.0), 2.8)


def test_6_pgf_at_one_is_one_and_at_zero_is_p_of_zero():
    p = [0.1, 0.4, 0.5]
    assert math.isclose(pgf(p, 1.0), 1.0)
    assert math.isclose(pgf(p, 0.0), 0.1)


def test_7_pgf_accepts_an_array_of_z():
    z = np.array([0.0, 0.5, 1.0])
    np.testing.assert_allclose(pgf([0.25, 0.25, 0.5], z), 0.25 + 0.25 * z + 0.5 * z**2)


# ---- 8-10: moments from the MGF ----


def test_8_moments_of_a_fair_die_from_numerical_derivatives():
    values = np.arange(1, 7)
    probs = np.full(6, 1 / 6)
    first, second = mgf_moments(lambda t: mgf(values, probs, t))
    assert math.isclose(first, 3.5, rel_tol=1e-4)
    assert math.isclose(second, 91 / 6, rel_tol=1e-4)


def test_9_moments_of_a_normal_mgf():
    # N(2, 3^2): M(t) = exp(2 t + 4.5 t^2); E[X] = 2, E[X^2] = 4 + 9 = 13
    first, second = mgf_moments(lambda t: math.exp(2 * t + 4.5 * t**2), step=1e-3)
    assert math.isclose(first, 2.0, rel_tol=1e-5)
    assert math.isclose(second, 13.0, rel_tol=1e-4)


def test_10_smaller_step_gives_a_more_accurate_derivative():
    f = lambda t: math.exp(t)
    err_coarse = abs(mgf_moments(f, step=0.1)[0] - 1.0)
    err_fine = abs(mgf_moments(f, step=0.01)[0] - 1.0)
    assert err_fine < err_coarse


# ---- 11-14: mean and variance from the PGF ----


def test_11_binomial_mean_and_variance():
    mean, var = pgf_mean_variance(_binomial(10, 0.3))
    assert math.isclose(mean, 3.0)
    assert math.isclose(var, 10 * 0.3 * 0.7)


def test_12_point_mass_has_zero_variance():
    mean, var = pgf_mean_variance([0, 0, 0, 1.0])
    assert math.isclose(mean, 3.0)
    assert abs(var) < 1e-12


def test_13_matches_a_direct_weighted_average():
    p = np.array([0.1, 0.2, 0.3, 0.4])
    k = np.arange(4)
    mean, var = pgf_mean_variance(p)
    assert math.isclose(mean, (k * p).sum())
    assert math.isclose(var, (p * (k - (k * p).sum()) ** 2).sum())


def test_14_returns_plain_floats():
    mean, var = pgf_mean_variance([0.5, 0.5])
    assert isinstance(mean, float) and isinstance(var, float)


# ---- 15-18: sums of independent variables ----


def test_15_sum_of_two_fair_dice():
    die = [0] + [1 / 6] * 6  # faces 1..6 as outcomes 1..6 (index = outcome)
    total = sum_distribution(die, die)
    assert len(total) == 13
    assert math.isclose(total[7], 6 / 36)
    assert math.isclose(total[2], 1 / 36)
    assert math.isclose(total.sum(), 1.0)


def test_16_sum_of_binomials_is_binomial():
    got = sum_distribution(_binomial(4, 0.3), _binomial(6, 0.3))
    np.testing.assert_allclose(got, _binomial(10, 0.3), atol=1e-12)


def test_17_pgf_of_the_sum_is_the_product_of_pgfs():
    p, q = [0.2, 0.5, 0.3], [0.6, 0.4]
    s = sum_distribution(p, q)
    for z in (0.3, 1.0, 1.7):
        assert math.isclose(pgf(s, z), pgf(p, z) * pgf(q, z))


def test_18_means_add_for_independent_sums():
    p, q = [0.2, 0.5, 0.3], [0.6, 0.4]
    mean_sum, var_sum = pgf_mean_variance(sum_distribution(p, q))
    mean_p, var_p = pgf_mean_variance(p)
    mean_q, var_q = pgf_mean_variance(q)
    assert math.isclose(mean_sum, mean_p + mean_q)
    assert math.isclose(var_sum, var_p + var_q)
