"""
pytest data/app_data/01-classical-ml/01-linear-regression/04-gd-step/tests.py

Numbered for the same reason every question in this track is: "Run"
shows the first couple by name, "Submit" runs all of them, and the
numbering keeps both views in the same deliberate order (simple hand-
computed cases first, then shape/bias coverage, edge cases, array
hygiene, a mutation-catching case, then a real torch.optim.SGD oracle).
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

gd_step = load_solution(
    f"01-classical-ml/01-linear-regression/{Path(__file__).resolve().parent.name}"
).gd_step


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_matches_hand_computed_update():
    new_weight, new_bias = gd_step(
        np.array([1.0, 2.0]), np.array([0.5]), np.array([0.1, -0.2]), np.array([0.05]), lr=10.0
    )
    assert np.allclose(new_weight, [0.0, 4.0])
    assert np.allclose(new_bias, [0.0])


def test_02_zero_gradient_leaves_parameters_unchanged():
    weight, bias = np.array([3.0, -1.0]), np.array([2.0])
    new_weight, new_bias = gd_step(weight, bias, np.zeros(2), np.array([0.0]), lr=0.5)
    assert np.allclose(new_weight, weight)
    assert np.allclose(new_bias, bias)


# --- Shape / bias handling ------------------------------------------------


def test_03_bias_none_returns_updated_bias_none():
    # No bias parameter means there's nothing to step -- must stay None,
    # not a fabricated zero-stepped value.
    weight = np.array([1.0, 2.0])
    new_weight, new_bias = gd_step(weight, None, np.array([0.1, 0.1]), None, lr=1.0)
    assert new_bias is None
    assert np.allclose(new_weight, [0.9, 1.9])


def test_04_works_on_matrix_shaped_weight():
    # weight/grad_weight generalize to the (out_features, in_features)
    # shape 01-hypothesis-function actually produces, not just 1-D.
    weight = np.array([[1.0, 2.0], [3.0, 4.0]])
    grad_weight = np.ones((2, 2))
    new_weight, _ = gd_step(weight, None, grad_weight, None, lr=0.5)
    assert np.allclose(new_weight, [[0.5, 1.5], [2.5, 3.5]])


# --- Edge cases -------------------------------------------------------


def test_05_larger_learning_rate_moves_further():
    small, _ = gd_step(np.array([0.0]), None, np.array([1.0]), None, lr=0.01)
    large, _ = gd_step(np.array([0.0]), None, np.array([1.0]), None, lr=1.0)
    assert abs(large[0]) > abs(small[0])


def test_06_lr_zero_leaves_parameters_unchanged():
    # A zero learning rate is a valid (if useless) call -- must not step
    # at all, regardless of how large the gradient is.
    weight, bias = np.array([5.0, -5.0]), np.array([1.0])
    new_weight, new_bias = gd_step(weight, bias, np.array([100.0, -100.0]), np.array([50.0]), lr=0.0)
    assert np.allclose(new_weight, weight)
    assert np.allclose(new_bias, bias)


# --- Array hygiene: memory layout and mutability ---------------------------


def test_07_works_on_non_contiguous_arrays():
    base = np.arange(8.0).reshape(2, 4)
    weight = base[:, ::2]  # shape (2, 2), non-contiguous
    assert not weight.flags["C_CONTIGUOUS"]
    grad_weight = np.ones((2, 2))
    new_weight, _ = gd_step(weight, None, grad_weight, None, lr=1.0)
    assert np.allclose(new_weight, weight.copy() - 1.0)


def test_08_does_not_require_writable_inputs():
    weight, bias = np.array([1.0, 2.0]), np.array([0.5])
    grad_weight, grad_bias = np.array([0.1, 0.1]), np.array([0.05])
    for arr in (weight, bias, grad_weight, grad_bias):
        arr.setflags(write=False)
    new_weight, new_bias = gd_step(weight, bias, grad_weight, grad_bias, lr=1.0)
    assert new_weight.shape == (2,)
    assert new_bias.shape == (1,)


def test_09_does_not_mutate_its_inputs():
    # A real, common bug: modifying weight in place silently corrupts
    # the caller's "before" value -- breaks any before/after comparison,
    # like the loss-decrease test in the training-loop question.
    weight, bias = np.array([1.0, 1.0]), np.array([2.0])
    grad_weight, grad_bias = np.array([1.0, 1.0]), np.array([1.0])
    weight_copy, bias_copy = weight.copy(), bias.copy()
    grad_weight_copy, grad_bias_copy = grad_weight.copy(), grad_bias.copy()
    gd_step(weight, bias, grad_weight, grad_bias, lr=1.0)
    assert np.array_equal(weight, weight_copy)
    assert np.array_equal(bias, bias_copy)
    assert np.array_equal(grad_weight, grad_weight_copy)
    assert np.array_equal(grad_bias, grad_bias_copy)


# --- Independent correctness oracle -----------------------------------


def test_10_matches_torch_optim_sgd_step():
    # torch.optim.SGD with no momentum/weight-decay does exactly this
    # update rule: p -= lr * p.grad. Verified once, offline, with:
    #   w = torch.tensor([2.0, -1.0, 0.5], requires_grad=True)
    #   b = torch.tensor([0.3], requires_grad=True)
    #   opt = torch.optim.SGD([w, b], lr=0.1)
    #   w.grad = torch.tensor([1.0, 2.0, -3.0])
    #   b.grad = torch.tensor([0.5])
    #   opt.step()
    #   # w, b now hold the expected values below
    #
    # This test needs no torch installed to run -- the reference values
    # are baked in below.
    weight = np.array([2.0, -1.0, 0.5])
    bias = np.array([0.3])
    grad_weight = np.array([1.0, 2.0, -3.0])
    grad_bias = np.array([0.5])
    new_weight, new_bias = gd_step(weight, bias, grad_weight, grad_bias, lr=0.1)
    assert np.allclose(new_weight, [1.9, -1.2, 0.8])
    assert np.allclose(new_bias, [0.25])
