"""
pytest data/app_data/12-research-papers/05-unsupervised-and-representation-learning/07-moco/03-enqueue/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-moco-enqueue")
enqueue = _module.enqueue


import numpy as np


def test_1_queue_length_is_capped_at_k():
    out = enqueue(np.zeros((4, 2)), np.ones((3, 2)), 5)
    assert out.shape == (5, 2)


def test_2_newest_keys_are_at_the_end():
    out = enqueue(np.array([[1.0], [2.0]]), np.array([[3.0]]), 3)
    np.testing.assert_allclose(out[-1], [3.0])


def test_3_oldest_keys_are_dropped():
    out = enqueue(np.array([[1.0], [2.0]]), np.array([[3.0]]), 2)
    np.testing.assert_allclose(out, [[2.0], [3.0]])


def test_4_queue_below_capacity_grows():
    out = enqueue(np.array([[1.0]]), np.array([[2.0]]), 10)
    assert out.shape == (2, 1)


def test_5_keeps_the_feature_dimension():
    assert enqueue(np.zeros((2, 4)), np.ones((1, 4)), 3).shape[1] == 4


def test_6_does_not_mutate_the_queue():
    queue = np.array([[1.0], [2.0]])
    enqueue(queue, np.array([[3.0]]), 2)
    np.testing.assert_array_equal(queue, [[1.0], [2.0]])

