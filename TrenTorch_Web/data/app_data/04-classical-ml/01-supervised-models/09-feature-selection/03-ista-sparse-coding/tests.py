"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
soft_threshold = _module.soft_threshold
sparse_code = _module.sparse_code


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_soft_threshold_known_values():
    z = np.array([3.0, 0.5, -2.0, -0.2])
    assert np.allclose(soft_threshold(z, 1.0), [2.0, 0.0, -1.0, 0.0])


def test_soft_threshold_with_zero_threshold_is_identity():
    z = np.array([1.5, -0.3, 0.0])
    assert np.allclose(soft_threshold(z, 0.0), z)


def test_soft_threshold_keeps_sign():
    z = np.array([5.0, -5.0])
    out = soft_threshold(z, 2.0)
    assert np.sign(out[0]) == 1 and np.sign(out[1]) == -1


def test_one_iteration_on_identity_is_soft_threshold_of_y():
    # D = I, L = 1, x0 = 0: one step gives soft_threshold(y, lam).
    y = np.array([3.0, 0.5, -2.0])
    x = sparse_code(np.eye(3), y, lam=1.0, iters=1)
    assert np.allclose(x, [2.0, 0.0, -1.0])


def test_zero_penalty_on_identity_returns_y_after_one_step():
    y = np.array([1.0, -4.0, 0.25])
    assert np.allclose(sparse_code(np.eye(3), y, lam=0.0, iters=1), y)


def test_zero_penalty_converges_to_least_squares():
    rng = np.random.default_rng(0)
    D = rng.normal(size=(10, 3))
    y = rng.normal(size=10)
    lstsq = np.linalg.lstsq(D, y, rcond=None)[0]
    assert np.allclose(sparse_code(D, y, lam=0.0, iters=20000), lstsq, atol=1e-6)


def test_large_penalty_gives_all_zeros():
    rng = np.random.default_rng(1)
    D = rng.normal(size=(8, 4))
    y = rng.normal(size=8)
    lam = np.max(np.abs(D.T @ y)) + 1.0
    assert np.array_equal(sparse_code(D, y, lam=lam, iters=50), np.zeros(4))


def test_zero_iterations_returns_zeros():
    D = np.eye(3)
    assert np.array_equal(sparse_code(D, np.ones(3), lam=0.1, iters=0), np.zeros(3))


def test_objective_is_no_larger_than_at_zero():
    rng = np.random.default_rng(2)
    D = rng.normal(size=(12, 6))
    y = rng.normal(size=12)
    lam = 0.5

    def objective(x):
        return 0.5 * np.sum((y - D @ x) ** 2) + lam * np.sum(np.abs(x))

    x = sparse_code(D, y, lam=lam, iters=500)
    assert objective(x) <= objective(np.zeros(6)) + 1e-12


def test_solution_is_sparser_with_larger_penalty():
    rng = np.random.default_rng(3)
    D = rng.normal(size=(15, 8))
    y = rng.normal(size=15)
    weak = sparse_code(D, y, lam=0.05, iters=2000)
    strong = sparse_code(D, y, lam=2.0, iters=2000)
    assert np.count_nonzero(strong) <= np.count_nonzero(weak)


def test_output_length_is_number_of_atoms():
    rng = np.random.default_rng(4)
    D = rng.normal(size=(5, 7))
    assert sparse_code(D, rng.normal(size=5)).shape == (7,)


def test_zero_matrix_uses_unit_step_and_returns_zeros():
    assert np.array_equal(sparse_code(np.zeros((3, 2)), np.ones(3), lam=0.0, iters=5), np.zeros(2))


def test_negative_lambda_raises():
    assert _raises_value_error(sparse_code, np.eye(2), np.ones(2), -0.1, 10)


def test_negative_iterations_raise():
    assert _raises_value_error(sparse_code, np.eye(2), np.ones(2), 0.1, -1)


def test_length_mismatch_raises():
    assert _raises_value_error(sparse_code, np.eye(3), np.ones(2), 0.1, 10)


def test_does_not_modify_inputs():
    D = np.array([[1.0, 0.5], [0.0, 1.0], [0.2, 0.3]])
    y = np.array([1.0, -1.0, 0.5])
    D0, y0 = D.copy(), y.copy()
    sparse_code(D, y, lam=0.1, iters=30)
    assert np.array_equal(D, D0) and np.array_equal(y, y0)
