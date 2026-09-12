"""
pytest data/app_data/00-math-and-statistics/07-statistical-inference/01-confidence-interval/tests.py
"""

import sys
from pathlib import Path

import numpy as np
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/07-statistical-inference/{Path(__file__).resolve().parent.name}"
)
standard_error_of_mean = _module.standard_error_of_mean
confidence_interval_mean = _module.confidence_interval_mean


def test_standard_error_of_mean_matches_hand_computation():
    x = np.array([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])
    expected = np.std(x, ddof=1) / np.sqrt(8)
    assert np.isclose(standard_error_of_mean(x), expected)


def test_confidence_interval_is_centered_on_the_sample_mean():
    rng = np.random.default_rng(0)
    x = rng.normal(50.0, 10.0, size=30)
    lower, upper = confidence_interval_mean(x)
    assert np.isclose((lower + upper) / 2, np.mean(x))


def test_confidence_interval_matches_scipy_reference():
    rng = np.random.default_rng(1)
    x = rng.normal(100.0, 15.0, size=30)
    lower, upper = confidence_interval_mean(x, confidence=0.95)
    sem = np.std(x, ddof=1) / np.sqrt(len(x))
    expected_lower, expected_upper = stats.t.interval(0.95, df=len(x) - 1, loc=np.mean(x), scale=sem)
    assert np.isclose(lower, expected_lower)
    assert np.isclose(upper, expected_upper)


def test_higher_confidence_gives_a_wider_interval():
    rng = np.random.default_rng(2)
    x = rng.normal(0.0, 1.0, size=30)
    lower_90, upper_90 = confidence_interval_mean(x, confidence=0.90)
    lower_99, upper_99 = confidence_interval_mean(x, confidence=0.99)
    assert (upper_99 - lower_99) > (upper_90 - lower_90)


def test_larger_sample_gives_a_narrower_interval():
    rng = np.random.default_rng(3)
    small_sample = rng.normal(0.0, 1.0, size=10)
    large_sample = rng.normal(0.0, 1.0, size=1000)
    small_lower, small_upper = confidence_interval_mean(small_sample)
    large_lower, large_upper = confidence_interval_mean(large_sample)
    assert (large_upper - large_lower) < (small_upper - small_lower)


def test_confidence_interval_contains_the_true_mean_most_of_the_time():
    # A direct empirical check of the definition: repeatedly sample from
    # a known distribution and confirm the interval contains the true
    # mean roughly as often as the confidence level promises.
    rng = np.random.default_rng(4)
    true_mean = 50.0
    contained = 0
    trials = 200
    for _ in range(trials):
        sample = rng.normal(true_mean, 10.0, size=25)
        lower, upper = confidence_interval_mean(sample, confidence=0.95)
        if lower <= true_mean <= upper:
            contained += 1
    assert contained / trials > 0.85  # should be close to 0.95, allow slack for randomness


def test_confidence_interval_uses_t_distribution_not_a_fixed_z_value():
    # Directly targets a mutant that hardcodes a z-value (like 1.96) in
    # place of the t-distribution's critical value: for a small sample,
    # the correct t-based interval must be strictly WIDER than a
    # z-based (1.96) interval would give, since t has heavier tails.
    rng = np.random.default_rng(5)
    x = rng.normal(0.0, 1.0, size=5)  # small sample, t and z diverge noticeably
    lower, upper = confidence_interval_mean(x, confidence=0.95)
    sem = np.std(x, ddof=1) / np.sqrt(len(x))
    z_based_margin = 1.96 * sem
    t_based_margin = (upper - lower) / 2
    assert t_based_margin > z_based_margin
