import numpy as np
from _load import load_solution


_module = load_solution(__file__)
nesterov_step = _module.nesterov_step


def _raises_value_error(func):
    try:
        func()
    except ValueError:
        return True
    return False


def test_hand_computed_scalar_step():
    param = np.array(5.0)
    grad = np.array(2.0)
    velocity = np.array(3.0)

    new_param, new_velocity = nesterov_step(
        param,
        grad,
        velocity,
        0.1,
        0.9,
    )

    expected_velocity = 0.9 * 3.0 + 2.0
    expected_param = 5.0 - 0.1 * (
        2.0 + 0.9 * expected_velocity
    )

    np.testing.assert_allclose(new_velocity, expected_velocity)
    np.testing.assert_allclose(new_param, expected_param)


def test_hand_computed_vector_step():
    param = np.array([1.0, -2.0, 3.0])
    grad = np.array([0.5, -1.0, 2.0])
    velocity = np.array([2.0, 1.0, -0.5])

    new_param, new_velocity = nesterov_step(
        param,
        grad,
        velocity,
        0.2,
        0.5,
    )

    expected_velocity = np.array([1.5, -0.5, 1.75])
    expected_param = np.array([0.75, -1.75, 2.425])

    np.testing.assert_allclose(new_velocity, expected_velocity)
    np.testing.assert_allclose(new_param, expected_param)


def test_zero_velocity_one_step():
    param = np.array(1.0)
    grad = np.array(2.0)
    velocity = np.array(0.0)

    new_param, new_velocity = nesterov_step(
        param,
        grad,
        velocity,
        0.1,
        0.9,
    )

    np.testing.assert_allclose(new_velocity, 2.0)
    np.testing.assert_allclose(new_param, 0.62)


def test_zero_momentum_equals_sgd():
    param = np.array([3.0, -4.0, 5.0])
    grad = np.array([0.5, -2.0, 1.5])
    velocity = np.array([8.0, 7.0, 6.0])
    lr = 0.25

    new_param, new_velocity = nesterov_step(
        param,
        grad,
        velocity,
        lr,
        0.0,
    )

    expected_param = param - lr * grad

    np.testing.assert_allclose(new_param, expected_param)
    np.testing.assert_allclose(new_velocity, grad)


def test_two_chained_steps():
    param = np.array(1.0)
    velocity = np.array(0.0)

    param, velocity = nesterov_step(
        param,
        np.array(1.0),
        velocity,
        0.1,
        0.5,
    )

    param, velocity = nesterov_step(
        param,
        np.array(2.0),
        velocity,
        0.1,
        0.5,
    )

    np.testing.assert_allclose(param, 0.525)


def test_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 2))
    velocity = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: nesterov_step(
            param,
            grad,
            velocity,
            0.1,
            0.9,
        )
    )


def test_momentum_out_of_range_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    velocity = np.array([0.0])

    assert _raises_value_error(
        lambda: nesterov_step(
            param,
            grad,
            velocity,
            0.1,
            1.0,
        )
    )

    assert _raises_value_error(
        lambda: nesterov_step(
            param,
            grad,
            velocity,
            0.1,
            -0.1,
        )
    )


def test_inputs_are_not_modified():
    param = np.array([1.0, 2.0, 3.0])
    grad = np.array([0.1, 0.2, 0.3])
    velocity = np.array([0.4, 0.5, 0.6])

    param_before = param.copy()
    grad_before = grad.copy()
    velocity_before = velocity.copy()

    nesterov_step(
        param,
        grad,
        velocity,
        0.1,
        0.9,
    )

    assert np.array_equal(param, param_before)
    assert np.array_equal(grad, grad_before)
    assert np.array_equal(velocity, velocity_before)


def test_two_dimensional_parameter_keeps_shape():
    param = np.zeros((2, 3))
    grad = np.ones((2, 3))
    velocity = np.zeros((2, 3))

    new_param, new_velocity = nesterov_step(
        param,
        grad,
        velocity,
        0.1,
        0.9,
    )

    assert new_param.shape == (2, 3)
    assert new_velocity.shape == (2, 3)


def test_nesterov_differs_from_classical_momentum():
    param = np.array(0.0)
    grad = np.array(1.0)
    velocity = np.array(0.0)

    new_param, _ = nesterov_step(
        param,
        grad,
        velocity,
        1.0,
        0.5,
    )

    classical_param = -1.0

    assert np.isclose(new_param, -1.5)
    assert not np.isclose(new_param, classical_param)


def test_independent_oracle_over_twenty_steps():
    rng = np.random.default_rng(0)

    param = np.array([1.0, -2.0, 3.0, -4.0])
    velocity = np.zeros(4)
    lr = 0.07
    momentum = 0.8

    for _ in range(20):
        grad = rng.normal(size=4)

        expected_velocity = np.empty(4)
        expected_param = np.empty(4)

        for i in range(4):
            expected_velocity[i] = (
                momentum * velocity[i] + grad[i]
            )
            expected_param[i] = (
                param[i]
                - lr
                * (
                    grad[i]
                    + momentum * expected_velocity[i]
                )
            )

        actual_param, actual_velocity = nesterov_step(
            param,
            grad,
            velocity,
            lr,
            momentum,
        )

        np.testing.assert_allclose(
            actual_velocity,
            expected_velocity,
        )
        np.testing.assert_allclose(
            actual_param,
            expected_param,
        )

        param = actual_param
        velocity = actual_velocity


def test_nesterov_beats_classical_on_quadratic():
    lr = 0.1
    momentum = 0.9

    nesterov_x = 5.0
    nesterov_velocity = 0.0

    classical_x = 5.0
    classical_velocity = 0.0

    for _ in range(50):
        nesterov_grad = nesterov_x

        nesterov_velocity = (
            momentum * nesterov_velocity + nesterov_grad
        )
        nesterov_x = (
            nesterov_x
            - lr
            * (
                nesterov_grad
                + momentum * nesterov_velocity
            )
        )

        classical_grad = classical_x

        classical_velocity = (
            momentum * classical_velocity + classical_grad
        )
        classical_x = (
            classical_x
            - lr * classical_velocity
        )

    assert abs(nesterov_x) < abs(classical_x)
