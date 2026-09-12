"""
pytest data/app_data/01-classical-ml/04-support-vector-machines/02-margin-maximization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/04-support-vector-machines/{Path(__file__).resolve().parent.name}")
functional_margin = _module.functional_margin
geometric_margin = _module.geometric_margin
dataset_margin = _module.dataset_margin


def test_functional_margin_matches_hand_computation():
    weight = np.array([1.0, 0.0])
    bias = 0.0
    x = np.array([[2.0, 0.0], [-2.0, 0.0]])
    y = np.array([1.0, -1.0])
    result = functional_margin(weight, bias, x, y)
    assert np.allclose(result, [2.0, 2.0])


def test_functional_margin_is_negative_for_misclassified_points():
    weight = np.array([1.0, 0.0])
    bias = 0.0
    x = np.array([[2.0, 0.0]])
    y = np.array([-1.0])  # wrong label for a point on the positive side
    result = functional_margin(weight, bias, x, y)
    assert result[0] < 0.0


def test_geometric_margin_matches_hand_computation():
    weight = np.array([3.0, 4.0])  # ||weight|| = 5
    bias = 0.0
    x = np.array([[5.0, 0.0]])
    y = np.array([1.0])
    # functional margin = 1*(3*5 + 4*0 + 0) = 15, geometric = 15/5 = 3
    result = geometric_margin(weight, bias, x, y)
    assert np.isclose(result[0], 3.0)


def test_geometric_margin_is_invariant_to_scaling_weight_and_bias():
    rng = np.random.default_rng(0)
    weight = rng.normal(size=3)
    bias = 0.5
    x = rng.normal(size=(10, 3))
    y = np.sign(x @ weight + bias)
    y[y == 0] = 1.0

    original = geometric_margin(weight, bias, x, y)
    scaled = geometric_margin(weight * 7.0, bias * 7.0, x, y)
    assert np.allclose(original, scaled, atol=1e-8)


def test_functional_margin_is_not_scale_invariant_unlike_geometric():
    weight = np.array([1.0, 0.0])
    bias = 0.0
    x = np.array([[2.0, 0.0]])
    y = np.array([1.0])
    original = functional_margin(weight, bias, x, y)
    scaled = functional_margin(weight * 10.0, bias * 10.0, x, y)
    assert not np.isclose(original[0], scaled[0])
    assert np.isclose(scaled[0], original[0] * 10.0)


def test_dataset_margin_returns_the_minimum_across_points():
    weight = np.array([1.0, 0.0])
    bias = 0.0
    x = np.array([[2.0, 0.0], [-2.0, 0.0], [5.0, 0.0]])
    y = np.array([1.0, -1.0, 1.0])
    result = dataset_margin(weight, bias, x, y)
    assert np.isclose(result, 2.0)


def test_dataset_margin_is_a_plain_scalar():
    weight = np.array([1.0, 1.0])
    bias = 0.0
    x = np.array([[1.0, 1.0], [-1.0, -1.0]])
    y = np.array([1.0, -1.0])
    result = dataset_margin(weight, bias, x, y)
    assert isinstance(result, float)


def test_dataset_margin_does_not_use_max_instead_of_min():
    # Directly targets a mutant that takes the MAX geometric margin
    # instead of the MIN: the dataset margin is defined by the closest
    # (hardest) point, not the farthest (easiest) one.
    weight = np.array([1.0, 0.0])
    bias = 0.0
    x = np.array([[1.0, 0.0], [10.0, 0.0]])
    y = np.array([1.0, 1.0])
    result = dataset_margin(weight, bias, x, y)
    assert np.isclose(result, 1.0)  # the closer point's margin
    assert not np.isclose(result, 10.0)  # not the farther point's margin
