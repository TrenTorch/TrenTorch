import numpy as np
from _load import load_solution


_module = load_solution(__file__)
adamax_step = _module.adamax_step


def _raises_value_error(func):
    try:
        func()
    except ValueError:
        return True
    return False


def test_hand_computed_scalar_step():
    param = np.array(5.0)
    grad = np.array(2.0)
    m = np.array(0.0)
    u = np.array(0.0)

    lr = 0.1
    beta1 = 0.9
    beta2 = 0.999
    eps = 1.0e-8

    new_param, new_m, new_u = adamax_step(
        param,
        grad,
        m,
        u,
        lr,
        beta1,
        beta2,
        eps,
    )

    expected_m = 0.1 * 2.0
    expected_u = np.maximum(0.0, np.abs(2.0))
    expected_param = 5.0 - 0.1 * expected_m / (expected_u + eps)

    np.testing.assert_allclose(new_m, expected_m)
    np.testing.assert_allclose(new_u, expected_u)
    np.testing.assert_allclose(new_param, expected_param)


def test_hand_computed_vector_step():
    param = np.array([2.0, -3.0, 4.0])
    grad = np.array([1.0, -2.0, 3.0])
    m = np.array([0.1, 0.2, 0.3])
    u = np.array([0.5, 1.0, 1.5])

    lr = 0.01
    beta1 = 0.9
    beta2 = 0.999
    eps = 1.0e-8

    new_param, new_m, new_u = adamax_step(
        param,
        grad,
        m,
        u,
        lr,
        beta1,
        beta2,
        eps,
    )

    expected_m = 0.9 * m + 0.1 * grad
    expected_u = np.maximum(0.999 * u, np.abs(grad))
    expected_param = param - 0.01 * expected_m / (expected_u + eps)

    np.testing.assert_allclose(new_m, expected_m)
    np.testing.assert_allclose(new_u, expected_u)
    np.testing.assert_allclose(new_param, expected_param)


def test_zero_m_and_u_first_step():
    param = np.array([2.0, -4.0])
    grad = np.array([3.0, -2.0])
    m = np.zeros_like(param)
    u = np.zeros_like(param)

    lr = 0.1
    beta1 = 0.9
    beta2 = 0.999
    eps = 1.0e-8

    new_param, new_m, new_u = adamax_step(
        param,
        grad,
        m,
        u,
        lr,
        beta1,
        beta2,
        eps,
    )

    expected_m = 0.1 * grad
    expected_u = np.abs(grad)
    expected_param = param - 0.1 * expected_m / (expected_u + eps)

    np.testing.assert_allclose(new_m, expected_m)
    np.testing.assert_allclose(new_u, expected_u)
    np.testing.assert_allclose(new_param, expected_param)


def test_zero_gradient_keeps_parameter():
    param = np.array([1.0, -2.0, 3.0])
    grad = np.zeros(3)
    m = np.array([0.1, 0.2, 0.3])
    u = np.array([0.5, 1.0, 1.5])

    new_param, new_m, new_u = adamax_step(
        param,
        grad,
        m,
        u,
        0.1,
        0.9,
        0.999,
        1.0e-8,
    )

    assert np.array_equal(new_param, param)

    expected_m = 0.9 * m
    expected_u = 0.999 * u

    np.testing.assert_allclose(new_m, expected_m)
    np.testing.assert_allclose(new_u, expected_u)


def test_two_chained_steps_match_hand_computation():
    param = np.array(3.0)
    grad_1 = np.array(2.0)
    grad_2 = np.array(1.0)
    m = np.array(0.0)
    u = np.array(0.0)

    lr = 0.1
    beta1 = 0.9
    beta2 = 0.999
    eps = 1.0e-8

    param, m, u = adamax_step(
        param,
        grad_1,
        m,
        u,
        lr,
        beta1,
        beta2,
        eps,
    )

    expected_m_1 = 0.1 * 2.0
    expected_u_1 = 2.0
    expected_param_1 = (
        3.0 - 0.1 * expected_m_1 / (expected_u_1 + eps)
    )

    np.testing.assert_allclose(m, expected_m_1)
    np.testing.assert_allclose(u, expected_u_1)
    np.testing.assert_allclose(param, expected_param_1)

    param, m, u = adamax_step(
        param,
        grad_2,
        m,
        u,
        lr,
        beta1,
        beta2,
        eps,
    )

    expected_m_2 = 0.9 * expected_m_1 + 0.1 * 1.0
    expected_u_2 = np.maximum(0.999 * expected_u_1, 1.0)
    expected_param_2 = (
        expected_param_1
        - 0.1 * expected_m_2 / (expected_u_2 + eps)
    )

    np.testing.assert_allclose(m, expected_m_2)
    np.testing.assert_allclose(u, expected_u_2)
    np.testing.assert_allclose(param, expected_param_2)


