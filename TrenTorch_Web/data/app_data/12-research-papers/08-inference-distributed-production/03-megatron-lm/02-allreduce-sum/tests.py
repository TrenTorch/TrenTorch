"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/03-megatron-lm/02-allreduce-sum/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-megatron-row-allreduce")
allreduce_sum = _module.allreduce_sum


import numpy as np


def test_1_sums_partial_results():
    np.testing.assert_allclose(allreduce_sum([np.array([1.0, 2.0]), np.array([3.0, 4.0])]), [4.0, 6.0])


def test_2_single_device_is_unchanged():
    np.testing.assert_allclose(allreduce_sum([np.array([5.0])]), [5.0])


def test_3_keeps_the_shape():
    assert allreduce_sum([np.ones((2, 3)), np.ones((2, 3))]).shape == (2, 3)


def test_4_three_devices():
    np.testing.assert_allclose(allreduce_sum([np.ones(2)] * 3), [3.0, 3.0])


def test_5_order_does_not_matter():
    a = allreduce_sum([np.array([1.0]), np.array([2.0])])
    b = allreduce_sum([np.array([2.0]), np.array([1.0])])
    np.testing.assert_allclose(a, b)


def test_6_does_not_mutate_parts():
    p = np.array([1.0])
    allreduce_sum([p, p])
    np.testing.assert_array_equal(p, [1.0])

