"""
pytest data/app_data/11-production-ml/03-monitoring-and-drift/01-data-drift-psi/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"11-production-ml/03-monitoring-and-drift/{Path(__file__).resolve().parent.name}")
bin_distribution = _module.bin_distribution
population_stability_index = _module.population_stability_index
detect_data_drift = _module.detect_data_drift


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_identical_distributions_have_near_zero_psi():
    rng = np.random.default_rng(0)
    baseline = rng.normal(0, 1, 3000)
    same = rng.normal(0, 1, 3000)
    edges = np.linspace(-4, 4, 9)
    psi = population_stability_index(bin_distribution(baseline, edges), bin_distribution(same, edges))
    assert psi < 0.05


def test_02_genuinely_shifted_distribution_has_high_psi():
    rng = np.random.default_rng(1)
    baseline = rng.normal(0, 1, 3000)
    shifted = rng.normal(3, 1, 3000)
    edges = np.linspace(-4, 8, 13)
    psi = population_stability_index(bin_distribution(baseline, edges), bin_distribution(shifted, edges))
    assert psi > 0.25


# --- General-case coverage --------------------------------------------


def test_03_bin_distribution_sums_to_one():
    rng = np.random.default_rng(2)
    samples = rng.normal(0, 1, 1000)
    edges = np.linspace(-4, 4, 9)
    binned = bin_distribution(samples, edges)
    assert np.isclose(binned.sum(), 1.0)


def test_04_larger_shift_gives_larger_psi():
    rng = np.random.default_rng(3)
    baseline = rng.normal(0, 1, 3000)
    edges = np.linspace(-4, 10, 15)
    small_shift = bin_distribution(rng.normal(0.5, 1, 3000), edges)
    large_shift = bin_distribution(rng.normal(4, 1, 3000), edges)
    expected = bin_distribution(baseline, edges)
    assert population_stability_index(expected, small_shift) < population_stability_index(expected, large_shift)


def test_05_detect_data_drift_matches_the_threshold():
    assert detect_data_drift(0.3, threshold=0.2) is True
    assert detect_data_drift(0.1, threshold=0.2) is False


# --- Parameter handling -------------------------------------------------


def test_06_psi_is_zero_for_identical_already_normalized_arrays():
    dist = np.array([0.25, 0.25, 0.25, 0.25])
    assert np.isclose(population_stability_index(dist, dist), 0.0)


def test_07_empty_bins_do_not_produce_nan_or_inf():
    samples = np.array([1.0, 1.0, 1.0])  # all in one bin, others empty
    edges = np.linspace(0, 4, 5)
    binned = bin_distribution(samples, edges)
    assert np.all(np.isfinite(binned))


# --- Edge cases ---------------------------------------------------------


def test_08_threshold_boundary_is_exclusive():
    assert detect_data_drift(0.2, threshold=0.2) is False


def test_09_single_bin_distribution():
    samples = np.array([1.0, 2.0, 3.0])
    edges = np.array([0.0, 10.0])
    binned = bin_distribution(samples, edges)
    assert np.isclose(binned.sum(), 1.0)
    assert binned.shape == (1,)


# --- Independent correctness oracle -----------------------------------


def test_10_psi_computed_from_actual_bin_proportions_not_raw_counts():
    # Directly targets a mutant that forgets to normalize bin
    # proportions (using raw counts instead), which would make PSI
    # incorrectly sensitive to sample SIZE rather than distribution
    # SHAPE -- two differently-sized samples from the SAME true
    # distribution should still give a near-zero PSI.
    rng = np.random.default_rng(4)
    dist_a = rng.normal(0, 1, 2000)
    dist_b = rng.normal(0, 1, 8000)  # 4x more samples, same true distribution
    edges = np.linspace(-4, 4, 9)
    psi = population_stability_index(bin_distribution(dist_a, edges), bin_distribution(dist_b, edges))
    assert psi < 0.05
