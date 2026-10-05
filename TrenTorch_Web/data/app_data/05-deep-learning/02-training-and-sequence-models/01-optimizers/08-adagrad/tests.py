import numpy as np
from _load import load_solution


_module = load_solution(__file__)
adagrad_step = _module.adagrad_step


def _raises_value_error(func):
    try:
        func()
    except ValueError:
        return True
    return False


def test_hand_computed_scalar_step():
    param = np.array(5.0)
    grad = np.array(2.0)
    accum = np.array(0.0)
    lr = 0.1
    eps = 1.0e-8

    new_param, new_accum = adagrad_step(
        param,
        grad,
        accum,
        lr,
        eps,
    )

    expected_accum = 4.0
    expected_param = 5.0 - 0.1 * 2.0 / (
        np.sqrt(4.0) + eps
    )

    np.testing.assert_allclose(new_accum, expected_accum)
    np.testing.assert_allclose(new_param, expected_param)


def test_hand_computed_vector_step():
    param = np.array([4.0, -2.0, 3.0])
    grad = np.array([2.0, -1.0, 3.0])
    accum = np.array([1.0, 4.0, 9.0])
    lr = 0.2
    eps = 1.0e-8

    new_param, new_accum = adagrad_step(
        param,
        grad,
        accum,
        lr,
        eps,
    )

    expected_accum = np.array([
        5.0,
        5.0,
        18.0,
    ])

    expected_param = param - lr * grad / (
        np.sqrt(expected_accum) + eps
    )

    np.testing.assert_allclose(new_accum, expected_accum)
    np.testing.assert_allclose(new_param, expected_param)


def test_zero_accumulator_first_step():
    param = np.array([2.0, -4.0])
    grad = np.array([3.0, -2.0])
    accum = np.zeros_like(param)

    new_param, new_accum = adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    expected_accum = grad * grad
    expected_param = param - 0.1 * grad / (
        np.sqrt(expected_accum) + 1.0e-8
    )

    np.testing.assert_allclose(new_accum, expected_accum)
    np.testing.assert_allclose(new_param, expected_param)


def test_zero_gradient_keeps_parameter_and_accumulator():
    param = np.array([1.0, -2.0, 3.0])
    grad = np.zeros(3)
    accum = np.array([2.0, 4.0, 8.0])

    new_param, new_accum = adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    np.testing.assert_allclose(new_param, param)
    np.testing.assert_allclose(new_accum, accum)


def test_repeated_gradient_accumulates_squared_values():
    param = np.array(3.0)
    accum = np.array(0.0)
    grad = np.array(2.0)

    param, accum = adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    param, accum = adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    np.testing.assert_allclose(accum, 8.0)


def test_two_chained_steps_match_hand_computation():
    param = np.array(4.0)
    grad_1 = np.array(2.0)
    grad_2 = np.array(1.0)
    accum = np.array(0.0)
    lr = 0.1
    eps = 1.0e-8

    param, accum = adagrad_step(
        param,
        grad_1,
        accum,
        lr,
        eps,
    )

    expected_accum_1 = 4.0
    expected_param_1 = 4.0 - 0.1 * 2.0 / (
        np.sqrt(4.0) + eps
    )

    np.testing.assert_allclose(accum, expected_accum_1)
    np.testing.assert_allclose(param, expected_param_1)

    param, accum = adagrad_step(
        param,
        grad_2,
        accum,
        lr,
        eps,
    )

    expected_accum_2 = 5.0
    expected_param_2 = expected_param_1 - 0.1 * 1.0 / (
        np.sqrt(5.0) + eps
    )

    np.testing.assert_allclose(accum, expected_accum_2)
    np.testing.assert_allclose(param, expected_param_2)


def test_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 2))
    accum = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            0.1,
            1.0e-8,
        )
    )


def test_accumulator_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 3))
    accum = np.zeros((3, 2))

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            0.1,
            1.0e-8,
        )
    )


def test_non_positive_learning_rate_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    accum = np.array([0.0])

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            0.0,
            1.0e-8,
        )
    )

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            -0.1,
            1.0e-8,
        )
    )


def test_non_positive_epsilon_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    accum = np.array([0.0])

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            0.1,
            0.0,
        )
    )

    assert _raises_value_error(
        lambda: adagrad_step(
            param,
            grad,
            accum,
            0.1,
            -1.0e-8,
        )
    )


def test_inputs_are_not_modified():
    param = np.array([1.0, 2.0, 3.0])
    grad = np.array([0.1, 0.2, 0.3])
    accum = np.array([0.4, 0.5, 0.6])

    param_before = param.copy()
    grad_before = grad.copy()
    accum_before = accum.copy()

    adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    assert np.array_equal(param, param_before)
    assert np.array_equal(grad, grad_before)
    assert np.array_equal(accum, accum_before)


def test_two_dimensional_parameter_keeps_shape():
    param = np.zeros((2, 3))
    grad = np.ones((2, 3))
    accum = np.zeros((2, 3))

    new_param, new_accum = adagrad_step(
        param,
        grad,
        accum,
        0.1,
        1.0e-8,
    )

    assert new_param.shape == (2, 3)
    assert new_accum.shape == (2, 3)


def test_independent_oracle_over_twenty_steps():
    rng = np.random.default_rng(0)

    param = np.array([1.0, -2.0, 3.0, -4.0])
    accum = np.zeros(4)
    lr = 0.05
    eps = 1.0e-8

    for _ in range(20):
        grad = rng.normal(size=4)

        expected_accum = np.empty(4)
        expected_param = np.empty(4)

        for i in range(4):
            expected_accum[i] = (
                accum[i] + grad[i] * grad[i]
            )
            expected_param[i] = (
                param[i]
                - lr
                * grad[i]
                / (
                    np.sqrt(expected_accum[i])
                    + eps
                )
            )

        actual_param, actual_accum = adagrad_step(
            param,
            grad,
            accum,
            lr,
            eps,
        )

        np.testing.assert_allclose(
            actual_accum,
            expected_accum,
        )
        np.testing.assert_allclose(
            actual_param,
            expected_param,
        )

        param = actual_param
        accum = actual_accum
