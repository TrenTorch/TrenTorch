"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/03-megatron-lm/03-tp-matmul/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-megatron-tp-matmul")
tensor_parallel_matmul = _module.tensor_parallel_matmul


import numpy as np


def test_1_matches_the_dense_matmul():
    rng = np.random.default_rng(0)
    x = rng.normal(size=(3, 4))
    W = rng.normal(size=(4, 6))
    np.testing.assert_allclose(tensor_parallel_matmul(x, np.split(W, 3, axis=1)), x @ W)


def test_2_single_shard_is_the_plain_matmul():
    x = np.ones((2, 2))
    W = np.array([[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(tensor_parallel_matmul(x, [W]), x @ W)


def test_3_output_shape_is_rows_by_total_columns():
    out = tensor_parallel_matmul(np.ones((5, 3)), [np.ones((3, 2)), np.ones((3, 4))])
    assert out.shape == (5, 6)


def test_4_hand_value():
    x = np.array([[1.0, 1.0]])
    shards = [np.array([[1.0], [0.0]]), np.array([[0.0], [2.0]])]
    np.testing.assert_allclose(tensor_parallel_matmul(x, shards), [[1.0, 2.0]])


def test_5_zero_input_gives_zero_output():
    out = tensor_parallel_matmul(np.zeros((2, 2)), [np.eye(2)])
    np.testing.assert_allclose(out, 0.0)


def test_6_does_not_mutate_inputs():
    x = np.ones((1, 2))
    tensor_parallel_matmul(x, [np.ones((2, 1))])
    np.testing.assert_array_equal(x, np.ones((1, 2)))

