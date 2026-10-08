"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/03-deep-forest/01-class-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-deep-forest-class-distribution")
class_distribution = _module.class_distribution


import numpy as np


def test_1_matches_a_hand_value():
    np.testing.assert_allclose(class_distribution([0, 1, 1], 2), [1 / 3, 2 / 3])


def test_2_sums_to_one():
    assert abs(class_distribution([0, 2, 2, 1], 3).sum() - 1.0) < 1e-12


def test_3_absent_class_gets_zero():
    np.testing.assert_allclose(class_distribution([0, 0], 3), [1.0, 0.0, 0.0])


def test_4_output_length_is_n_classes():
    assert class_distribution([1], 5).shape == (5,)


def test_5_uniform_labels_give_uniform_distribution():
    np.testing.assert_allclose(class_distribution([0, 1, 2, 3], 4), [0.25] * 4)


def test_6_does_not_mutate_the_labels():
    labels = np.array([0, 1])
    class_distribution(labels, 2)
    np.testing.assert_array_equal(labels, [0, 1])

