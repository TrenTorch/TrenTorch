"""
pytest data/app_data/01-classical-ml/02-classification/11-distribution-shift-detection/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}")
bin_proportions = _module.bin_proportions
population_stability_index = _module.population_stability_index
detect_distribution_shift = _module.detect_distribution_shift


def test_bin_proportions_sums_to_one():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])
    bin_edges = np.array([-np.inf, 3.0, np.inf])
    result = bin_proportions(values, bin_edges)
    assert np.isclose(result.sum(), 1.0)


def test_bin_proportions_matches_hand_computation():
    values = np.array([1.0, 1.0, 5.0, 5.0, 5.0])
    bin_edges = np.array([-np.inf, 3.0, np.inf])
    result = bin_proportions(values, bin_edges)
    assert np.allclose(result, [0.4, 0.6])


def test_psi_is_near_zero_for_identical_distributions():
    rng = np.random.default_rng(0)
    train = rng.normal(50.0, 10.0, size=5000)
    live = rng.normal(50.0, 10.0, size=2000)
    psi = population_stability_index(train, live)
    assert psi < 0.05


def test_psi_is_large_for_a_dramatically_shifted_distribution():
    rng = np.random.default_rng(1)
    train = rng.normal(50.0, 10.0, size=5000)
    live = rng.normal(90.0, 20.0, size=2000)  # dramatically shifted mean and spread
    psi = population_stability_index(train, live)
    assert psi > 0.5


def test_psi_is_never_negative():
    rng = np.random.default_rng(2)
    train = rng.normal(0.0, 1.0, size=1000)
    live = rng.normal(0.5, 1.5, size=500)
    assert population_stability_index(train, live) >= 0.0


def test_psi_increases_monotonically_with_shift_magnitude():
    rng = np.random.default_rng(3)
    train = rng.normal(0.0, 1.0, size=5000)
    small_shift = rng.normal(0.5, 1.0, size=2000)
    large_shift = rng.normal(3.0, 1.0, size=2000)
    psi_small = population_stability_index(train, small_shift)
    psi_large = population_stability_index(train, large_shift)
    assert psi_large > psi_small


def test_detect_distribution_shift_flags_a_real_shift():
    rng = np.random.default_rng(4)
    train = rng.normal(50.0, 10.0, size=5000)
    shifted_live = rng.normal(90.0, 20.0, size=2000)
    assert detect_distribution_shift(train, shifted_live) is True


def test_detect_distribution_shift_does_not_flag_matching_distributions():
    rng = np.random.default_rng(5)
    train = rng.normal(50.0, 10.0, size=5000)
    same_live = rng.normal(50.0, 10.0, size=2000)
    assert detect_distribution_shift(train, same_live) is False


def test_psi_does_not_confuse_the_direction_of_the_ratio():
    # Directly targets a mutant that swaps train_pct and live_pct inside
    # the log term (e.g. log(train_pct/live_pct) instead of
    # log(live_pct/train_pct)): PSI's formula is actually symmetric in
    # its final value (the (a-b)*log(a/b) form is invariant to swapping
    # a and b), but a mutant that swaps only ONE of the two occurrences
    # (the subtraction order OR the log ratio, not both) breaks that
    # symmetry and produces a negative PSI, which should never happen.
    rng = np.random.default_rng(6)
    train = rng.normal(0.0, 1.0, size=3000)
    live = rng.normal(2.0, 1.0, size=1500)
    psi = population_stability_index(train, live)
    assert psi > 0.0
