"""
pytest data/app_data/10-rl-alignment/03-fine-tuning/01-lora-low-rank-adapters/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/03-fine-tuning/{Path(__file__).resolve().parent.name}")
lora_forward = _module.lora_forward
lora_backward = _module.lora_backward
linear = _module.linear


def _random_setup(seed, batch=4, in_f=5, out_f=3, rank=2):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(batch, in_f))
    W = rng.normal(size=(out_f, in_f))
    b = rng.normal(size=out_f)
    A = rng.normal(size=(rank, in_f))
    B = rng.normal(size=(out_f, rank))
    return x, W, b, A, B


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_lora_output_equals_base_plus_delta():
    x, W, b, A, B = _random_setup(0)
    out, _ = lora_forward(x, W, b, A, B, alpha=4.0, rank=2)
    base = linear(x, W, b)
    delta = (4.0 / 2) * (x @ A.T) @ B.T
    assert np.allclose(out, base + delta)


def test_02_gradients_match_finite_differences():
    x, W, b, A, B = _random_setup(1, batch=3, in_f=4, out_f=3, rank=2)
    alpha, rank = 2.0, 2
    out, cache = lora_forward(x, W, b, A, B, alpha, rank)
    rng = np.random.default_rng(2)
    grad_output = rng.normal(size=out.shape)
    grad_A, grad_B = lora_backward(grad_output, cache, B, alpha, rank)

    eps = 1e-5

    def loss(A_, B_):
        o, _ = lora_forward(x, W, b, A_, B_, alpha, rank)
        return np.sum(o * grad_output)

    numeric_grad_A = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            Ap, Am = A.copy(), A.copy()
            Ap[i, j] += eps
            Am[i, j] -= eps
            numeric_grad_A[i, j] = (loss(Ap, B) - loss(Am, B)) / (2 * eps)
    assert np.allclose(grad_A, numeric_grad_A, atol=1e-4)

    numeric_grad_B = np.zeros_like(B)
    for i in range(B.shape[0]):
        for j in range(B.shape[1]):
            Bp, Bm = B.copy(), B.copy()
            Bp[i, j] += eps
            Bm[i, j] -= eps
            numeric_grad_B[i, j] = (loss(A, Bp) - loss(A, Bm)) / (2 * eps)
    assert np.allclose(grad_B, numeric_grad_B, atol=1e-4)


# --- General-case coverage --------------------------------------------


def test_03_zero_lora_matrices_reduce_to_the_frozen_base_layer():
    x, W, b, A, B = _random_setup(3)
    zero_A, zero_B = np.zeros_like(A), np.zeros_like(B)
    out, _ = lora_forward(x, W, b, zero_A, zero_B, alpha=4.0, rank=2)
    assert np.allclose(out, linear(x, W, b))


def test_04_output_shape_matches_out_features():
    x, W, b, A, B = _random_setup(4, batch=6, out_f=7)
    out, _ = lora_forward(x, W, b, A, B, alpha=1.0, rank=A.shape[0])
    assert out.shape == (6, 7)


def test_05_alpha_scales_the_lora_contribution_linearly():
    x, W, b, A, B = _random_setup(5)
    out1, _ = lora_forward(x, W, b, A, B, alpha=1.0, rank=2)
    out2, _ = lora_forward(x, W, b, A, B, alpha=2.0, rank=2)
    base = linear(x, W, b)
    assert np.allclose((out2 - base), 2 * (out1 - base))


# --- Parameter handling -------------------------------------------------


def test_06_gradients_have_correct_shapes():
    x, W, b, A, B = _random_setup(6, batch=5, in_f=6, out_f=4, rank=3)
    out, cache = lora_forward(x, W, b, A, B, alpha=1.0, rank=3)
    grad_output = np.ones_like(out)
    grad_A, grad_B = lora_backward(grad_output, cache, B, alpha=1.0, rank=3)
    assert grad_A.shape == A.shape
    assert grad_B.shape == B.shape


def test_07_rank_one_lora_still_works():
    x, W, b, A, B = _random_setup(7, rank=1)
    out, cache = lora_forward(x, W, b, A, B, alpha=1.0, rank=1)
    assert out.shape[0] == x.shape[0]
    grad_A, grad_B = lora_backward(np.ones_like(out), cache, B, alpha=1.0, rank=1)
    assert grad_A.shape == (1, x.shape[1])


# --- Edge cases ---------------------------------------------------------


def test_08_does_not_mutate_its_inputs():
    x, W, b, A, B = _random_setup(8)
    x_c, W_c, b_c, A_c, B_c = x.copy(), W.copy(), b.copy(), A.copy(), B.copy()
    lora_forward(x, W, b, A, B, alpha=4.0, rank=2)
    assert np.array_equal(x, x_c)
    assert np.array_equal(W, W_c)
    assert np.array_equal(b, b_c)
    assert np.array_equal(A, A_c)
    assert np.array_equal(B, B_c)


def test_09_single_example_batch():
    x, W, b, A, B = _random_setup(9, batch=1)
    out, _ = lora_forward(x, W, b, A, B, alpha=1.0, rank=2)
    assert out.shape == (1, W.shape[0])


# --- Independent correctness oracle -----------------------------------


def test_10_base_weight_and_bias_genuinely_frozen_no_gradient_path():
    # Directly targets a mutant that accidentally treats base_weight or
    # base_bias as trainable (e.g. by returning gradients for them, or
    # by silently folding a spurious extra term into grad_A/grad_B):
    # perturbing base_weight must not change the LoRA gradients at all,
    # since they only depend on the frozen forward pass's cached input.
    x, W, b, A, B = _random_setup(10)
    alpha, rank = 3.0, 2
    out, cache = lora_forward(x, W, b, A, B, alpha, rank)
    grad_output = np.ones_like(out)
    grad_A_1, grad_B_1 = lora_backward(grad_output, cache, B, alpha, rank)

    W_perturbed = W + 100.0
    out2, cache2 = lora_forward(x, W_perturbed, b, A, B, alpha, rank)
    grad_A_2, grad_B_2 = lora_backward(grad_output, cache2, B, alpha, rank)

    assert np.allclose(grad_A_1, grad_A_2)
    assert np.allclose(grad_B_1, grad_B_2)
