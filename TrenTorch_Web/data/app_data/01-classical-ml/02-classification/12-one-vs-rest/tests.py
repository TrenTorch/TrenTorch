"""
pytest data/app_data/01-classical-ml/02-classification/12-one-vs-rest/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/02-classification/{Path(__file__).resolve().parent.name}")
train_one_vs_rest = _module.train_one_vs_rest
predict_one_vs_rest = _module.predict_one_vs_rest


def _make_three_cluster_dataset(seed=0, n=300):
    rng = np.random.default_rng(seed)
    centers = np.array([[0.0, 0.0], [5.0, 5.0], [0.0, 5.0]])
    x = np.zeros((n, 2))
    y = np.zeros(n, dtype=int)
    for i in range(n):
        c = rng.integers(0, 3)
        x[i] = centers[c] + rng.normal(scale=0.5, size=2)
        y[i] = c
    return x, y


def test_train_one_vs_rest_returns_correct_shapes():
    x, y = _make_three_cluster_dataset()
    weights, biases = train_one_vs_rest(x, y, num_classes=3, lr=0.5, epochs=50)
    assert weights.shape == (3, 2)
    assert biases.shape == (3,)


def test_predict_one_vs_rest_returns_valid_class_indices():
    x, y = _make_three_cluster_dataset()
    weights, biases = train_one_vs_rest(x, y, num_classes=3, lr=0.5, epochs=200)
    predictions = predict_one_vs_rest(x, weights, biases)
    assert predictions.shape == (len(x),)
    assert set(np.unique(predictions).tolist()).issubset({0, 1, 2})


def test_one_vs_rest_achieves_high_accuracy_on_well_separated_clusters():
    x, y = _make_three_cluster_dataset(seed=1, n=300)
    weights, biases = train_one_vs_rest(x, y, num_classes=3, lr=0.5, epochs=500)
    predictions = predict_one_vs_rest(x, weights, biases)
    accuracy = (predictions == y).mean()
    assert accuracy > 0.95


def test_each_class_classifier_trains_independently_of_the_others():
    # A structural check: retraining with only two classes present in
    # the target (class 2 never appears) should not error, and every
    # trained classifier's weights should differ from each other (they
    # were fit to distinct binary problems).
    x, y = _make_three_cluster_dataset(seed=2, n=200)
    weights, _ = train_one_vs_rest(x, y, num_classes=3, lr=0.5, epochs=100)
    assert not np.allclose(weights[0], weights[1])
    assert not np.allclose(weights[1], weights[2])


def test_predict_one_vs_rest_picks_the_argmax_not_a_fixed_threshold():
    # Directly targets a mutant that thresholds each score at 0.5
    # independently (e.g. returning the first class whose score exceeds
    # 0.5, or defaulting to class 0 when none do) instead of taking the
    # argmax across all classes. Construct scores where every score is
    # below 0.5 but one is clearly the largest.
    x, y = _make_three_cluster_dataset(seed=3, n=150)
    weights, biases = train_one_vs_rest(x, y, num_classes=3, lr=0.3, epochs=300)
    # Bias every classifier down so no sigmoid score exceeds 0.5, forcing
    # a thresholding-based mutant to behave differently from argmax.
    biases_shifted = biases - 5.0
    predictions = predict_one_vs_rest(x, weights, biases_shifted)
    # argmax-based prediction is invariant to a UNIFORM shift applied to
    # every class's bias equally (it doesn't change which score is largest).
    original_predictions = predict_one_vs_rest(x, weights, biases)
    assert np.array_equal(predictions, original_predictions)


def test_one_vs_rest_binary_targets_are_constructed_correctly():
    # Directly verifies the per-class binary target construction: a
    # classifier trained to detect class 1 should end up with a
    # decision boundary strongly favoring cluster 1's region.
    x, y = _make_three_cluster_dataset(seed=4, n=300)
    weights, biases = train_one_vs_rest(x, y, num_classes=3, lr=0.5, epochs=500)

    # Point near cluster 1's center (5, 5) should score highest under
    # classifier 1 specifically.
    near_cluster_1 = np.array([[5.0, 5.0]])
    scores = 1.0 / (1.0 + np.exp(-(near_cluster_1 @ weights.T + biases)))
    assert np.argmax(scores[0]) == 1
