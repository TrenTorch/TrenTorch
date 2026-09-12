"""
pytest data/app_data/01-classical-ml/04-ensembles/01-random-forest-majority-vote/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

random_forest_predict = load_solution(
    f"01-classical-ml/04-ensembles/{Path(__file__).resolve().parent.name}"
).random_forest_predict


def _leaf(prediction: int) -> dict:
    return {"leaf": True, "prediction": prediction}


def test_unanimous_vote():
    trees = [_leaf(1), _leaf(1), _leaf(1)]
    input = np.array([[0.0], [0.0]])
    result = random_forest_predict(trees, input)
    assert np.array_equal(result, [1, 1])


def test_clear_majority_wins():
    trees = [_leaf(0), _leaf(1), _leaf(1)]
    input = np.array([[0.0]])
    result = random_forest_predict(trees, input)
    assert result[0] == 1


def test_tie_breaks_to_lower_class_label():
    trees = [_leaf(0), _leaf(1)]
    input = np.array([[0.0]])
    result = random_forest_predict(trees, input)
    assert result[0] == 0


def test_per_sample_votes_are_independent():
    # Trees that split on the input feature, so different samples get
    # genuinely different vote distributions -- catches a bug that
    # accidentally votes globally instead of per sample.
    trees = [
        {"leaf": False, "feature": 0, "threshold": 0.0,
         "left": _leaf(0), "right": _leaf(1)},
        {"leaf": False, "feature": 0, "threshold": 0.0,
         "left": _leaf(0), "right": _leaf(1)},
        _leaf(1),
    ]
    input = np.array([[-5.0], [5.0]])
    result = random_forest_predict(trees, input)
    # sample 0 (x=-5): votes [0, 0, 1] -> majority 0
    # sample 1 (x=5):  votes [1, 1, 1] -> majority 1
    assert np.array_equal(result, [0, 1])


def test_single_tree_forest_matches_that_tree_exactly():
    tree = {
        "leaf": False, "feature": 0, "threshold": 2.5,
        "left": _leaf(0), "right": _leaf(1),
    }
    input = np.array([[1.0], [2.0], [3.0], [4.0]])
    result = random_forest_predict([tree], input)
    assert np.array_equal(result, [0, 0, 1, 1])


def test_larger_odd_forest_matches_manual_vote_count():
    rng = np.random.default_rng(0)
    thresholds = rng.normal(size=11)
    trees = [
        {"leaf": False, "feature": 0, "threshold": t, "left": _leaf(0), "right": _leaf(1)}
        for t in thresholds
    ]
    input = np.array([[0.3], [-1.2]])
    result = random_forest_predict(trees, input)
    for col in range(input.shape[0]):
        votes = [1 if input[col, 0] > t else 0 for t in thresholds]
        expected = 1 if votes.count(1) > votes.count(0) else 0
        assert result[col] == expected
