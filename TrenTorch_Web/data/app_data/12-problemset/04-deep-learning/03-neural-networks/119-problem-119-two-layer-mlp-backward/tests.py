"""Contract tests with examples and targeted valid-input cases."""
import numpy as np

from _load import load_solution

solve = load_solution(__file__).solve

def test_01_visible_example():
    result = solve([[1, 2]], [[1]], [[1, 0], [0, 1]], [[2], [3]], ([[1, -1]], [[1, 0]]))
    expected = ([[2, 0]], [[2, 0], [4, 0]], [2, 0], [[1], [0]], [1])
    for actual, want in zip(result, expected):
        np.testing.assert_allclose(actual, want)

def test_02_single_hidden_unit():
    result = solve([[2]], [[3]], [[1]], [[4]], ([[1]], [[1]]))
    expected = ([[12]], [[24]], [12], [[3]], [3])
    for actual, want in zip(result, expected):
        np.testing.assert_allclose(actual, want)

def test_03_inactive_relu_blocks_hidden_gradient():
    result = solve([[1]], [[1]], [[1]], [[2]], ([[-1]], [[0]]))
    for gradient in result[:4]:
        np.testing.assert_array_equal(gradient, np.zeros_like(gradient))
    np.testing.assert_array_equal(result[4], [1])

def test_04_two_hidden_units():
    result = solve([[1, 2]], [[1]], [[1, 0], [0, 1]], [[1], [1]], ([[1, 1]], [[1, 1]]))
    expected = ([[1, 1]], [[1, 1], [2, 2]], [1, 1], [[1], [1]], [1])
    for actual, want in zip(result, expected):
        np.testing.assert_allclose(actual, want)

def test_05_bias_gradient_sums_batch():
    result = solve([[1], [2]], [[1], [1]], [[1]], [[2]], ([[1], [2]], [[1], [2]]))
    np.testing.assert_allclose(result[2], [4])
    np.testing.assert_allclose(result[4], [2])

def test_06_multi_output_hidden_gradient():
    result = solve([[1]], [[1, 2]], [[1, 2]], [[1, 1], [1, 1]], ([[1, 1]], [[1, 1]]))
    np.testing.assert_allclose(result[2], [3, 3])

def test_07_weight_gradient_uses_hidden_activation():
    result = solve([[1]], [[2]], [[1]], [[3]], ([[2]], [[2]]))
    np.testing.assert_allclose(result[3], [[4]])

def test_08_zero_preactivation_blocks_relu_path():
    result = solve([[0]], [[1]], [[1]], [[1]], ([[0]], [[0]]))
    for gradient in result[:4]:
        np.testing.assert_array_equal(gradient, np.zeros_like(gradient))
    np.testing.assert_array_equal(result[4], [1])

def test_09_input_gradient_propagates_through_weights():
    result = solve([[1, 2]], [[1]], [[1, 0], [0, 1]], [[1], [1]], ([[1, 2]], [[1, 2]]))
    np.testing.assert_allclose(result[0], [[1, 1]])

def test_10_all_gradients_are_finite():
    result = solve([[1]], [[1]], [[1]], [[2]], ([[1]], [[1]]))
    assert all(np.isfinite(gradient).all() for gradient in result)

def test_11_first_layer_weight_gradient():
    result = solve([[1, 2]], [[1]], [[1, 0], [0, 1]], [[1], [1]], ([[1, 2]], [[1, 2]]))
    np.testing.assert_allclose(result[1], [[1, 1], [2, 2]])

def test_12_returns_all_five_gradients():
    result = solve([[1]], [[1]], [[1]], [[1]], ([[1]], [[1]]))
    assert len(result) == 5

def test_13_output_weight_gradient_shape_and_values():
    result = solve([[1, 2]], [[1]], [[1, 1], [1, 1]], [[1]], ([[3, 3]], [[3, 3]]))
    np.testing.assert_allclose(result[3], [[3], [3]])
