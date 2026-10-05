import numpy as np
from _load import load_solution


_module = load_solution(__file__)
adadelta_step = _module.adadelta_step


def _raises_value_error(func):
    try:
        func()
    except ValueError:
        return True
    return False


def test_hand_computed_scalar_step():
    param = np.array(5.0)
    grad = np.array(2.0)
    square_avg = np.array(0.0)
    acc_delta = np.array(0.0)

    lr = 1.0
    rho = 0.9
    eps = 1.0e-6

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        lr,
        rho,
        eps,
    )

    expected_square_avg = 0.1 * 4.0
    expected_delta = (
        np.sqrt(eps)
        / np.sqrt(expected_square_avg + eps)
        * 2.0
    )
    expected_param = 5.0 - expected_delta
    expected_acc_delta = 0.1 * expected_delta * expected_delta

    np.testing.assert_allclose(
        new_square_avg,
        expected_square_avg,
    )
    np.testing.assert_allclose(
        new_param,
        expected_param,
    )
    np.testing.assert_allclose(
        new_acc_delta,
        expected_acc_delta,
    )


def test_hand_computed_vector_step():
    param = np.array([2.0, -3.0, 4.0])
    grad = np.array([1.0, -2.0, 3.0])
    square_avg = np.array([0.5, 1.0, 2.0])
    acc_delta = np.array([0.2, 0.4, 0.8])

    lr = 0.5
    rho = 0.5
    eps = 1.0e-6

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        lr,
        rho,
        eps,
    )

    expected_square_avg = (
        0.5 * square_avg
        + 0.5 * grad * grad
    )

    expected_delta = (
        np.sqrt(acc_delta + eps)
        / np.sqrt(expected_square_avg + eps)
        * grad
    )

    expected_param = param - 0.5 * expected_delta

    expected_acc_delta = (
        0.5 * acc_delta
        + 0.5 * expected_delta * expected_delta
    )

    np.testing.assert_allclose(
        new_square_avg,
        expected_square_avg,
    )
    np.testing.assert_allclose(
        new_param,
        expected_param,
    )
    np.testing.assert_allclose(
        new_acc_delta,
        expected_acc_delta,
    )


def test_zero_states_first_step():
    param = np.array([2.0, -4.0])
    grad = np.array([3.0, -2.0])
    square_avg = np.zeros_like(param)
    acc_delta = np.zeros_like(param)

    lr = 1.0
    rho = 0.9
    eps = 1.0e-6

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        lr,
        rho,
        eps,
    )

    expected_square_avg = (
        (1.0 - rho) * grad * grad
    )

    expected_delta = (
        np.sqrt(eps)
        / np.sqrt(expected_square_avg + eps)
        * grad
    )

    expected_param = param - expected_delta

    expected_acc_delta = (
        (1.0 - rho)
        * expected_delta
        * expected_delta
    )

    np.testing.assert_allclose(
        new_square_avg,
        expected_square_avg,
    )
    np.testing.assert_allclose(
        new_param,
        expected_param,
    )
    np.testing.assert_allclose(
        new_acc_delta,
        expected_acc_delta,
    )


def test_zero_gradient_keeps_parameter():
    param = np.array([1.0, -2.0, 3.0])
    grad = np.zeros(3)
    square_avg = np.array([0.5, 1.0, 2.0])
    acc_delta = np.array([0.2, 0.4, 0.8])

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        0.5,
        0.9,
        1.0e-6,
    )

    assert np.array_equal(new_param, param)

    expected_square_avg = 0.9 * square_avg
    expected_acc_delta = 0.9 * acc_delta

    np.testing.assert_allclose(
        new_square_avg,
        expected_square_avg,
    )
    np.testing.assert_allclose(
        new_acc_delta,
        expected_acc_delta,
    )


def test_two_chained_steps_match_hand_computation():
    param = np.array(3.0)
    square_avg = np.array(0.0)
    acc_delta = np.array(0.0)

    lr = 1.0
    rho = 0.5
    eps = 1.0e-6

    grad_1 = np.array(2.0)

    param, square_avg, acc_delta = adadelta_step(
        param,
        grad_1,
        square_avg,
        acc_delta,
        lr,
        rho,
        eps,
    )

    expected_square_avg_1 = 0.5 * 4.0
    expected_delta_1 = (
        np.sqrt(eps)
        / np.sqrt(expected_square_avg_1 + eps)
        * 2.0
    )
    expected_param_1 = 3.0 - expected_delta_1
    expected_acc_delta_1 = (
        0.5 * expected_delta_1 * expected_delta_1
    )

    np.testing.assert_allclose(
        param,
        expected_param_1,
    )
    np.testing.assert_allclose(
        square_avg,
        expected_square_avg_1,
    )
    np.testing.assert_allclose(
        acc_delta,
        expected_acc_delta_1,
    )

    grad_2 = np.array(1.0)

    param, square_avg, acc_delta = adadelta_step(
        param,
        grad_2,
        square_avg,
        acc_delta,
        lr,
        rho,
        eps,
    )

    expected_square_avg_2 = (
        0.5 * expected_square_avg_1
        + 0.5 * 1.0
    )

    expected_delta_2 = (
        np.sqrt(expected_acc_delta_1 + eps)
        / np.sqrt(expected_square_avg_2 + eps)
        * 1.0
    )

    expected_param_2 = (
        expected_param_1 - expected_delta_2
    )

    expected_acc_delta_2 = (
        0.5 * expected_acc_delta_1
        + 0.5 * expected_delta_2 * expected_delta_2
    )

    np.testing.assert_allclose(
        param,
        expected_param_2,
    )
    np.testing.assert_allclose(
        square_avg,
        expected_square_avg_2,
    )
    np.testing.assert_allclose(
        acc_delta,
        expected_acc_delta_2,
    )


