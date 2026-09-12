"""
pytest data/app_data/03-dl-training/04-regularization/03-label-smoothing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/04-regularization/{Path(__file__).resolve().parent.name}")
smooth_labels = _module.smooth_labels


def test_zero_smoothing_leaves_the_one_hot_vector_unchanged():
    one_hot = np.array([1.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.0, num_classes=3)
    assert np.allclose(result, one_hot)


def test_smoothed_vector_sums_to_one():
    one_hot = np.array([0.0, 1.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.1, num_classes=4)
    assert np.isclose(np.sum(result), 1.0)


def test_hand_computed_smoothing_example():
    one_hot = np.array([1.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.3, num_classes=3)
    # true class: (1 - 0.3) + 0.3/3 = 0.7 + 0.1 = 0.8
    # other classes: 0 + 0.3/3 = 0.1
    assert np.allclose(result, [0.8, 0.1, 0.1])


def test_every_previously_zero_class_gets_the_same_uniform_bump():
    one_hot = np.array([0.0, 0.0, 1.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.5, num_classes=5)
    # non-true classes should all be exactly smoothing / num_classes = 0.1
    assert np.isclose(result[0], 0.1)
    assert np.isclose(result[1], 0.1)
    assert np.isclose(result[3], 0.1)
    assert np.isclose(result[4], 0.1)


def test_true_class_value_matches_the_derived_formula():
    one_hot = np.array([0.0, 1.0])
    smoothing = 0.2
    num_classes = 2
    result = smooth_labels(one_hot, smoothing, num_classes)
    expected_true_class = (1.0 - smoothing) + smoothing / num_classes
    assert np.isclose(result[1], expected_true_class)


def test_smoothing_reduces_confidence_in_the_true_class():
    one_hot = np.array([1.0, 0.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.4, num_classes=4)
    assert result[0] < 1.0
    assert result[0] > 0.0


def test_high_smoothing_approaches_a_uniform_distribution():
    one_hot = np.array([1.0, 0.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=1.0, num_classes=4)
    # with smoothing=1, every entry should be exactly 1/num_classes
    assert np.allclose(result, [0.25, 0.25, 0.25, 0.25])


def test_works_on_a_batch_of_one_hot_vectors():
    batch = np.array([[1.0, 0.0], [0.0, 1.0]])
    result = smooth_labels(batch, smoothing=0.2, num_classes=2)
    assert result.shape == (2, 2)
    assert np.allclose(result.sum(axis=1), [1.0, 1.0])


def test_adds_uniform_bump_to_every_class_not_just_the_zero_entries():
    # Directly targets a mutant that only bumps up the ZERO entries and
    # leaves the true class at plain (1 - smoothing), forgetting the true
    # class ALSO receives the uniform smoothing/num_classes addition: this
    # breaks the "sums to exactly 1" property.
    one_hot = np.array([1.0, 0.0, 0.0])
    result = smooth_labels(one_hot, smoothing=0.3, num_classes=3)
    assert np.isclose(np.sum(result), 1.0)
    assert np.isclose(result[0], 0.8)
