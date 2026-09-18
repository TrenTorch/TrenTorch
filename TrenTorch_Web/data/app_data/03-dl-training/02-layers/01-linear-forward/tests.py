"""
pytest data/app_data/03-dl-training/02-layers/01-linear-forward/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
linear_forward = _module.linear_forward


def test_matches_hand_computation_for_a_single_sample():
    x = np.array([[1.0, 2.0]])
    weight = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])  # (3, 2)
    bias = np.array([0.0, 0.0, 10.0])
    result = linear_forward(x, weight, bias)
    # neuron0: 1*1+2*0=1, neuron1: 1*0+2*1=2, neuron2: 1*1+2*1+10=13
    assert np.allclose(result, [[1.0, 2.0, 13.0]])


def test_output_shape_is_batch_size_by_out_features():
    x = np.random.randn(5, 4)
    weight = np.random.randn(3, 4)
    bias = np.random.randn(3)
    result = linear_forward(x, weight, bias)
    assert result.shape == (5, 3)


def test_works_for_batch_size_one():
    x = np.random.randn(1, 4)
    weight = np.random.randn(3, 4)
    bias = np.random.randn(3)
    result = linear_forward(x, weight, bias)
    assert result.shape == (1, 3)


def test_zero_weight_and_zero_bias_gives_zero_output():
    x = np.random.randn(5, 4)
    weight = np.zeros((3, 4))
    bias = np.zeros(3)
    result = linear_forward(x, weight, bias)
    assert np.allclose(result, 0.0)


def test_matches_known_oracle_from_pytorch_nn_linear():
    x = np.array([[0.5, -0.5, 1.0]])
    weight = np.array([[0.1, 0.2, 0.3], [-0.1, 0.4, -0.2]])
    bias = np.array([0.05, -0.05])
    result = linear_forward(x, weight, bias)
    # verified against torch.nn.Linear with these exact weight/bias
    assert np.allclose(result, [[0.3, -0.5]], atol=1e-6)


def test_bias_is_broadcast_identically_to_every_row_of_the_batch():
    weight = np.eye(3)
    bias = np.array([1.0, 2.0, 3.0])
    x = np.zeros((4, 3))
    result = linear_forward(x, weight, bias)
    for row in result:
        assert np.allclose(row, bias)


def test_uses_weight_transpose_not_weight_directly():
    # Directly targets a mutant that computes x @ weight instead of
    # x @ weight.T: for a non-square weight this would be a shape error,
    # but for a square, non-symmetric weight it silently produces the
    # WRONG numbers instead of matching the true linear-layer convention.
    x = np.array([[1.0, 0.0]])
    weight = np.array([[1.0, 2.0], [3.0, 4.0]])  # NOT symmetric
    bias = np.array([0.0, 0.0])
    result = linear_forward(x, weight, bias)
    # correct: x @ weight.T = [1,0] @ [[1,3],[2,4]] = [1, 3]
    assert np.allclose(result, [[1.0, 3.0]])
