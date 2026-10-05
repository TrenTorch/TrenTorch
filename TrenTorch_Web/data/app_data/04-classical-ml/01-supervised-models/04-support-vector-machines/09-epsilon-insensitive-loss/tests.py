"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
epsilon_insensitive_loss = _module.epsilon_insensitive_loss


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_residuals_inside_the_tube_cost_nothing():
    predictions = np.array([1.0, 2.0])
    targets = np.array([1.05, 1.95])
    assert np.isclose(epsilon_insensitive_loss(predictions, targets, epsilon=0.1), 0.0)


def test_residual_outside_the_tube_pays_the_distance_past_its_edge():
    # |3 - 1| = 2, minus epsilon 0.1 gives 1.9
    assert np.isclose(epsilon_insensitive_loss(np.array([3.0]), np.array([1.0]), epsilon=0.1), 1.9)


def test_residual_exactly_on_the_edge_costs_zero():
    assert np.isclose(epsilon_insensitive_loss(np.array([1.5]), np.array([1.0]), epsilon=0.5), 0.0)


def test_default_epsilon_is_point_one():
    assert np.isclose(epsilon_insensitive_loss(np.array([0.3]), np.array([0.0])), 0.2)


def test_epsilon_zero_is_the_mean_absolute_error():
    rng = np.random.default_rng(0)
    p = rng.normal(size=20)
    t = rng.normal(size=20)
    assert np.isclose(epsilon_insensitive_loss(p, t, epsilon=0.0), np.mean(np.abs(p - t)))


def test_loss_is_symmetric_in_the_sign_of_the_residual():
    assert np.isclose(
        epsilon_insensitive_loss(np.array([2.0]), np.array([0.0]), epsilon=0.1),
        epsilon_insensitive_loss(np.array([0.0]), np.array([2.0]), epsilon=0.1),
    )


def test_loss_is_never_negative():
    rng = np.random.default_rng(1)
    elementwise = epsilon_insensitive_loss(rng.normal(size=50), rng.normal(size=50), reduction="none")
    assert np.all(elementwise >= 0.0)


def test_sum_reduction_adds_the_elementwise_losses():
    p = np.array([0.0, 5.0, 10.0])
    t = np.array([0.0, 0.0, 0.0])
    assert np.isclose(epsilon_insensitive_loss(p, t, epsilon=1.0, reduction="sum"), 4.0 + 9.0)


def test_none_reduction_returns_the_elementwise_array():
    p = np.array([0.0, 3.0])
    t = np.array([0.0, 0.0])
    result = epsilon_insensitive_loss(p, t, epsilon=1.0, reduction="none")
    assert isinstance(result, np.ndarray)
    assert np.allclose(result, [0.0, 2.0])


def test_invalid_reduction_raises():
    assert _raises_value_error(epsilon_insensitive_loss, np.array([1.0]), np.array([1.0]), reduction="median")


def test_larger_epsilon_never_increases_the_loss():
    rng = np.random.default_rng(2)
    p = rng.normal(size=30)
    t = rng.normal(size=30)
    small = epsilon_insensitive_loss(p, t, epsilon=0.1)
    large = epsilon_insensitive_loss(p, t, epsilon=0.5)
    assert large <= small


def test_matches_an_explicit_loop():
    p = np.array([0.5, -1.0, 2.0])
    t = np.array([0.0, 0.0, 0.0])
    eps = 0.3
    expected = np.mean([max(0.0, abs(a - b) - eps) for a, b in zip(p, t)])
    assert np.isclose(epsilon_insensitive_loss(p, t, epsilon=eps), expected)


def test_does_not_modify_its_inputs():
    p = np.array([1.0, 2.0])
    t = np.array([0.0, 4.0])
    p_before, t_before = p.copy(), t.copy()
    epsilon_insensitive_loss(p, t)
    assert np.array_equal(p, p_before)
    assert np.array_equal(t, t_before)
