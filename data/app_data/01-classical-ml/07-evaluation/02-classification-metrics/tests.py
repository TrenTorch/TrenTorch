"""
pytest data/app_data/01-classical-ml/07-evaluation/02-classification-metrics/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
precision_recall_f1 = _module.precision_recall_f1
roc_curve = _module.roc_curve
auc = _module.auc


def test_precision_recall_f1_matches_hand_computation():
    # TP=2 (idx 0,2), FP=1 (idx 3), FN=1 (idx 1)
    labels = np.array([1, 1, 1, 0])
    predictions = np.array([1, 0, 1, 1])
    precision, recall, f1 = precision_recall_f1(labels, predictions)
    assert np.isclose(precision, 2 / 3)
    assert np.isclose(recall, 2 / 3)
    assert np.isclose(f1, 2 / 3)


def test_precision_is_zero_when_no_positive_predictions():
    labels = np.array([1, 0, 1])
    predictions = np.array([0, 0, 0])
    precision, recall, f1 = precision_recall_f1(labels, predictions)
    assert precision == 0.0
    assert recall == 0.0


def test_perfect_predictions_give_precision_recall_f1_of_one():
    labels = np.array([1, 0, 1, 0])
    predictions = np.array([1, 0, 1, 0])
    precision, recall, f1 = precision_recall_f1(labels, predictions)
    assert precision == 1.0 and recall == 1.0 and f1 == 1.0


def test_precision_and_recall_are_not_swapped():
    # Directly targets a mutant that swaps the two formulas: many false
    # positives, zero false negatives -- precision should be LOW,
    # recall should be HIGH (perfectly distinguishable from the swap).
    labels = np.array([1, 0, 0, 0, 0])
    predictions = np.array([1, 1, 1, 1, 1])
    precision, recall, _ = precision_recall_f1(labels, predictions)
    assert recall == 1.0
    assert precision < 0.5


def test_roc_curve_endpoints():
    labels = np.array([1, 0, 1, 0])
    scores = np.array([0.9, 0.6, 0.3, 0.1])
    fpr, tpr, thresholds = roc_curve(labels, scores)
    assert thresholds[0] == np.inf
    assert fpr[0] == 0.0 and tpr[0] == 0.0  # nothing predicted positive
    assert fpr[-1] == 1.0 and tpr[-1] == 1.0  # everything predicted positive


def test_auc_of_perfect_separation_is_one():
    labels = np.array([1, 1, 1, 0, 0, 0])
    scores = np.array([0.9, 0.8, 0.7, 0.3, 0.2, 0.1])
    fpr, tpr, _ = roc_curve(labels, scores)
    assert np.isclose(auc(fpr, tpr), 1.0)


def test_auc_of_perfectly_wrong_order_is_zero():
    labels = np.array([1, 1, 1, 0, 0, 0])
    scores = np.array([0.1, 0.2, 0.3, 0.7, 0.8, 0.9])  # exactly backwards
    fpr, tpr, _ = roc_curve(labels, scores)
    assert np.isclose(auc(fpr, tpr), 0.0)


def test_matches_real_sklearn_roc_curve_and_auc_on_a_baked_dataset():
    # Ground truth from the actual library, not our own derivation.
    #
    # Generated once, offline, with:
    #   rng = np.random.default_rng(0)
    #   labels = rng.integers(0, 2, 50)
    #   scores = rng.random(50)
    #   sklearn.metrics.roc_curve(labels, scores, drop_intermediate=False)
    #   sklearn.metrics.roc_auc_score(labels, scores)  # == 0.500805152979066
    #
    # This test needs no scikit-learn installed to run.
    rng = np.random.default_rng(0)
    labels = rng.integers(0, 2, 50)
    scores = rng.random(50)
    fpr, tpr, _ = roc_curve(labels, scores)
    assert np.isclose(auc(fpr, tpr), 0.500805152979066, atol=1e-9)
