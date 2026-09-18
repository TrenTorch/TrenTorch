"""
pytest data/app_data/02-deep-learning-core/01-tensors/04-matmul/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

matmul = load_solution(f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}").matmul


def test_1d_dot_1d_gives_a_scalar():
    result = matmul(np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, 6.0]))
    assert result.shape == ()
    assert np.isclose(result, 32.0)  # 1*4+2*5+3*6


def test_2d_matmul_1d_gives_1d_result():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([5.0, 6.0])
    result = matmul(a, b)
    assert result.shape == (2,)
    assert np.allclose(result, [17.0, 39.0])  # [1*5+2*6, 3*5+4*6]


def test_1d_matmul_2d_gives_1d_result():
    a = np.array([1.0, 2.0])
    b = np.array([[1.0, 0.0, 1.0], [0.0, 1.0, 1.0]])
    result = matmul(a, b)
    assert result.shape == (3,)
    assert np.allclose(result, [1.0, 2.0, 3.0])


def test_2d_matmul_2d_matches_hand_computation():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[5.0, 6.0], [7.0, 8.0]])
    result = matmul(a, b)
    assert np.allclose(result, [[19.0, 22.0], [43.0, 50.0]])


def test_batched_matmul_broadcasts_the_leading_dimension():
    # A (2, 3, 4) batch of matrices, each multiplied by the SAME shared
    # (4, 5) weight matrix -- the leading batch dim broadcasts, the
    # trailing two dims matrix-multiply, per 03-broadcasting-rules.
    rng = np.random.default_rng(0)
    batch = rng.normal(size=(2, 3, 4))
    shared_weight = rng.normal(size=(4, 5))
    result = matmul(batch, shared_weight)
    assert result.shape == (2, 3, 5)
    assert np.allclose(result[0], batch[0] @ shared_weight)
    assert np.allclose(result[1], batch[1] @ shared_weight)


def test_batched_matmul_of_two_batches_multiplies_matching_batch_elements():
    rng = np.random.default_rng(1)
    a = rng.normal(size=(3, 2, 4))
    b = rng.normal(size=(3, 4, 5))
    result = matmul(a, b)
    for i in range(3):
        assert np.allclose(result[i], a[i] @ b[i])
