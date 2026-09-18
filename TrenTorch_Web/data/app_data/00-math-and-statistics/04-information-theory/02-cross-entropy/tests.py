"""
pytest data/app_data/00-math-and-statistics/04-information-theory/02-cross-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-math-and-statistics/04-information-theory/{Path(__file__).resolve().parent.name}")
cross_entropy = _module.cross_entropy

entropy = load_solution("00-math-and-statistics/04-information-theory/01-entropy").entropy


def test_cross_entropy_of_p_with_itself_equals_entropy():
    p = np.array([0.5, 0.3, 0.2])
    assert np.isclose(cross_entropy(p, p), entropy(p))


def test_cross_entropy_matches_hand_computation():
    p = np.array([1.0, 0.0])  # one-hot: true class is index 0
    q = np.array([0.25, 0.75])
    # H(p, q) = -1*log2(0.25) - 0*log2(0.75) = 2.0
    assert np.isclose(cross_entropy(p, q), 2.0)


def test_cross_entropy_is_never_less_than_entropy():
    # Gibbs' inequality: H(p, q) >= H(p), with equality iff p == q.
    rng = np.random.default_rng(0)
    p_raw = rng.uniform(size=5)
    p = p_raw / p_raw.sum()
    q_raw = rng.uniform(size=5)
    q = q_raw / q_raw.sum()
    assert cross_entropy(p, q) >= entropy(p) - 1e-9


def test_cross_entropy_penalizes_confident_wrong_predictions_heavily():
    p = np.array([1.0, 0.0])  # true class: 0
    confident_correct = np.array([0.99, 0.01])
    confident_wrong = np.array([0.01, 0.99])
    assert cross_entropy(p, confident_wrong) > cross_entropy(p, confident_correct)


def test_cross_entropy_does_not_crash_on_zero_predicted_probability():
    p = np.array([1.0, 0.0])
    q = np.array([1e-15, 1.0 - 1e-15])
    result = cross_entropy(p, q)
    assert np.isfinite(result)
    assert result > 0.0


def test_cross_entropy_uses_log_of_q_not_log_of_p():
    # Directly targets a mutant that computes 01-entropy's formula
    # verbatim (taking log(p) instead of log(q)), silently ignoring the
    # predicted distribution entirely. With a very different q than p,
    # this produces a clearly wrong (too-small) result.
    p = np.array([1.0, 0.0])
    q = np.array([0.01, 0.99])  # model is confidently WRONG about class 0
    result = cross_entropy(p, q)
    entropy_of_p_alone = entropy(p)
    assert result > entropy_of_p_alone + 1.0  # should reflect the bad prediction
    assert not np.isclose(result, entropy_of_p_alone)