def test_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 2))
    square_avg = np.zeros((2, 3))
    acc_delta = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            0.9,
            1.0e-6,
        )
    )


def test_square_average_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 3))
    square_avg = np.zeros((3, 2))
    acc_delta = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            0.9,
            1.0e-6,
        )
    )


def test_acc_delta_shape_mismatch_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 3))
    square_avg = np.zeros((2, 3))
    acc_delta = np.zeros((3, 2))

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            0.9,
            1.0e-6,
        )
    )


def test_non_positive_learning_rate_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    square_avg = np.array([0.0])
    acc_delta = np.array([0.0])

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            0.0,
            0.9,
            1.0e-6,
        )
    )

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            -0.1,
            0.9,
            1.0e-6,
        )
    )


def test_rho_out_of_range_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    square_avg = np.array([0.0])
    acc_delta = np.array([0.0])

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            -0.1,
            1.0e-6,
        )
    )

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            1.0,
            1.0e-6,
        )
    )


def test_non_positive_epsilon_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    square_avg = np.array([0.0])
    acc_delta = np.array([0.0])

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            0.9,
            0.0,
        )
    )

    assert _raises_value_error(
        lambda: adadelta_step(
            param,
            grad,
            square_avg,
            acc_delta,
            1.0,
            0.9,
            -1.0e-6,
        )
    )


def test_inputs_are_not_modified():
    param = np.array([1.0, 2.0, 3.0])
    grad = np.array([0.1, 0.2, 0.3])
    square_avg = np.array([0.4, 0.5, 0.6])
    acc_delta = np.array([0.7, 0.8, 0.9])

    param_before = param.copy()
    grad_before = grad.copy()
    square_avg_before = square_avg.copy()
    acc_delta_before = acc_delta.copy()

    adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        1.0,
        0.9,
        1.0e-6,
    )

    assert np.array_equal(param, param_before)
    assert np.array_equal(grad, grad_before)
    assert np.array_equal(square_avg, square_avg_before)
    assert np.array_equal(acc_delta, acc_delta_before)


def test_two_dimensional_parameter_keeps_shape():
    param = np.zeros((2, 3))
    grad = np.ones((2, 3))
    square_avg = np.zeros((2, 3))
    acc_delta = np.zeros((2, 3))

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        1.0,
        0.9,
        1.0e-6,
    )

    assert new_param.shape == (2, 3)
    assert new_square_avg.shape == (2, 3)
    assert new_acc_delta.shape == (2, 3)


def test_rho_zero_uses_current_values_only():
    param = np.array([2.0, -3.0])
    grad = np.array([1.0, -2.0])
    square_avg = np.array([100.0, 100.0])
    acc_delta = np.array([25.0, 36.0])

    new_param, new_square_avg, new_acc_delta = adadelta_step(
        param,
        grad,
        square_avg,
        acc_delta,
        1.0,
        0.0,
        1.0e-6,
    )

    expected_square_avg = grad * grad
    expected_delta = (
        np.sqrt(acc_delta + 1.0e-6)
        / np.sqrt(expected_square_avg + 1.0e-6)
        * grad
    )
    expected_param = param - expected_delta
    expected_acc_delta = expected_delta * expected_delta

    np.testing.assert_allclose(
        new_square_avg,
        expected_square_avg,
    )
    np.testing.assert_allclose(
        new_param,
        expected_param,
    )
    np.testing.assert_allclose(
        new_acc_delta,
        expected_acc_delta,
    )


def test_independent_oracle_over_twenty_steps():
    rng = np.random.default_rng(0)

    param = np.array([1.0, -2.0, 3.0, -4.0])
    square_avg = np.zeros(4)
    acc_delta = np.zeros(4)

    lr = 0.5
    rho = 0.9
    eps = 1.0e-6

    for _ in range(20):
        grad = rng.normal(size=4)

        expected_square_avg = np.empty(4)
        expected_delta = np.empty(4)
        expected_param = np.empty(4)
        expected_acc_delta = np.empty(4)

        for i in range(4):
            expected_square_avg[i] = (
                rho * square_avg[i]
                + (1.0 - rho) * grad[i] * grad[i]
            )

            expected_delta[i] = (
                np.sqrt(acc_delta[i] + eps)
                / np.sqrt(
                    expected_square_avg[i] + eps
                )
                * grad[i]
            )

            expected_param[i] = (
                param[i] - lr * expected_delta[i]
            )

            expected_acc_delta[i] = (
                rho * acc_delta[i]
                + (1.0 - rho)
                * expected_delta[i]
                * expected_delta[i]
            )

        actual_param, actual_square_avg, actual_acc_delta = (
            adadelta_step(
                param,
                grad,
                square_avg,
                acc_delta,
                lr,
                rho,
                eps,
            )
        )

        np.testing.assert_allclose(
            actual_param,
            expected_param,
        )
        np.testing.assert_allclose(
            actual_square_avg,
            expected_square_avg,
        )
        np.testing.assert_allclose(
            actual_acc_delta,
            expected_acc_delta,
        )

        param = actual_param
        square_avg = actual_square_avg
        acc_delta = actual_acc_delta
