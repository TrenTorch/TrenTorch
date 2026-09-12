"""
pytest data/app_data/02-deep-learning-core/03-losses/03-binary-cross-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/03-losses/{Path(__file__).resolve().parent.name}")
bce_loss_forward, bce_loss_backward = _module.bce_loss_forward, _module.bce_loss_backward


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.binary_cross_entropy
    probs = np.array([0.9, 0.2, 0.5, 0.7])
    target = np.array([1.0, 0.0, 1.0, 0.0])
    assert np.isclose(bce_loss_forward(probs, target, "mean"), 0.55640601, atol=1e-6)
    assert np.isclose(bce_loss_forward(probs, target, "sum"), 2.22562405, atol=1e-6)
    assert np.allclose(
        bce_loss_forward(probs, target, "none"),
        [0.10536052, 0.22314355, 0.69314718, 1.2039728],
        atol=1e-6,
    )


def test_forward_confident_correct_prediction_gives_near_zero_loss():
    probs = np.array([0.999])
    target = np.array([1.0])
    assert bce_loss_forward(probs, target, "none")[0] < 0.01


def test_forward_confident_wrong_prediction_gives_high_loss():
    probs = np.array([0.999])
    target = np.array([0.0])
    assert bce_loss_forward(probs, target, "none")[0] > 5.0


def test_forward_does_not_blow_up_at_exact_zero_or_one():
    probs = np.array([0.0, 1.0])
    target = np.array([0.0, 1.0])
    result = bce_loss_forward(probs, target, "none")
    assert np.all(np.isfinite(result))


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.binary_cross_entropy + autograd
    probs = np.array([0.9, 0.2, 0.5, 0.7])
    target = np.array([1.0, 0.0, 1.0, 0.0])
    expected_mean = np.array([-0.27777778, 0.3125, -0.5, 0.83333333])
    assert np.allclose(bce_loss_backward(probs, target, "mean"), expected_mean, atol=1e-6)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    probs = rng.uniform(0.1, 0.9, size=6)
    target = rng.integers(0, 2, size=6).astype(float)
    analytic = bce_loss_backward(probs, target, "sum")

    eps = 1e-5
    numeric = np.empty(6)
    for i in range(6):
        plus, minus = probs.copy(), probs.copy()
        plus[i] += eps
        minus[i] -= eps
        numeric[i] = (
            bce_loss_forward(plus, target, "sum") - bce_loss_forward(minus, target, "sum")
        ) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-3)


def test_backward_sign_matches_over_and_under_confidence():
    # For target=1: probs < target -> negative gradient (push probs up).
    # For target=0: probs > target -> positive gradient (push probs down).
    grad_under = bce_loss_backward(np.array([0.3]), np.array([1.0]), "sum")[0]
    grad_over = bce_loss_backward(np.array([0.7]), np.array([0.0]), "sum")[0]
    assert grad_under < 0.0
    assert grad_over > 0.0


def test_backward_uses_probability_space_formula_not_the_fused_logit_gradient():
    # Directly targets a mutant that copy-pastes the much simpler fused
    # sigmoid+BCE gradient (prediction - target, from
    # classification-bce-gradient) instead of the correct probability-
    # space formula (probs - target) / (probs * (1 - probs)). At
    # probs=0.9, target=1.0: fused form gives -0.1, but the correct
    # probability-space gradient is -0.1/0.09 (~-1.1111).
    probs = np.array([0.9])
    target = np.array([1.0])
    result = bce_loss_backward(probs, target, "sum")[0]
    assert not np.isclose(result, -0.1)
    assert np.isclose(result, -1.11111111, atol=1e-6)
