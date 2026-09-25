"""
pytest data/app_data/01-numpy/10-bridging-to-tensors/04-assemble-linear-layer-and-attention/tests.py
"""

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/10-bridging-to-tensors/{Path(__file__).resolve().parent.name}")
init_linear_params = _module.init_linear_params
linear_forward = _module.linear_forward
attention_weights = _module.attention_weights


def test_parameter_shapes_dtypes_and_flags():
    rng = np.random.default_rng(0)
    params = init_linear_params(rng, 8, 4, device="cuda")
    assert params["W"]["data"].shape == (8, 4)
    assert params["W"]["data"].dtype == np.float32
    assert params["b"]["data"].shape == (4,)
    assert params["b"]["data"].dtype == np.float32
    np.testing.assert_array_equal(params["b"]["data"], np.zeros(4))
    assert params["W"]["requires_grad"] is True
    assert params["b"]["requires_grad"] is True
    assert params["W"]["device"] == "cuda"
    assert params["b"]["device"] == "cuda"


def test_initialization_reproducible_and_scaled():
    rng_a = np.random.default_rng(42)
    rng_b = np.random.default_rng(42)
    params_a = init_linear_params(rng_a, 256, 128)
    params_b = init_linear_params(rng_b, 256, 128)
    np.testing.assert_array_equal(params_a["W"]["data"], params_b["W"]["data"])

    expected_std = np.sqrt(2.0 / 256)
    assert abs(params_a["W"]["data"].std() - expected_std) < 0.01
    assert abs(params_a["W"]["data"].mean()) < 0.01


def test_initialization_draws_in_specified_way():
    rng = np.random.default_rng(7)
    params = init_linear_params(rng, 4, 3)
    reference_rng = np.random.default_rng(7)
    expected_W = reference_rng.normal(0.0, np.sqrt(2.0 / 4), (4, 3)).astype(np.float32)
    np.testing.assert_array_equal(params["W"]["data"], expected_W)


def test_forward_output_value_and_shape():
    rng = np.random.default_rng(0)
    params = init_linear_params(rng, 5, 3)
    for batch in [1, 4]:
        x_data = rng.standard_normal((batch, 5)).astype(np.float32)
        x = {"data": x_data, "device": "cpu", "requires_grad": False}
        result = linear_forward(x, params)
        assert result["data"].shape == (batch, 3)
        expected = x_data @ params["W"]["data"] + params["b"]["data"]
        np.testing.assert_allclose(result["data"], expected, atol=1e-5)


def test_bias_broadcast_across_batch():
    params = {
        "W": {"data": np.zeros((3, 2), dtype=np.float32), "device": "cpu", "requires_grad": True},
        "b": {"data": np.array([1.0, 2.0], dtype=np.float32), "device": "cpu", "requires_grad": True},
    }
    x = {"data": np.ones((4, 3), dtype=np.float32), "device": "cpu", "requires_grad": False}
    result = linear_forward(x, params)
    for row in result["data"]:
        np.testing.assert_array_equal(row, [1.0, 2.0])


def test_gradient_flag_propagation():
    rng = np.random.default_rng(0)
    params = init_linear_params(rng, 4, 2)
    x_no_grad = {"data": np.ones((2, 4), dtype=np.float32), "device": "cpu", "requires_grad": False}
    assert linear_forward(x_no_grad, params)["requires_grad"] is True

    params_no_grad = {
        "W": {"data": np.zeros((4, 2), dtype=np.float32), "device": "cpu", "requires_grad": False},
        "b": {"data": np.zeros(2, dtype=np.float32), "device": "cpu", "requires_grad": False},
    }
    assert linear_forward(x_no_grad, params_no_grad)["requires_grad"] is False


def test_device_and_shape_errors():
    rng = np.random.default_rng(0)
    params = init_linear_params(rng, 4, 2, device="cpu")
    x_wrong_device = {
        "data": np.ones((2, 4), dtype=np.float32),
        "device": "cuda",
        "requires_grad": False,
    }
    with pytest.raises(ValueError):
        linear_forward(x_wrong_device, params)

    x_wrong_shape = {
        "data": np.ones((2, 5), dtype=np.float32),
        "device": "cpu",
        "requires_grad": False,
    }
    with pytest.raises(ValueError):
        linear_forward(x_wrong_shape, params)


def test_attention_weights_are_valid_distributions():
    rng = np.random.default_rng(0)
    q = rng.standard_normal((5, 8))
    k = rng.standard_normal((7, 8))
    result = attention_weights(q, k)
    assert result.shape == (5, 7)
    assert np.all(result >= 0)
    np.testing.assert_allclose(result.sum(axis=1), np.ones(5), atol=1e-6)


def test_attention_weights_matches_reference():
    rng = np.random.default_rng(1)
    q = rng.standard_normal((3, 4))
    k = rng.standard_normal((3, 4))
    d = q.shape[-1]
    scores = q @ k.T / np.sqrt(d)
    reference = np.exp(scores) / np.exp(scores).sum(axis=1, keepdims=True)
    result = attention_weights(q, k)
    np.testing.assert_allclose(result, reference, atol=1e-6)


def test_numerical_stability():
    q = np.array([[1000.0, 0.0], [0.0, 1000.0]])
    k = np.array([[1000.0, 0.0], [0.0, 1000.0]])
    result = attention_weights(q, k)
    assert not np.any(np.isnan(result))
    assert not np.any(np.isinf(result))
    np.testing.assert_allclose(result.sum(axis=1), [1.0, 1.0], atol=1e-6)


def test_attention_edge_cases():
    q_zero = np.zeros((2, 3))
    k = np.random.default_rng(0).standard_normal((4, 3))
    result = attention_weights(q_zero, k)
    np.testing.assert_allclose(result, np.full((2, 4), 1.0 / 4), atol=1e-6)

    q_single = np.array([[1.0, 2.0]])
    k_single = np.array([[3.0, 4.0]])
    result_single = attention_weights(q_single, k_single)
    np.testing.assert_allclose(result_single, [[1.0]])

    with pytest.raises(ValueError):
        attention_weights(np.zeros((2, 3)), np.zeros((2, 4)))


def test_no_input_mutation():
    q = np.array([[1.0, 2.0], [3.0, 4.0]])
    k = np.array([[5.0, 6.0], [7.0, 8.0]])
    q_original = q.copy()
    k_original = k.copy()
    attention_weights(q, k)
    np.testing.assert_array_equal(q, q_original)
    np.testing.assert_array_equal(k, k_original)
