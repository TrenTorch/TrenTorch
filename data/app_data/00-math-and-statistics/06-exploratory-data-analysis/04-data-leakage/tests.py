"""
pytest data/app_data/00-math-and-statistics/06-exploratory-data-analysis/04-data-leakage/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/06-exploratory-data-analysis/{Path(__file__).resolve().parent.name}"
)
feature_target_correlations = _module.feature_target_correlations
find_suspicious_features = _module.find_suspicious_features


def test_feature_target_correlations_shape_matches_feature_count():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(50, 3))
    target = rng.normal(size=50)
    result = feature_target_correlations(x, target)
    assert result.shape == (3,)


def test_feature_target_correlations_matches_hand_computation():
    x = np.array([[1.0], [2.0], [3.0], [4.0]])
    target = np.array([2.0, 4.0, 6.0, 8.0])  # perfectly correlated
    result = feature_target_correlations(x, target)
    assert np.isclose(result[0], 1.0)


def test_find_suspicious_features_flags_an_almost_perfectly_correlated_feature():
    rng = np.random.default_rng(1)
    target = rng.integers(0, 2, size=200).astype(float)
    leaky_feature = target * 100.0 + rng.normal(scale=0.01, size=200)
    normal_feature = rng.normal(size=200)
    x = np.column_stack([normal_feature, leaky_feature])

    result = find_suspicious_features(x, target)
    assert list(result) == [1]


def test_find_suspicious_features_flags_nothing_when_no_feature_is_suspicious():
    rng = np.random.default_rng(2)
    x = rng.normal(size=(200, 3))
    target = rng.normal(size=200)  # unrelated to every feature
    result = find_suspicious_features(x, target)
    assert len(result) == 0


def test_find_suspicious_features_flags_strong_negative_correlation_too():
    rng = np.random.default_rng(3)
    target = rng.integers(0, 2, size=200).astype(float)
    leaky_feature = -target * 100.0 + rng.normal(scale=0.01, size=200)  # NEGATIVELY correlated
    x = leaky_feature.reshape(-1, 1)
    result = find_suspicious_features(x, target)
    assert list(result) == [0]


def test_find_suspicious_features_respects_custom_threshold():
    rng = np.random.default_rng(4)
    a = rng.normal(size=200)
    target = 0.5 * a + rng.normal(scale=0.9, size=200)  # moderately correlated, not leaky
    x = a.reshape(-1, 1)
    lenient = find_suspicious_features(x, target, threshold=0.3)
    strict = find_suspicious_features(x, target, threshold=0.99)
    assert len(lenient) >= len(strict)


def test_find_suspicious_features_returns_indices_not_a_boolean_mask():
    # Directly targets a mutant that returns the boolean condition array
    # itself instead of converting it to indices via np.where.
    rng = np.random.default_rng(5)
    target = rng.integers(0, 2, size=200).astype(float)
    leaky_feature = target * 100.0 + rng.normal(scale=0.01, size=200)
    x = leaky_feature.reshape(-1, 1)
    result = find_suspicious_features(x, target)
    assert result.dtype != bool
    assert result[0] == 0
