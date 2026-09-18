"""
pytest data/app_data/01-classical-ml/04-ensembles/08-histogram-boosting/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}")
build_histogram = _module.build_histogram
find_best_split_histogram = _module.find_best_split_histogram
find_best_split = load_solution(
    "01-classical-ml/03-decision-trees/03-best-split-minimal-tree"
).find_best_split


def test_build_histogram_matches_hand_computation():
    values = np.array([0.0, 3.0, 10.0])  # min=0, max=10
    edges = build_histogram(values, n_bins=5)
    assert np.allclose(edges, [0.0, 2.0, 4.0, 6.0, 8.0, 10.0])


def test_build_histogram_has_n_bins_plus_one_edges():
    values = np.array([1.0, 2.0, 3.0, 100.0])
    for n_bins in (2, 10, 50):
        assert build_histogram(values, n_bins).shape == (n_bins + 1,)


def test_find_best_split_histogram_finds_the_obvious_step():
    input = np.array([[1.0], [2.0], [3.0], [4.0], [5.0], [6.0], [7.0], [8.0]])
    labels = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    feature, threshold, gain = find_best_split_histogram(input, labels, n_bins=8)
    assert feature == 0
    assert 4.0 < threshold < 5.0
    assert gain > 0.0


def test_returns_none_for_a_pure_node():
    input = np.array([[1.0], [2.0], [3.0]])
    labels = np.array([1, 1, 1])
    assert find_best_split_histogram(input, labels, n_bins=4) is None


def test_candidate_threshold_count_does_not_grow_with_dataset_size():
    # The actual point of the exercise: information_gain gets called
    # exactly n_features * (n_bins - 1) times, regardless of whether
    # there are 20 rows or 20,000 unique values.
    call_counts = {}
    original_information_gain = _module.information_gain

    def counting_information_gain(*args, **kwargs):
        call_counts["n"] = call_counts.get("n", 0) + 1
        return original_information_gain(*args, **kwargs)

    _module.information_gain = counting_information_gain
    try:
        rng = np.random.default_rng(0)
        small_input = rng.normal(size=(50, 1))
        small_labels = rng.integers(0, 2, 50)
        call_counts["n"] = 0
        find_best_split_histogram(small_input, small_labels, n_bins=10)
        small_calls = call_counts["n"]

        large_input = rng.normal(size=(20_000, 1))  # many more unique values
        large_labels = rng.integers(0, 2, 20_000)
        call_counts["n"] = 0
        find_best_split_histogram(large_input, large_labels, n_bins=10)
        large_calls = call_counts["n"]
    finally:
        _module.information_gain = original_information_gain

    assert small_calls == large_calls == 9  # n_bins - 1, one feature


def test_matches_exact_search_reasonably_closely_with_enough_bins():
    # With enough bins, histogram search should land close to the same
    # threshold and gain the exact method finds -- not identical
    # (binning is inherently approximate), but in the right ballpark.
    rng = np.random.default_rng(1)
    input = rng.normal(size=(200, 1))
    labels = (input[:, 0] > 0.3).astype(int)

    exact_feature, exact_threshold, exact_gain = find_best_split(input, labels)
    hist_feature, hist_threshold, hist_gain = find_best_split_histogram(input, labels, n_bins=100)

    assert exact_feature == hist_feature
    assert abs(exact_threshold - hist_threshold) < 0.15
    assert abs(exact_gain - hist_gain) < 0.05
