"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/02-flashattention-2/01-deferred-normalization/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fa2-deferred-normalization")
finalize_output = _module.finalize_output


import numpy as np


def test_1_divides_each_row_by_its_denominator():
    np.testing.assert_allclose(finalize_output(np.array([[2.0, 4.0]]), np.array([2.0])), [[1.0, 2.0]])


def test_2_unit_denominator_keeps_the_accumulator():
    a = np.array([[3.0, 5.0]])
    np.testing.assert_allclose(finalize_output(a, np.array([1.0])), a)


def test_3_each_row_uses_its_own_denominator():
    out = finalize_output(np.array([[2.0], [6.0]]), np.array([2.0, 3.0]))
    np.testing.assert_allclose(out, [[1.0], [2.0]])


def test_4_keeps_the_shape():
    assert finalize_output(np.ones((3, 4)), np.ones(3)).shape == (3, 4)


def test_5_result_matches_softmax_weighted_average():
    scores = np.array([0.0, 1.0])
    v = np.array([[1.0], [3.0]])
    w = np.exp(scores) / np.exp(scores).sum()
    acc = (np.exp(scores)[:, None] * v).sum(axis=0, keepdims=True)
    l = np.array([np.exp(scores).sum()])
    np.testing.assert_allclose(finalize_output(acc, l), (w[:, None] * v).sum(axis=0, keepdims=True))


def test_6_does_not_mutate_accumulator():
    acc = np.array([[2.0]])
    finalize_output(acc, np.array([2.0]))
    np.testing.assert_array_equal(acc, [[2.0]])

