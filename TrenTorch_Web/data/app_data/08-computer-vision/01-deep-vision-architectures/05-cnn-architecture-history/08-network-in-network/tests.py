"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
pointwise_mlp = _module.pointwise_mlp
global_avg_pool = _module.global_avg_pool
nin_logits = _module.nin_logits


def make(seed=0):
    rng = np.random.RandomState(seed)
    return rng.randn(4, 3, 3), [(rng.randn(6, 4), rng.randn(6)), (rng.randn(5, 6), rng.randn(5))]


def test_1_global_average_pool_hand_computed():
    x = np.array([[[1.0, 3.0], [5.0, 7.0]], [[0.0, 0.0], [0.0, 4.0]]])
    assert np.allclose(global_avg_pool(x), [4.0, 1.0])


def test_2_single_layer_is_a_linear_per_pixel_map():
    x = np.random.RandomState(1).randn(2, 3, 3)
    W, b = np.array([[1.0, -1.0]]), np.array([0.5])
    out = pointwise_mlp(x, [(W, b)])
    assert np.allclose(out[0], x[0] - x[1] + 0.5)


def test_3_relu_between_layers_but_not_after_the_last():
    x = np.full((1, 1, 1), -2.0)
    layers = [(np.array([[1.0]]), np.array([0.0])), (np.array([[1.0]]), np.array([-3.0]))]
    # first layer: relu(-2) = 0 ; second layer linear: 0 - 3 = -3 (negative output survives)
    assert np.allclose(pointwise_mlp(x, layers), -3.0)


def test_4_output_shapes():
    x, layers = make()
    assert pointwise_mlp(x, layers).shape == (5, 3, 3) and nin_logits(x, layers).shape == (5,)


def test_5_pooling_commutes_with_a_final_linear_layer():
    x, layers = make(2)
    hidden = pointwise_mlp(x, layers[:1])
    hidden_relu = np.maximum(hidden, 0)
    W, b = layers[1]
    assert np.allclose(nin_logits(x, layers), W @ hidden_relu.mean(axis=(1, 2)) + b)


def test_6_works_for_any_spatial_size():
    x, layers = make(3)
    big = np.random.RandomState(4).randn(4, 9, 7)
    assert nin_logits(big, layers).shape == nin_logits(x, layers).shape == (5,)


def test_7_inputs_untouched():
    x, layers = make(5)
    sx = x.copy()
    sl = [(W.copy(), b.copy()) for W, b in layers]
    nin_logits(x, layers)
    assert np.array_equal(x, sx) and all(np.array_equal(a[0], b[0]) for a, b in zip(layers, sl))
