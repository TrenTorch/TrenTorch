"""
pytest data/app_data/02-deep-learning-core/03-losses/01-mse/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"02-deep-learning-core/03-losses/{Path(__file__).resolve().parent.name}")
mse_loss_forward, mse_loss_backward = _module.mse_loss_forward, _module.mse_loss_backward


def test_forward_zero_when_input_equals_target():
    x = np.array([1.0, 2.0, 3.0])
    assert np.isclose(mse_loss_forward(x, x), 0.0)


def test_forward_mean_matches_hand_computation():
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([1.5, 1.5, 3.5, 3.0])
    # squared errors: 0.25, 0.25, 0.25, 1.0 -> mean = 1.75/4 = 0.4375
    assert np.isclose(mse_loss_forward(input_, target, "mean"), 0.4375)


def test_forward_sum_is_n_times_mean():
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([1.5, 1.5, 3.5, 3.0])
    mean_loss = mse_loss_forward(input_, target, "mean")
    sum_loss = mse_loss_forward(input_, target, "sum")
    assert np.isclose(sum_loss, mean_loss * input_.size)


def test_forward_none_returns_full_elementwise_array():
    input_ = np.array([1.0, 2.0])
    target = np.array([1.5, 1.5])
    result = mse_loss_forward(input_, target, "none")
    assert result.shape == input_.shape
    assert np.allclose(result, [0.25, 0.25])


def test_backward_matches_known_oracle_values():
    # generated once, offline, via torch.nn.functional.mse_loss + autograd
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([1.5, 1.5, 3.5, 3.0])
    assert np.allclose(
        mse_loss_backward(input_, target, "mean"), [-0.25, 0.25, -0.25, 0.5]
    )
    assert np.allclose(
        mse_loss_backward(input_, target, "sum"), [-1.0, 1.0, -1.0, 2.0]
    )
    assert np.allclose(
        mse_loss_backward(input_, target, "none"), [-1.0, 1.0, -1.0, 2.0]
    )


def test_backward_mean_scales_down_by_element_count_vs_sum():
    # Directly targets a mutant that forgets to divide by n for "mean",
    # silently reusing the "sum" gradient (differ by exactly n=4 here).
    input_ = np.array([1.0, 2.0, 3.0, 4.0])
    target = np.array([0.0, 0.0, 0.0, 0.0])
    mean_grad = mse_loss_backward(input_, target, "mean")
    sum_grad = mse_loss_backward(input_, target, "sum")
    assert np.allclose(mean_grad * input_.size, sum_grad)
    assert not np.allclose(mean_grad, sum_grad)


def test_backward_respects_grad_output_chain_rule():
    input_ = np.array([1.0, 2.0])
    target = np.array([0.0, 0.0])
    grad_at_one = mse_loss_backward(input_, target, "sum", grad_output=1.0)
    grad_at_three = mse_loss_backward(input_, target, "sum", grad_output=3.0)
    assert np.allclose(grad_at_three, grad_at_one * 3.0)


def test_backward_matches_finite_difference_gradient():
    rng = np.random.default_rng(0)
    input_ = rng.normal(size=6)
    target = rng.normal(size=6)
    analytic = mse_loss_backward(input_, target, "mean")

    eps = 1e-5
    numeric = np.empty(6)
    for i in range(6):
        plus, minus = input_.copy(), input_.copy()
        plus[i] += eps
        minus[i] -= eps
        numeric[i] = (
            mse_loss_forward(plus, target, "mean") - mse_loss_forward(minus, target, "mean")
        ) / (2 * eps)
    assert np.allclose(analytic, numeric, atol=1e-4)
