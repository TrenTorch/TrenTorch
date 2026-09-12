"""
pytest data/app_data/02-deep-learning-core/03-losses/02-cross-entropy/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/03-losses/{Path(__file__).resolve().parent.name}")
cross_entropy_forward, cross_entropy_backward = (
    _module.cross_entropy_forward,
    _module.cross_entropy_backward,
)


def test_forward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.cross_entropy
    logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0], [1.0, 1.0, 1.0]])
    target = np.array([0, 1, 2])
    assert np.isclose(cross_entropy_forward(logits, target, "mean"), 0.60733267, atol=1e-6)
    assert np.isclose(cross_entropy_forward(logits, target, "sum"), 1.82199802, atol=1e-6)
    assert np.allclose(
        cross_entropy_forward(logits, target, "none"),
        [0.41703002, 0.30635571, 1.09861229],
        atol=1e-6,
    )


def test_forward_uniform_logits_gives_log_of_num_classes():
    # When every class has an equal logit, softmax is uniform (1/k each),
    # so the loss is exactly -log(1/k) = log(k), regardless of target.
    logits = np.array([[0.0, 0.0, 0.0, 0.0]])
    target = np.array([2])
    assert np.isclose(cross_entropy_forward(logits, target, "none")[0], np.log(4))


def test_forward_confident_correct_prediction_gives_low_loss():
    logits = np.array([[10.0, 0.0, 0.0]])
    target = np.array([0])
    assert cross_entropy_forward(logits, target, "none")[0] < 0.01


def test_forward_confident_wrong_prediction_gives_high_loss():
    logits = np.array([[10.0, 0.0, 0.0]])
    target = np.array([1])
    assert cross_entropy_forward(logits, target, "none")[0] > 5.0


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.cross_entropy + autograd
    logits = np.array([[2.0, 1.0, 0.1], [0.5, 2.5, 1.0], [1.0, 1.0, 1.0]])
    target = np.array([0, 1, 2])
    expected_mean = np.array(
        [
            [-0.11366629, 0.08081099, 0.0328553],
            [0.03320788, -0.08795843, 0.05475054],
            [0.11111111, 0.11111111, -0.22222222],
        ]
    )
    assert np.allclose(cross_entropy_backward(logits, target, "mean"), expected_mean, atol=1e-6)


def test_backward_gradient_at_true_class_is_probability_minus_one():
    # A structural check straight from the closed form: at the true
    # class column, dL/d_logit = softmax(logit) - 1, always <= 0 (never
    # positive), since probability is always <= 1.
    logits = np.array([[1.0, 2.0, 0.5]])
    target = np.array([1])
    grad = cross_entropy_backward(logits, target, "sum")
    assert grad[0, 1] <= 0.0


def test_backward_rows_sum_to_zero():
    # softmax(logits) sums to 1 per row, one_hot(target) also sums to 1
    # per row, so their difference sums to 0 -- same structural property
    # 04-softmax's own backward has.
    rng = np.random.default_rng(0)
    logits = rng.normal(size=(5, 4))
    target = rng.integers(0, 4, size=5)
    grad = cross_entropy_backward(logits, target, "sum")
    assert np.allclose(grad.sum(axis=-1), 0.0, atol=1e-10)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(1)
    logits = rng.normal(size=(4, 3))
    target = rng.integers(0, 3, size=4)
    analytic = cross_entropy_backward(logits, target, "sum")

    eps = 1e-5
    numeric = np.empty_like(logits)
    for r in range(logits.shape[0]):
        for c in range(logits.shape[1]):
            plus, minus = logits.copy(), logits.copy()
            plus[r, c] += eps
            minus[r, c] -= eps
            numeric[r, c] = (
                cross_entropy_forward(plus, target, "sum")
                - cross_entropy_forward(minus, target, "sum")
            ) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-4)


def test_backward_does_not_forget_to_subtract_one_at_the_target_class():
    # Directly targets a mutant that returns plain softmax(logits) as
    # the gradient, forgetting the "- one_hot(target)" term entirely.
    # For a uniform-logit input, plain softmax is uniform (0.25 each),
    # but the correct gradient at the target column is 0.25 - 1 = -0.75.
    logits = np.array([[0.0, 0.0, 0.0, 0.0]])
    target = np.array([2])
    grad = cross_entropy_backward(logits, target, "sum")
    assert np.isclose(grad[0, 2], -0.75)
    assert not np.isclose(grad[0, 2], 0.25)
