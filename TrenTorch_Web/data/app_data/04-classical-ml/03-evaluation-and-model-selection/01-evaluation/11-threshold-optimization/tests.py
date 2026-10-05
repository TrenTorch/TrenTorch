"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
f1_metric = _module.f1_metric
optimize_threshold = _module.optimize_threshold
precision_recall_f1 = load_solution("evaluation-classification-metrics").precision_recall_f1


def test_f1_metric_matches_precision_recall_f1():
    labels = np.array([1, 1, 0, 0])
    predictions = np.array([1, 0, 0, 1])
    _, _, expected_f1 = precision_recall_f1(labels, predictions)
    assert np.isclose(f1_metric(labels, predictions), expected_f1)


def test_optimize_threshold_finds_the_perfectly_separating_threshold():
    labels = np.array([0, 0, 1, 1])
    scores = np.array([0.1, 0.2, 0.8, 0.9])
    best_threshold, best_score = optimize_threshold(labels, scores)
    assert np.isclose(best_score, 1.0)
    assert 0.2 < best_threshold <= 0.8


def test_optimize_threshold_works_with_a_custom_metric():
    def accuracy(labels, predictions):
        return float(np.mean(labels == predictions))

    labels = np.array([0, 0, 0, 1])
    scores = np.array([0.1, 0.3, 0.6, 0.4])
    best_threshold, best_score = optimize_threshold(labels, scores, metric_fn=accuracy)
    predictions = (scores >= best_threshold).astype(int)
    assert np.isclose(best_score, np.mean(labels == predictions))
    assert best_score >= 0.75  # at least 3 of 4 correct is achievable here


def test_optimizing_the_threshold_improves_f1_on_imbalanced_data():
    # The actual point of the exercise: on genuinely imbalanced data,
    # the default threshold of 0.5 is rarely optimal.
    rng = np.random.default_rng(0)
    n = 1000
    labels = (rng.random(n) < 0.05).astype(int)
    scores = np.clip(labels * 0.3 + rng.normal(scale=0.2, size=n) + 0.1, 0, 1)

    default_predictions = (scores >= 0.5).astype(int)
    default_f1 = f1_metric(labels, default_predictions)
    _, optimized_f1 = optimize_threshold(labels, scores)

    assert optimized_f1 > default_f1


def test_optimize_threshold_picks_the_maximum_not_the_minimum():
    # Directly targets a mutant that keeps the worst-scoring threshold
    # instead of the best.
    scores = np.array([0.1, 0.5, 0.9])
    labels = np.array([0, 0, 1])

    def scripted_metric(_labels, predictions):
        # score depends only on how many are predicted positive, chosen
        # so there's one clear best and one clear worst threshold
        return {0: 0.1, 1: 0.9, 2: 0.05, 3: 0.05}[int(predictions.sum())]

    best_threshold, best_score = optimize_threshold(labels, scores, metric_fn=scripted_metric)
    assert np.isclose(best_score, 0.9)
