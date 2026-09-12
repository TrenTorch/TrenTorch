"""
pytest data/app_data/00-math-and-statistics/07-statistical-inference/04-ab-testing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/07-statistical-inference/{Path(__file__).resolve().parent.name}"
)
conversion_rate = _module.conversion_rate
two_proportion_z_test = _module.two_proportion_z_test


def test_conversion_rate_matches_hand_computation():
    assert np.isclose(conversion_rate(120, 1000), 0.12)


def test_z_statistic_is_zero_for_identical_rates():
    z, p = two_proportion_z_test(100, 1000, 100, 1000)
    assert np.isclose(z, 0.0)
    assert np.isclose(p, 1.0)


def test_z_statistic_sign_matches_direction_of_difference():
    z_a_higher, _ = two_proportion_z_test(150, 1000, 100, 1000)
    z_b_higher, _ = two_proportion_z_test(100, 1000, 150, 1000)
    assert z_a_higher > 0.0
    assert z_b_higher < 0.0


def test_z_test_matches_known_oracle_values():
    # generated once, offline, via the standard pooled two-proportion
    # z-test formula (scipy.stats.norm for the CDF)
    z, p = two_proportion_z_test(120, 1000, 150, 1000)
    assert np.isclose(z, -1.963049807622355, atol=1e-9)
    assert np.isclose(p, 0.04964038686536876, atol=1e-9)


def test_p_value_is_small_for_a_dramatic_difference():
    _, p = two_proportion_z_test(500, 1000, 100, 1000)
    assert p < 0.001


def test_p_value_is_large_for_a_tiny_difference_with_small_samples():
    _, p = two_proportion_z_test(10, 100, 11, 100)
    assert p > 0.5


def test_larger_sample_sizes_make_the_same_rate_difference_more_significant():
    # The same 2-percentage-point gap is much more convincing with
    # more data behind it.
    _, p_small = two_proportion_z_test(12, 100, 10, 100)
    _, p_large = two_proportion_z_test(1200, 10000, 1000, 10000)
    assert p_large < p_small


def test_z_test_uses_pooled_proportion_not_each_groups_own_rate():
    # Directly targets a mutant that uses each group's own (unpooled)
    # rate in the standard error instead of the pooled rate: with very
    # different sample sizes and rates, pooled vs unpooled standard
    # errors diverge enough to give a clearly different z-statistic.
    conversions_a, visitors_a = 100, 200
    conversions_b, visitors_b = 100, 1000
    z, _ = two_proportion_z_test(conversions_a, visitors_a, conversions_b, visitors_b)

    p_a = conversions_a / visitors_a
    p_b = conversions_b / visitors_b
    p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / visitors_a + 1 / visitors_b))
    se_unpooled = np.sqrt(p_a * (1 - p_a) / visitors_a + p_b * (1 - p_b) / visitors_b)
    expected_pooled_z = (p_a - p_b) / se_pooled
    expected_unpooled_z = (p_a - p_b) / se_unpooled

    assert np.isclose(z, expected_pooled_z, atol=1e-9)
    assert not np.isclose(z, expected_unpooled_z, atol=1e-6)
