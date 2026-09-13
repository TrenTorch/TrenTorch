"""
pytest data/app_data/09-systems-distributed/01-memoization/03-gradient-checkpointing/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/01-memoization/{Path(__file__).resolve().parent.name}")
linear_backward = _module.linear_backward
forward_full = _module.forward_full
backward_full = _module.backward_full
forward_checkpointed = _module.forward_checkpointed
backward_checkpointed = _module.backward_checkpointed
count_stored_activations = _module.count_stored_activations


def _random_mlp(seed, num_layers=3, batch=4, d=3):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(batch, d))
    weights = [rng.normal(size=(d, d)) for _ in range(num_layers)]
    biases = [rng.normal(size=d) for _ in range(num_layers)]
    return x, weights, biases


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_forward_checkpointed_matches_forward_full_output():
    x, weights, biases = _random_mlp(0)
    out_full, _, _ = forward_full(x, weights, biases)
    out_ckpt = forward_checkpointed(x, weights, biases)
    assert np.allclose(out_full, out_ckpt)


def test_02_checkpointed_gradients_match_full_gradients_exactly():
    x, weights, biases = _random_mlp(1)
    out_full, activations, pre_activations = forward_full(x, weights, biases)
    grad_output = np.random.default_rng(2).normal(size=out_full.shape)

    grad_x_full, gw_full, gb_full = backward_full(grad_output, activations, pre_activations, weights)
    grad_x_ckpt, gw_ckpt, gb_ckpt = backward_checkpointed(grad_output, x, weights, biases)

    assert np.allclose(grad_x_full, grad_x_ckpt)
    for a, b in zip(gw_full, gw_ckpt):
        assert np.allclose(a, b)
    for a, b in zip(gb_full, gb_ckpt):
        assert np.allclose(a, b)


# --- Shape / general-case coverage -----------------------------------


def test_03_gradient_shapes_match_the_original_parameter_shapes():
    x, weights, biases = _random_mlp(3, num_layers=4)
    out_full, activations, pre_activations = forward_full(x, weights, biases)
    grad_output = np.ones_like(out_full)
    _, gw, gb = backward_full(grad_output, activations, pre_activations, weights)
    for w, g in zip(weights, gw):
        assert g.shape == w.shape
    for b, g in zip(biases, gb):
        assert g.shape == b.shape


def test_04_backward_matches_finite_difference_gradient():
    x, weights, biases = _random_mlp(4, num_layers=2, batch=3, d=2)
    rng = np.random.default_rng(5)
    grad_output_direction = rng.normal(size=(3, 2))

    def scalar_loss(xx):
        out, _, _ = forward_full(xx, weights, biases)
        return np.sum(out * grad_output_direction)

    out_full, activations, pre_activations = forward_full(x, weights, biases)
    analytic_grad_x, _, _ = backward_full(grad_output_direction, activations, pre_activations, weights)

    eps = 1e-5
    numeric_grad_x = np.empty_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            x_plus, x_minus = x.copy(), x.copy()
            x_plus[i, j] += eps
            x_minus[i, j] -= eps
            numeric_grad_x[i, j] = (scalar_loss(x_plus) - scalar_loss(x_minus)) / (2 * eps)
    assert np.allclose(analytic_grad_x, numeric_grad_x, atol=1e-4)


# --- Parameter handling -------------------------------------------------


def test_05_checkpointing_uses_far_fewer_stored_activations():
    num_layers = 10
    without = count_stored_activations(num_layers, use_checkpointing=False)
    with_ckpt = count_stored_activations(num_layers, use_checkpointing=True)
    assert without == num_layers + 1
    assert with_ckpt == 1
    assert with_ckpt < without


def test_06_stored_activation_gap_grows_with_network_depth():
    shallow_gap = count_stored_activations(3, False) - count_stored_activations(3, True)
    deep_gap = count_stored_activations(50, False) - count_stored_activations(50, True)
    assert deep_gap > shallow_gap


# --- Edge cases ---------------------------------------------------------


def test_07_single_layer_network_still_works():
    x, weights, biases = _random_mlp(6, num_layers=1)
    out_full, activations, pre_activations = forward_full(x, weights, biases)
    out_ckpt = forward_checkpointed(x, weights, biases)
    assert np.allclose(out_full, out_ckpt)
    assert len(activations) == 2  # input + one layer's output


def test_08_linear_backward_matches_hand_computation():
    grad_output = np.array([[1.0, 2.0]])
    input = np.array([[3.0, 4.0]])
    weight = np.eye(2)
    grad_input, grad_weight, grad_bias = linear_backward(grad_output, input, weight)
    assert np.allclose(grad_input, [[1.0, 2.0]])  # grad_output @ I
    assert np.allclose(grad_weight, [[3.0, 4.0], [6.0, 8.0]])  # outer(grad_output, input)
    assert np.allclose(grad_bias, [1.0, 2.0])


# --- Array hygiene ------------------------------------------------------


def test_09_does_not_mutate_its_inputs():
    x, weights, biases = _random_mlp(7)
    x_copy = x.copy()
    weights_copy = [w.copy() for w in weights]
    forward_checkpointed(x, weights, biases)
    assert np.array_equal(x, x_copy)
    for w, wc in zip(weights, weights_copy):
        assert np.array_equal(w, wc)


# --- Independent correctness oracle -----------------------------------


def test_10_checkpointing_recomputes_rather_than_silently_reusing_stale_state():
    # Directly targets a mutant that caches the forward pass's
    # activations somewhere as a side effect and reuses them in
    # backward_checkpointed instead of genuinely recomputing: calling
    # forward_checkpointed/backward_checkpointed with a DIFFERENT input
    # in between must still produce correct results for each call.
    x1, weights, biases = _random_mlp(8)
    x2, _, _ = _random_mlp(9, batch=x1.shape[0], d=x1.shape[1])

    out1 = forward_checkpointed(x1, weights, biases)
    out2 = forward_checkpointed(x2, weights, biases)
    assert not np.allclose(out1, out2)  # different inputs, genuinely different outputs

    grad_output = np.ones_like(out1)
    grad_x1, _, _ = backward_checkpointed(grad_output, x1, weights, biases)
    grad_x2, _, _ = backward_checkpointed(grad_output, x2, weights, biases)
    assert not np.allclose(grad_x1, grad_x2)  # genuinely recomputed for each input, not stale-cached
