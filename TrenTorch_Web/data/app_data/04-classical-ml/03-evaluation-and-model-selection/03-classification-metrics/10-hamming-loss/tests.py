"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

hamming_loss = load_solution(__file__).hamming_loss


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_identical_matrices_have_zero_loss():
    y = np.array([[1, 0], [0, 1]])
    assert hamming_loss(y, y) == 0.0


def test_fully_inverted_labels_have_loss_one():
    y = np.array([[1, 0], [0, 1]])
    assert hamming_loss(y, 1 - y) == 1.0


def test_worked_multilabel_example():
    y_true = np.array([[1, 0], [0, 1]])
    y_pred = np.array([[1, 1], [0, 1]])
    assert np.isclose(hamming_loss(y_true, y_pred), 0.25)


def test_single_label_vectors_work():
    assert np.isclose(hamming_loss(np.array([1, 0, 1]), np.array([1, 1, 1])), 1.0 / 3.0)


def test_partial_credit_is_given_per_label_not_per_row():
    y_true = np.array([[1, 1, 0], [0, 0, 1]])
    y_pred = np.array([[1, 0, 0], [0, 0, 1]])
    # one wrong slot out of six
    assert np.isclose(hamming_loss(y_true, y_pred), 1.0 / 6.0)


def test_loss_is_within_zero_and_one():
    rng = np.random.default_rng(14)
    a = rng.integers(0, 2, size=(20, 5))
    b = rng.integers(0, 2, size=(20, 5))
    assert 0.0 <= hamming_loss(a, b) <= 1.0


def test_is_symmetric():
    rng = np.random.default_rng(15)
    a = rng.integers(0, 2, size=(10, 3))
    b = rng.integers(0, 2, size=(10, 3))
    assert hamming_loss(a, b) == hamming_loss(b, a)


def test_one_wrong_entry_out_of_many():
    y_true = np.zeros((10, 10), dtype=int)
    y_pred = y_true.copy()
    y_pred[3, 4] = 1
    assert np.isclose(hamming_loss(y_true, y_pred), 0.01)


def test_shape_mismatch_raises():
    assert _raises_value_error(hamming_loss, np.array([[1, 0]]), np.array([1, 0]))


def test_length_mismatch_raises():
    assert _raises_value_error(hamming_loss, np.array([1, 0]), np.array([1]))


def test_empty_input_raises():
    assert _raises_value_error(hamming_loss, np.array([]), np.array([]))


def test_returns_a_python_float():
    assert isinstance(hamming_loss(np.array([1, 0]), np.array([0, 0])), float)


def test_does_not_modify_inputs():
    y_true = np.array([[1, 0]])
    y_pred = np.array([[1, 1]])
    before_true, before_pred = y_true.copy(), y_pred.copy()
    hamming_loss(y_true, y_pred)
    assert np.array_equal(y_true, before_true)
    assert np.array_equal(y_pred, before_pred)
