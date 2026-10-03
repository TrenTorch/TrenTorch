"""
pytest tests.py
"""

import math

import numpy as np

from _load import load_solution

gain_ratio = load_solution(__file__).gain_ratio


def _h(labels):
    labels = list(labels)
    n = len(labels)
    total = 0.0
    for c in set(labels):
        p = labels.count(c) / n
        total -= p * math.log2(p)
    return total


def test_perfect_binary_split_has_ratio_one():
    feature = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    labels = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    assert np.isclose(gain_ratio(feature, labels), 1.0)


def test_id_like_feature_is_penalised():
    # Every sample gets its own value: gain = H(labels) = 1 bit, but the
    # intrinsic value is log2(8) = 3 bits, so the ratio is 1/3.
    feature = np.arange(8)
    labels = np.array([0, 1] * 4)
    assert np.isclose(gain_ratio(feature, labels), 1.0 / 3.0)


def test_prefers_compact_feature_over_id_feature():
    labels = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    compact = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    id_like = np.arange(8)
    assert gain_ratio(compact, labels) > gain_ratio(id_like, labels)


def test_constant_feature_is_zero():
    assert gain_ratio(np.array([3, 3, 3, 3]), np.array([0, 1, 0, 1])) == 0.0


def test_uninformative_feature_is_zero():
    feature = np.array([0, 0, 1, 1])
    labels = np.array([0, 1, 0, 1])
    assert np.isclose(gain_ratio(feature, labels), 0.0)


def test_empty_input_is_zero():
    assert gain_ratio(np.array([], dtype=int), np.array([], dtype=int)) == 0.0


def test_matches_independent_computation():
    rng = np.random.default_rng(0)
    for n_values in (2, 3, 4):
        feature = rng.integers(0, n_values, size=60)
        labels = rng.integers(0, 3, size=60)
        n = len(labels)
        gain = _h(labels)
        iv = 0.0
        for v in set(feature.tolist()):
            sub = labels[feature == v]
            w = len(sub) / n
            gain -= w * _h(sub)
            iv -= w * math.log2(w)
        assert np.isclose(gain_ratio(feature, labels), gain / iv)


def test_return_type_is_float():
    assert isinstance(gain_ratio(np.array([0, 1, 1]), np.array([0, 1, 1])), float)
