"""
pytest data/app_data/01-classical-ml/07-evaluation/10-calibration/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
reliability_diagram = _module.reliability_diagram
expected_calibration_error = _module.expected_calibration_error


def test_reliability_diagram_matches_hand_computation():
    # 2 bins: [0, 0.5), [0.5, 1.0]
    probabilities = np.array([0.1, 0.2, 0.8, 0.9])
    labels = np.array([0, 1, 1, 1])
    confidences, accuracies, counts = reliability_diagram(labels, probabilities, n_bins=2)
    assert counts[0] == 2 and counts[1] == 2
    assert np.isclose(confidences[0], 0.15)  # mean(0.1, 0.2)
    assert np.isclose(confidences[1], 0.85)  # mean(0.8, 0.9)
    assert np.isclose(accuracies[0], 0.5)  # mean(0, 1)
    assert np.isclose(accuracies[1], 1.0)  # mean(1, 1)


def test_probability_of_exactly_one_falls_in_the_last_bin():
    probabilities = np.array([1.0])
    labels = np.array([1])
    _, _, counts = reliability_diagram(labels, probabilities, n_bins=10)
    assert counts[-1] == 1
    assert counts.sum() == 1


def test_empty_bins_have_zero_count_and_do_not_crash():
    probabilities = np.array([0.05, 0.05, 0.95])  # nothing in the middle bins
    labels = np.array([0, 1, 1])
    confidences, accuracies, counts = reliability_diagram(labels, probabilities, n_bins=10)
    assert counts[4] == 0
    assert confidences[4] == 0.0
    assert accuracies[4] == 0.0


def test_perfectly_calibrated_model_has_zero_ece():
    rng = np.random.default_rng(0)
    n = 10000
    probabilities = rng.random(n)
    labels = (rng.random(n) < probabilities).astype(int)  # genuinely matches its own probabilities
    ece = expected_calibration_error(labels, probabilities, n_bins=10)
    assert ece < 0.02  # small sampling noise only


def test_badly_overconfident_model_has_high_ece():
    # Always predicts 0.9, but only ~10% are actually positive.
    rng = np.random.default_rng(1)
    n = 1000
    probabilities = np.full(n, 0.9)
    labels = (rng.random(n) < 0.1).astype(int)
    ece = expected_calibration_error(labels, probabilities, n_bins=10)
    assert ece > 0.7


def test_confidence_and_accuracy_are_not_swapped():
    # Directly targets a mutant that swaps which array gets
    # probabilities.mean() vs labels.mean(): a heavily skewed single
    # bin makes the two clearly different and distinguishable.
    probabilities = np.array([0.95, 0.95, 0.95, 0.95])  # all confidently predict positive
    labels = np.array([0, 0, 0, 1])  # but only 25% actually are
    confidences, accuracies, _ = reliability_diagram(labels, probabilities, n_bins=10)
    bin_idx = int(0.95 * 10)  # which bin 0.95 falls in
    assert np.isclose(confidences[bin_idx], 0.95)
    assert np.isclose(accuracies[bin_idx], 0.25)


def test_matches_real_sklearn_calibration_curve_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(0)
    #   probs = rng.random(200)
    #   labels = (rng.random(200) < probs**1.5).astype(int)
    #   sklearn.calibration.calibration_curve(labels, probs, n_bins=10, strategy='uniform')
    #   # accuracies and confidences baked below (all 10 bins non-empty
    #   # for this dataset)
    #
    # This test needs no scikit-learn installed to run.
    rng = np.random.default_rng(0)
    probabilities = rng.random(200)
    labels = (rng.random(200) < probabilities**1.5).astype(int)

    expected_confidences = np.array(
        [0.04410997, 0.15215764, 0.25986634, 0.35396752, 0.44486072, 0.55491959,
         0.64571727, 0.74473642, 0.84947348, 0.95182609]
    )
    expected_accuracies = np.array(
        [0.0, 0.0625, 0.0625, 0.11764706, 0.11111111, 0.5, 0.47058824, 0.77777778, 0.72, 0.96666667]
    )

    confidences, accuracies, counts = reliability_diagram(labels, probabilities, n_bins=10)
    assert np.all(counts > 0)
    assert np.allclose(confidences, expected_confidences, atol=1e-6)
    assert np.allclose(accuracies, expected_accuracies, atol=1e-6)
