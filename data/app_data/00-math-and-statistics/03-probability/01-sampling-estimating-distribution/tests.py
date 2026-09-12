"""
pytest data/app_data/00-math-and-statistics/03-probability/01-sampling-estimating-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/03-probability/{Path(__file__).resolve().parent.name}")
sample_normal = _module.sample_normal
empirical_histogram = _module.empirical_histogram


def test_sample_normal_returns_correct_size():
    result = sample_normal(0.0, 1.0, 1000, seed=0)
    assert result.shape == (1000,)


def test_sample_normal_is_reproducible_with_same_seed():
    a = sample_normal(5.0, 2.0, 100, seed=42)
    b = sample_normal(5.0, 2.0, 100, seed=42)
    assert np.array_equal(a, b)


def test_sample_normal_differs_across_seeds():
    a = sample_normal(0.0, 1.0, 100, seed=1)
    b = sample_normal(0.0, 1.0, 100, seed=2)
    assert not np.array_equal(a, b)


def test_sample_normal_matches_target_mean_and_std_approximately():
    result = sample_normal(10.0, 3.0, 100_000, seed=0)
    assert np.isclose(np.mean(result), 10.0, atol=0.1)
    assert np.isclose(np.std(result), 3.0, atol=0.1)


def test_sample_normal_does_not_use_legacy_global_random_state():
    # Directly targets a mutant that uses np.random.seed + np.random.normal
    # (legacy global state) instead of a local generator: calling this
    # function should not perturb the global np.random state at all.
    np.random.seed(123)
    state_before = np.random.get_state()[1].copy()
    sample_normal(0.0, 1.0, 50, seed=99)
    state_after = np.random.get_state()[1]
    assert np.array_equal(state_before, state_after)


def test_empirical_histogram_counts_sum_to_sample_count():
    samples = np.array([1.0, 2.0, 2.5, 3.0, 5.0, 5.5, 9.0])
    counts, edges = empirical_histogram(samples, bins=4)
    assert counts.sum() == len(samples)


def test_empirical_histogram_bin_edges_length_is_bins_plus_one():
    samples = np.arange(20.0)
    counts, edges = empirical_histogram(samples, bins=5)
    assert len(counts) == 5
    assert len(edges) == 6


def test_empirical_histogram_matches_hand_computation():
    samples = np.array([0.0, 0.0, 1.0, 1.0, 1.0, 2.0])
    counts, edges = empirical_histogram(samples, bins=3)
    # 3 equal-width bins spanning [0, 2]: [0, 0.667), [0.667, 1.333), [1.333, 2]
    assert np.array_equal(counts, [2, 3, 1])


def test_empirical_histogram_of_normal_samples_peaks_near_the_mean():
    samples = sample_normal(0.0, 1.0, 10_000, seed=0)
    counts, edges = empirical_histogram(samples, bins=20)
    peak_bin_index = np.argmax(counts)
    peak_center = (edges[peak_bin_index] + edges[peak_bin_index + 1]) / 2
    assert abs(peak_center) < 0.5  # peak should land near 0, the true mean