def test_shape_mismatch_grad_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 2))
    m = np.zeros((2, 3))
    u = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            0.999,
            1.0e-8,
        )
    )


def test_shape_mismatch_m_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 3))
    m = np.zeros((3, 2))
    u = np.zeros((2, 3))

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            0.999,
            1.0e-8,
        )
    )


def test_shape_mismatch_u_raises_value_error():
    param = np.zeros((2, 3))
    grad = np.zeros((2, 3))
    m = np.zeros((2, 3))
    u = np.zeros((3, 2))

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            0.999,
            1.0e-8,
        )
    )


def test_non_positive_learning_rate_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    m = np.array([0.0])
    u = np.array([0.0])

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.0,
            0.9,
            0.999,
            1.0e-8,
        )
    )

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            -0.1,
            0.9,
            0.999,
            1.0e-8,
        )
    )


def test_beta1_out_of_range_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    m = np.array([0.0])
    u = np.array([0.0])

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            -0.1,
            0.999,
            1.0e-8,
        )
    )

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            1.0,
            0.999,
            1.0e-8,
        )
    )


def test_beta2_out_of_range_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    m = np.array([0.0])
    u = np.array([0.0])

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            -0.1,
            1.0e-8,
        )
    )

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            1.0,
            1.0e-8,
        )
    )


def test_non_positive_epsilon_raises_value_error():
    param = np.array([1.0])
    grad = np.array([1.0])
    m = np.array([0.0])
    u = np.array([0.0])

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            0.999,
            0.0,
        )
    )

    assert _raises_value_error(
        lambda: adamax_step(
            param,
            grad,
            m,
            u,
            0.1,
            0.9,
            0.999,
            -1.0e-8,
        )
    )


def test_inputs_are_not_modified():
    param = np.array([1.0, 2.0, 3.0])
    grad = np.array([0.1, 0.2, 0.3])
    m = np.array([0.4, 0.5, 0.6])
    u = np.array([0.7, 0.8, 0.9])

    param_before = param.copy()
    grad_before = grad.copy()
    m_before = m.copy()
    u_before = u.copy()

    adamax_step(
        param,
        grad,
        m,
        u,
        0.1,
        0.9,
        0.999,
        1.0e-8,
    )

    assert np.array_equal(param, param_before)
    assert np.array_equal(grad, grad_before)
    assert np.array_equal(m, m_before)
    assert np.array_equal(u, u_before)


def test_two_dimensional_parameter_keeps_shape():
    param = np.zeros((2, 3))
    grad = np.ones((2, 3))
    m = np.zeros((2, 3))
    u = np.zeros((2, 3))

    new_param, new_m, new_u = adamax_step(
        param,
        grad,
        m,
        u,
        0.1,
        0.9,
        0.999,
        1.0e-8,
    )

    assert new_param.shape == (2, 3)
    assert new_m.shape == (2, 3)
    assert new_u.shape == (2, 3)


def test_independent_oracle_over_twenty_steps():
    rng = np.random.default_rng(0)

    param = np.array([1.0, -2.0, 3.0, -4.0])
    m = np.zeros(4)
    u = np.zeros(4)

    lr = 0.01
    beta1 = 0.9
    beta2 = 0.999
    eps = 1.0e-8

    for _ in range(20):
        grad = rng.normal(size=4)

        expected_m = np.empty(4)
        expected_u = np.empty(4)
        expected_param = np.empty(4)

        for i in range(4):
            expected_m[i] = (
                beta1 * m[i] + (1 - beta1) * grad[i]
            )

            expected_u[i] = max(
                beta2 * u[i],
                np.abs(grad[i]),
            )

            expected_param[i] = (
                param[i]
                - lr * expected_m[i] / (expected_u[i] + eps)
            )

        actual_param, actual_m, actual_u = adamax_step(
            param,
            grad,
            m,
            u,
            lr,
            beta1,
            beta2,
            eps,
        )

        np.testing.assert_allclose(
            actual_m,
            expected_m,
        )
        np.testing.assert_allclose(
            actual_u,
            expected_u,
        )
        np.testing.assert_allclose(
            actual_param,
            expected_param,
        )

        param = actual_param
        m = actual_m
        u = actual_u
