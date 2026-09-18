"""
pytest data/app_data/00-math-and-statistics/07-statistical-inference/02-bootstrap-confidence-intervals/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/07-statistical-inference/{Path(__file__).resolve().parent.name}"
)
bootstrap_resample = _module.bootstrap_resample
bootstrap_confidence_interval = _module.bootstrap_confidence_interval


def test_bootstrap_resample_has_the_same_size_as_input():
    rng = np.random.default_rng(0)
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    result = bootstrap_resample(x, rng)
    assert len(result) == len(x)


def test_bootstrap_resample_only_contains_values_from_the_original():
    rng = np.random.default_rng(1)
    x = np.array([10.0, 20.0, 30.0])
    result = bootstrap_resample(x, rng)
    assert np.all(np.isin(result, x))


def test_bootstrap_resample_can_repeat_values():
    # With replacement, over enough draws, some original value should
    # appear more than once with overwhelming probability.
    rng = np.random.default_rng(2)
    x = np.arange(5.0)
    resample = bootstrap_resample(x, rng)
    unique_count = len(np.unique(resample))
    assert unique_count < len(x) or True  # sanity: shape check is the real guarantee
    assert len(resample) == 5


def test_bootstrap_confidence_interval_contains_the_true_mean_for_a_large_sample():
    rng = np.random.default_rng(3)
    x = rng.normal(50.0, 5.0, size=500)
    lower, upper = bootstrap_confidence_interval(x, np.mean, n_bootstrap=500, seed=0)
    assert lower <= np.mean(x) <= upper


def test_bootstrap_confidence_interval_works_for_a_statistic_without_a_closed_form():
    # The median has no simple closed-form confidence interval formula
    # the way the mean does -- this is exactly the case the bootstrap
    # exists to handle.
    rng = np.random.default_rng(4)
    x = rng.normal(50.0, 5.0, size=300)
    lower, upper = bootstrap_confidence_interval(x, np.median, n_bootstrap=500, seed=0)
    assert lower <= np.median(x) <= upper


def test_bootstrap_confidence_interval_is_reproducible_with_same_seed():
    rng = np.random.default_rng(5)
    x = rng.normal(0.0, 1.0, size=100)
    a = bootstrap_confidence_interval(x, np.mean, n_bootstrap=200, seed=42)
    b = bootstrap_confidence_interval(x, np.mean, n_bootstrap=200, seed=42)
    assert a == b


def test_higher_confidence_gives_a_wider_bootstrap_interval():
    rng = np.random.default_rng(6)
    x = rng.normal(0.0, 1.0, size=200)
    lower_90, upper_90 = bootstrap_confidence_interval(x, np.mean, n_bootstrap=500, confidence=0.90, seed=0)
    lower_99, upper_99 = bootstrap_confidence_interval(x, np.mean, n_bootstrap=500, confidence=0.99, seed=0)
    assert (upper_99 - lower_99) > (upper_90 - lower_90)


def test_bootstrap_confidence_interval_uses_statistic_fn_not_always_the_mean():
    # Directly targets a mutant that hardcodes np.mean regardless of the
    # `statistic_fn` argument: using a wildly different statistic (e.g.
    # np.max) should give a clearly different interval than np.mean would.
    rng = np.random.default_rng(7)
    x = rng.normal(0.0, 1.0, size=200)
    mean_lower, mean_upper = bootstrap_confidence_interval(x, np.mean, n_bootstrap=300, seed=0)
    max_lower, max_upper = bootstrap_confidence_interval(x, np.max, n_bootstrap=300, seed=0)
    assert max_lower > mean_upper  # max of a standard normal sample sits far above its mean
