"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
average_nll = _module.average_nll

ITOS = [".", "a", "b"]


def test_1_hand_computed():
    probs = np.array([[0.0, 0.5, 0.5], [0.25, 0.25, 0.5], [0.5, 0.25, 0.25]])
    # word "ab": .a (0.5), ab (0.5), b. (0.5)
    assert np.isclose(average_nll(["ab"], probs, ITOS), -np.log(0.5))


def test_2_uniform_model_scores_ln_v():
    probs = np.full((3, 3), 1 / 3)
    assert np.isclose(average_nll(["ab", "ba", "aab"], probs, ITOS), np.log(3))


def test_3_better_model_scores_lower():
    uniform = np.full((3, 3), 1 / 3)
    peaked = np.array([[0.0, 0.9, 0.1], [0.1, 0.1, 0.8], [0.8, 0.1, 0.1]]) + 1e-12
    peaked = peaked / peaked.sum(axis=1, keepdims=True)
    # "ab" is exactly what the peaked model expects
    assert average_nll(["ab"], peaked, ITOS) < average_nll(["ab"], uniform, ITOS)


def test_4_mean_over_all_pairs_not_over_words():
    probs = np.array([[0.1, 0.6, 0.3], [0.2, 0.2, 0.6], [0.5, 0.25, 0.25]])
    words = ["a", "bab"]
    pairs = [(0, 1), (1, 0), (0, 2), (2, 1), (1, 2), (2, 0)]
    expected = np.mean([-np.log(probs[i, j]) for i, j in pairs])
    assert np.isclose(average_nll(words, probs, ITOS), expected)


def test_5_zero_probability_gives_infinity():
    probs = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0]])
    assert np.isinf(average_nll(["b"], probs, ITOS))


def test_6_returns_python_float_and_does_not_mutate():
    probs = np.full((3, 3), 1 / 3)
    snapshot = probs.copy()
    out = average_nll(["ab"], probs, ITOS)
    assert isinstance(out, float)
    assert np.array_equal(probs, snapshot)
