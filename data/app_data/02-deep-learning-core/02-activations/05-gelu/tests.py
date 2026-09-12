"""
pytest data/app_data/02-deep-learning-core/02-activations/05-gelu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/02-activations/{Path(__file__).resolve().parent.name}")
gelu_forward, gelu_backward = _module.gelu_forward, _module.gelu_backward


def test_forward_at_zero_is_zero():
    assert np.isclose(gelu_forward(np.array([0.0]))[0], 0.0)


def test_forward_at_large_positive_x_approaches_identity():
    # Phi(x) -> 1 as x -> +inf, so GELU(x) -> x.
    x = np.array([10.0])
    assert np.isclose(gelu_forward(x)[0], 10.0, atol=1e-4)


def test_forward_at_large_negative_x_approaches_zero():
    x = np.array([-10.0])
    assert np.isclose(gelu_forward(x)[0], 0.0, atol=1e-4)


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.gelu
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.00404987, -0.15865529, -0.15426879, 0.34573120, 0.84134471, 2.99595022]
    )
    assert np.allclose(gelu_forward(x), expected, atol=1e-6)


def test_forward_dips_below_zero_for_small_negative_x():
    # The defining non-monotonic quirk that separates GELU from ReLU:
    # GELU is slightly negative around x = -0.75, not just "clamped to 0".
    x = np.array([-0.75])
    assert gelu_forward(x)[0] < 0.0


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.gelu + autograd
    x = np.array([-3.0, -1.0, -0.5, 0.5, 1.0, 3.0])
    expected = np.array(
        [-0.01194561, -0.08331543, 0.13250491, 0.86749506, 1.08331537, 1.01194561]
    )
    grad_output = np.ones_like(x)
    assert np.allclose(gelu_backward(grad_output, x), expected, atol=1e-6)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    x = rng.normal(size=10)
    grad_output = rng.normal(size=10)
    analytic = gelu_backward(grad_output, x)

    eps = 1e-5
    numeric = np.empty(10)
    for i in range(10):
        x_plus, x_minus = x.copy(), x.copy()
        x_plus[i] += eps
        x_minus[i] -= eps
        numeric[i] = (
            (gelu_forward(x_plus)[i] - gelu_forward(x_minus)[i]) / (2 * eps) * grad_output[i]
        )
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_uses_input_x_not_a_reconstructed_output_based_formula():
    # Directly targets a mutant that (wrongly) tries to reuse the
    # output-based backward pattern from sigmoid/tanh, e.g. treating
    # the local derivative as though it only depended on gelu_forward(x)
    # rather than needing x itself in the phi(x) term. At x=1.0 the
    # correct derivative is ~1.0833, not close to gelu_forward(1.0)-based
    # shortcuts like output*(1-output) (~0.134 for output~0.841).
    x = np.array([1.0])
    grad_output = np.array([1.0])
    result = gelu_backward(grad_output, x)[0]
    assert np.isclose(result, 1.08331537, atol=1e-6)
    assert not np.isclose(result, 0.134, atol=0.05)
