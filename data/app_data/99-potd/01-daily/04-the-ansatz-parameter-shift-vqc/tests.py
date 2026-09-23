"""
pytest data/app_data/12-quantum-computing/01-variational-circuits/01-the-ansatz-parameter-shift-vqc/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
circuit_output = _module.circuit_output
train_and_predict = _module.train_and_predict


def test_example_one_matches_the_specs_worked_derivation():
    X = np.array([[0.5, -0.3], [1.0, 0.2]])
    y = np.array([1.0, -1.0])
    theta_init = np.array([0.1, -0.1])
    queries = np.array([[0.4, 0.4], [-0.2, 0.6]])
    predictions = train_and_predict(X, y, n=2, L=1, theta_init=theta_init, eta=0.5, T=3, queries=queries)
    assert np.allclose(predictions, [0.571864, 0.794600], atol=1e-4)


def test_example_two_matches_the_specs_worked_derivation():
    X = np.array([[0.3, 0.7], [-0.5, 0.1], [0.9, -0.4]])
    y = np.array([1.0, -1.0, 0.5])
    theta_init = np.array([0.2, 0.0, -0.1, 0.3])
    queries = np.array([[0.0, 0.0], [0.5, -0.5]])
    predictions = train_and_predict(X, y, n=2, L=2, theta_init=theta_init, eta=0.3, T=2, queries=queries)
    assert np.allclose(predictions, [0.861363, 0.967439], atol=1e-4)


def test_output_is_always_within_the_valid_z_expectation_range():
    rng = np.random.default_rng(0)
    for n, L in [(1, 1), (2, 3), (4, 2)]:
        x = rng.uniform(-5, 5, size=n)
        theta = rng.uniform(-5, 5, size=(L, n))
        p = circuit_output(x, theta, n=n, L=L)
        assert -1.0 - 1e-9 <= p <= 1.0 + 1e-9


def test_single_qubit_matches_the_closed_form_rotation_composition():
    # For n=1 the entangling chain is always empty, so every RY in the
    # circuit acts on the SAME qubit about the SAME axis -- rotations
    # about a shared axis compose additively, giving an exact,
    # solver-independent closed form: p = cos(x + sum(theta)).
    rng = np.random.default_rng(1)
    for _ in range(5):
        x0 = rng.uniform(-3.0, 3.0)
        L = int(rng.integers(1, 5))
        thetas = rng.uniform(-3.0, 3.0, size=L)
        p = circuit_output(np.array([x0]), thetas.reshape(L, 1), n=1, L=L)
        expected = np.cos(x0 + thetas.sum())
        assert np.isclose(p, expected, atol=1e-9)


def test_t_zero_is_a_direct_forward_pass_with_no_training():
    X = np.array([[0.5, -0.3], [1.0, 0.2]])
    y = np.array([1.0, -1.0])
    theta_init = np.array([0.1, -0.1])
    queries = np.array([[0.4, 0.4]])
    predicted = train_and_predict(X, y, n=2, L=1, theta_init=theta_init, eta=0.5, T=0, queries=queries)
    direct = circuit_output(np.array([0.4, 0.4]), theta_init.reshape(1, 2), n=2, L=1)
    assert np.isclose(predicted[0], direct, atol=1e-9)


def test_one_gradient_step_matches_an_independent_finite_difference_oracle():
    # Cross-checks the ENTIRE parameter-shift + gradient-descent pipeline
    # against plain central-difference numerical differentiation of the
    # loss -- an independent oracle that never calls the parameter-shift
    # formula at all, so a sign-flipped or mis-indexed shift rule would
    # diverge from it.
    X = np.array([[0.2, -0.4], [0.6, 0.1], [-0.3, 0.5]])
    y = np.array([0.3, -0.6, 0.2])
    theta0 = np.array([[0.15, -0.25]])
    eta = 0.4
    eps = 1e-6

    def loss(theta):
        preds = np.array([circuit_output(X[k], theta, 2, 1) for k in range(X.shape[0])])
        return np.mean((preds - y) ** 2)

    numeric_grad = np.zeros_like(theta0)
    for idx in np.ndindex(theta0.shape):
        plus, minus = theta0.copy(), theta0.copy()
        plus[idx] += eps
        minus[idx] -= eps
        numeric_grad[idx] = (loss(plus) - loss(minus)) / (2 * eps)

    expected_theta = theta0 - eta * numeric_grad
    queries = np.array([[0.1, 0.1]])
    expected_prediction = circuit_output(queries[0], expected_theta, n=2, L=1)

    predicted = train_and_predict(X, y, n=2, L=1, theta_init=theta0.flatten(), eta=eta, T=1, queries=queries)
    assert np.allclose(predicted, [expected_prediction], atol=1e-4)


def test_four_qubits_and_four_layers_stay_finite_and_well_shaped():
    rng = np.random.default_rng(2)
    n, L, n_train, m = 4, 4, 6, 3
    X = rng.uniform(-2, 2, size=(n_train, n))
    y = rng.uniform(-2, 2, size=n_train)
    theta_init = rng.uniform(-1, 1, size=L * n)
    queries = rng.uniform(-2, 2, size=(m, n))
    predictions = train_and_predict(X, y, n=n, L=L, theta_init=theta_init, eta=0.2, T=3, queries=queries)
    assert predictions.shape == (m,)
    assert np.all(np.isfinite(predictions))
    assert np.all(predictions >= -1.0 - 1e-9)
    assert np.all(predictions <= 1.0 + 1e-9)


def test_targets_outside_valid_range_still_reduce_training_loss():
    # Large-residual targets (impossible to fit exactly, since the model
    # is bounded to [-1, 1]) still must push the loss down over training,
    # confirming gradient direction/magnitude stay correct even when the
    # model can never reach zero loss.
    rng = np.random.default_rng(3)
    X = rng.uniform(-1, 1, size=(5, 2))
    y = np.array([5.0, -6.0, 4.5, -5.5, 6.0])
    theta_init = np.zeros(2)

    def mean_loss(theta_flat, T):
        preds = train_and_predict(X, y, n=2, L=1, theta_init=theta_flat, eta=0.3, T=T, queries=X)
        return np.mean((preds - y) ** 2)

    loss_before = mean_loss(theta_init, T=0)
    loss_after = mean_loss(theta_init, T=15)
    assert loss_after < loss_before


def test_large_eta_does_not_crash_and_stays_in_valid_output_range():
    rng = np.random.default_rng(4)
    X = rng.uniform(-2, 2, size=(4, 2))
    y = rng.uniform(-3, 3, size=4)
    theta_init = rng.uniform(-1, 1, size=2)
    queries = rng.uniform(-2, 2, size=(3, 2))
    predictions = train_and_predict(X, y, n=2, L=1, theta_init=theta_init, eta=2.0, T=10, queries=queries)
    assert np.all(np.isfinite(predictions))
    assert np.all(predictions >= -1.0 - 1e-9)
    assert np.all(predictions <= 1.0 + 1e-9)


def test_predict_returns_one_value_per_query():
    rng = np.random.default_rng(5)
    X = rng.uniform(-1, 1, size=(6, 3))
    y = rng.uniform(-1, 1, size=6)
    theta_init = rng.uniform(-1, 1, size=2 * 3)
    queries = rng.uniform(-1, 1, size=(7, 3))
    predictions = train_and_predict(X, y, n=3, L=2, theta_init=theta_init, eta=0.2, T=2, queries=queries)
    assert predictions.shape == (7,)
