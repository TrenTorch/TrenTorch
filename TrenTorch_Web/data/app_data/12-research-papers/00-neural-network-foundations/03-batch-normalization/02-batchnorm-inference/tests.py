"""
pytest data/app_data/12-research-papers/00-neural-network-foundations/03-batch-normalization/02-batchnorm-inference/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-batchnorm-inference")
batchnorm_inference = _module.batchnorm_inference


import numpy as np


def test_1_uses_running_stats_not_batch_stats():
    x = np.array([[10.0]])
    out = batchnorm_inference(x, np.ones(1), np.zeros(1), np.array([10.0]), np.array([1.0]), eps=0.0)
    np.testing.assert_allclose(out, [[0.0]])


def test_2_single_example_batch_works():
    out = batchnorm_inference(np.array([[2.0, 4.0]]), np.ones(2), np.zeros(2), np.zeros(2), np.ones(2), eps=0.0)
    np.testing.assert_allclose(out, [[2.0, 4.0]])


def test_3_scale_and_shift_are_applied():
    x = np.array([[1.0]])
    out = batchnorm_inference(x, np.array([3.0]), np.array([5.0]), np.array([0.0]), np.array([1.0]), eps=0.0)
    np.testing.assert_allclose(out, [[8.0]])


def test_4_output_shape_matches_input():
    out = batchnorm_inference(np.ones((5, 2)), np.ones(2), np.zeros(2), np.zeros(2), np.ones(2))
    assert out.shape == (5, 2)


def test_5_does_not_mutate_inputs():
    rm = np.array([1.0])
    batchnorm_inference(np.array([[2.0]]), np.ones(1), np.zeros(1), rm, np.ones(1))
    np.testing.assert_array_equal(rm, [1.0])


def test_6_matches_a_hand_computed_case():
    # (4 - 2) / sqrt(4) = 1, then 1 * 2 + 1 = 3
    out = batchnorm_inference(np.array([[4.0]]), np.array([2.0]), np.array([1.0]), np.array([2.0]), np.array([4.0]), eps=0.0)
    np.testing.assert_allclose(out, [[3.0]])

