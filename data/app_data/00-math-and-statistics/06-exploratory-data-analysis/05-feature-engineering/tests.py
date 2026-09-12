"""
pytest data/app_data/00-math-and-statistics/06-exploratory-data-analysis/05-feature-engineering/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/06-exploratory-data-analysis/{Path(__file__).resolve().parent.name}"
)
radius_feature = _module.radius_feature
ratio_feature = _module.ratio_feature

correlation = load_solution("00-math-and-statistics/03-probability/03-covariance-correlation").correlation


def test_radius_feature_matches_hand_computation():
    # classic 3-4-5 triangle
    x = np.array([3.0])
    y = np.array([4.0])
    assert np.isclose(radius_feature(x, y)[0], 5.0)


def test_radius_feature_at_origin_is_zero():
    assert np.isclose(radius_feature(np.array([0.0]), np.array([0.0]))[0], 0.0)


def test_radius_feature_is_never_negative():
    rng = np.random.default_rng(0)
    x = rng.normal(size=20)
    y = rng.normal(size=20)
    assert np.all(radius_feature(x, y) >= 0.0)


def test_ratio_feature_matches_hand_computation():
    numerator = np.array([10.0, 20.0, 30.0])
    denominator = np.array([2.0, 4.0, 5.0])
    assert np.allclose(ratio_feature(numerator, denominator), [5.0, 5.0, 6.0])


def test_radius_feature_dramatically_more_correlated_with_a_circular_label_than_raw_coordinates():
    # The core demonstration this question exists to make concrete: for
    # a label determined by "inside a circle", raw x/y are nearly
    # useless individually, but the engineered radius feature is
    # strongly correlated with the label.
    rng = np.random.default_rng(1)
    x = rng.uniform(-5.0, 5.0, size=500)
    y = rng.uniform(-5.0, 5.0, size=500)
    label = (radius_feature(x, y) < 3.0).astype(float)

    corr_x = abs(correlation(x, label))
    corr_y = abs(correlation(y, label))
    corr_radius = abs(correlation(radius_feature(x, y), label))

    assert corr_radius > 0.5
    assert corr_radius > corr_x * 3
    assert corr_radius > corr_y * 3


def test_radius_feature_uses_sum_of_squares_not_sum():
    # Directly targets a mutant that computes sqrt(x + y) instead of
    # sqrt(x^2 + y^2): for negative coordinates, sqrt(x + y) can be
    # undefined (negative under the root) while the true radius never is.
    x = np.array([-3.0])
    y = np.array([-4.0])
    result = radius_feature(x, y)
    assert np.isclose(result[0], 5.0)
    assert result[0] >= 0.0


def test_ratio_feature_divides_not_subtracts():
    # Directly targets a mutant that computes numerator - denominator
    # instead of numerator / denominator.
    numerator = np.array([100.0])
    denominator = np.array([4.0])
    result = ratio_feature(numerator, denominator)
    assert np.isclose(result[0], 25.0)
    assert not np.isclose(result[0], 96.0)
