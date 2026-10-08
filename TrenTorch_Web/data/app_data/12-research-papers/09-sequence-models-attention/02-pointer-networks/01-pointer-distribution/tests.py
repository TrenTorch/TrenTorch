"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/02-pointer-networks/01-pointer-distribution/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ptr-pointer-distribution")
pointer_distribution = _module.pointer_distribution


import numpy as np


def test_1_sums_to_one():
    assert abs(pointer_distribution(np.array([0.3, -1.0, 2.0])).sum() - 1.0) < 1e-12


def test_2_equal_scores_point_uniformly():
    np.testing.assert_allclose(pointer_distribution(np.zeros(4)), [0.25] * 4)


def test_3_highest_score_gets_most_mass():
    p = pointer_distribution(np.array([0.0, 3.0, 1.0]))
    assert np.argmax(p) == 1


def test_4_is_stable_for_large_scores():
    np.testing.assert_allclose(pointer_distribution(np.array([1000.0, 1000.0])), [0.5, 0.5])


def test_5_returns_one_entry_per_input():
    assert pointer_distribution(np.ones(6)).shape == (6,)


def test_6_does_not_mutate_scores():
    s = np.array([1.0, 2.0])
    pointer_distribution(s)
    np.testing.assert_array_equal(s, [1.0, 2.0])

