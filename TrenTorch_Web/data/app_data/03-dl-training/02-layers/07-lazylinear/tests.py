"""
pytest data/app_data/03-dl-training/02-layers/07-lazylinear/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/02-layers/{Path(__file__).resolve().parent.name}")
LazyLinear = _module.LazyLinear


def test_weight_and_bias_are_none_before_the_first_forward_call():
    layer = LazyLinear(out_features=3)
    assert layer.weight is None
    assert layer.bias is None


def test_infers_in_features_from_the_first_forward_call():
    layer = LazyLinear(out_features=3)
    x = np.random.randn(5, 7)
    layer.forward(x)
    assert layer.weight.shape == (3, 7)
    assert layer.bias.shape == (3,)


def test_output_shape_matches_batch_size_and_out_features():
    layer = LazyLinear(out_features=4)
    x = np.random.randn(6, 10)
    out = layer.forward(x)
    assert out.shape == (6, 4)


def test_second_call_reuses_the_same_weight_object_not_a_new_one():
    layer = LazyLinear(out_features=3)
    x1 = np.random.randn(5, 7)
    layer.forward(x1)
    weight_after_first_call = layer.weight
    x2 = np.random.randn(2, 7)
    layer.forward(x2)
    assert layer.weight is weight_after_first_call


def test_uses_the_provided_weight_init_function_not_the_default():
    def custom_weight_init(in_features, out_features):
        return np.ones((out_features, in_features)) * 5.0

    def custom_bias_init(out_features):
        return np.ones(out_features) * 2.0

    layer = LazyLinear(out_features=2, weight_init=custom_weight_init, bias_init=custom_bias_init)
    x = np.zeros((1, 3))
    out = layer.forward(x)
    assert np.allclose(layer.weight, 5.0)
    assert np.allclose(layer.bias, 2.0)
    # x is all zeros, so output should equal the bias exactly
    assert np.allclose(out, [[2.0, 2.0]])


def test_parameters_are_registered_after_first_forward_call():
    layer = LazyLinear(out_features=3)
    x = np.random.randn(2, 4)
    layer.forward(x)
    params = layer.parameters()
    assert len(params) == 2


def test_output_matches_hand_computation_after_lazy_initialization():
    def weight_init(in_features, out_features):
        return np.eye(out_features, in_features)

    def bias_init(out_features):
        return np.zeros(out_features)

    layer = LazyLinear(out_features=2, weight_init=weight_init, bias_init=bias_init)
    x = np.array([[3.0, 4.0]])
    out = layer.forward(x)
    assert np.allclose(out, [[3.0, 4.0]])


def test_does_not_reinitialize_on_a_second_call_even_with_a_different_batch_size():
    # Directly targets a mutant that forgets the `if self.weight is None`
    # guard and re-runs the initializer on EVERY call: with a fresh
    # np.zeros-based default initializer this would coincidentally still
    # look right, so use a call-counting initializer to catch it directly.
    call_count = {"n": 0}

    def counting_weight_init(in_features, out_features):
        call_count["n"] += 1
        return np.zeros((out_features, in_features))

    def bias_init(out_features):
        return np.zeros(out_features)

    layer = LazyLinear(out_features=2, weight_init=counting_weight_init, bias_init=bias_init)
    layer.forward(np.zeros((1, 5)))
    layer.forward(np.zeros((3, 5)))
    layer.forward(np.zeros((7, 5)))
    assert call_count["n"] == 1
