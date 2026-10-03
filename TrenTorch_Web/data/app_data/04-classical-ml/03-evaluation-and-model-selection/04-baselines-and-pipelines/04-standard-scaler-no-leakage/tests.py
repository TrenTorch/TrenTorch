"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
standard_scale_no_leakage = _module.standard_scale_no_leakage


def test_scaled_training_columns_have_zero_mean_and_unit_std():
    rng = np.random.default_rng(0)
    X_train = rng.normal(loc=5.0, scale=3.0, size=(100, 3))
    scaled_train, _ = standard_scale_no_leakage(X_train, X_train[:10])
    assert np.allclose(scaled_train.mean(axis=0), 0.0, atol=1e-10)
    assert np.allclose(scaled_train.std(axis=0), 1.0, atol=1e-10)


def test_test_rows_use_the_training_statistics():
    # train column [0, 2]: mean 1, std 1. Test value 3 maps to (3 - 1) / 1 = 2.
    X_train = np.array([[0.0], [2.0]])
    X_test = np.array([[3.0]])
    _, scaled_test = standard_scale_no_leakage(X_train, X_test)
    assert np.isclose(scaled_test[0, 0], 2.0)


def test_test_data_does_not_change_the_scaling_of_the_train_data():
    X_train = np.array([[0.0], [2.0]])
    scaled_a, _ = standard_scale_no_leakage(X_train, np.array([[100.0]]))
    scaled_b, _ = standard_scale_no_leakage(X_train, np.array([[-100.0]]))
    assert np.array_equal(scaled_a, scaled_b)


def test_shifted_test_data_is_not_re_centered():
    rng = np.random.default_rng(1)
    X_train = rng.normal(size=(50, 2))
    X_test = rng.normal(loc=10.0, size=(50, 2))
    _, scaled_test = standard_scale_no_leakage(X_train, X_test)
    assert np.all(np.abs(scaled_test.mean(axis=0)) > 5.0)


def test_zero_variance_column_becomes_all_zeros():
    X_train = np.array([[4.0, 1.0], [4.0, 3.0]])
    X_test = np.array([[4.0, 2.0], [9.0, 2.0]])
    scaled_train, scaled_test = standard_scale_no_leakage(X_train, X_test)
    assert np.allclose(scaled_train[:, 0], 0.0)
    assert np.allclose(scaled_test[:, 0], [0.0, 5.0])


def test_no_nan_appears_when_a_column_is_constant():
    X_train = np.full((4, 2), 7.0)
    scaled_train, scaled_test = standard_scale_no_leakage(X_train, np.full((2, 2), 8.0))
    assert np.all(np.isfinite(scaled_train))
    assert np.all(np.isfinite(scaled_test))


def test_output_shapes_match_the_inputs():
    scaled_train, scaled_test = standard_scale_no_leakage(np.ones((5, 3)) * 2.0, np.ones((2, 3)))
    assert scaled_train.shape == (5, 3)
    assert scaled_test.shape == (2, 3)


def test_matches_manual_computation_on_a_small_example():
    X_train = np.array([[1.0, 10.0], [3.0, 30.0]])
    X_test = np.array([[5.0, 20.0]])
    mean = np.array([2.0, 20.0])
    std = np.array([1.0, 10.0])
    _, scaled_test = standard_scale_no_leakage(X_train, X_test)
    assert np.allclose(scaled_test, (X_test - mean) / std)


def test_accepts_integer_inputs_and_returns_floats():
    scaled_train, _ = standard_scale_no_leakage(np.array([[1, 2], [3, 4]]), np.array([[1, 2]]))
    assert np.issubdtype(scaled_train.dtype, np.floating)


def test_does_not_modify_its_inputs():
    X_train = np.array([[1.0], [3.0]])
    X_test = np.array([[2.0]])
    train_before, test_before = X_train.copy(), X_test.copy()
    standard_scale_no_leakage(X_train, X_test)
    assert np.array_equal(X_train, train_before)
    assert np.array_equal(X_test, test_before)


def test_returns_a_tuple_of_two_arrays():
    result = standard_scale_no_leakage(np.array([[1.0], [2.0]]), np.array([[1.5]]))
    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(isinstance(part, np.ndarray) for part in result)


def test_training_and_test_outputs_use_the_same_transformation():
    X_train = np.array([[0.0, 4.0], [2.0, 8.0]])
    scaled_train, scaled_test = standard_scale_no_leakage(X_train, X_train)
    assert np.allclose(scaled_train, scaled_test)
