"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
majority_class_baseline = _module.majority_class_baseline


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_predicts_the_most_frequent_label():
    y = np.array([0, 1, 1, 1, 0])
    assert np.array_equal(majority_class_baseline(y, 4), np.array([1, 1, 1, 1]))


def test_output_length_is_n_samples():
    y = np.array([2, 2, 3])
    assert majority_class_baseline(y, 7).shape == (7,)


def test_zero_samples_returns_an_empty_array():
    assert majority_class_baseline(np.array([1, 0]), 0).shape == (0,)


def test_ties_go_to_the_smaller_label():
    y = np.array([3, 1, 3, 1])
    assert np.array_equal(majority_class_baseline(y, 2), np.array([1, 1]))


def test_string_labels_work():
    y = np.array(["cat", "dog", "dog"])
    assert np.array_equal(majority_class_baseline(y, 3), np.array(["dog", "dog", "dog"]))


def test_dtype_matches_the_training_labels():
    y = np.array([1.5, 1.5, 2.0])
    assert majority_class_baseline(y, 2).dtype == y.dtype


def test_single_class_is_returned_for_every_sample():
    y = np.array([7, 7, 7])
    assert np.array_equal(majority_class_baseline(y, 5), np.full(5, 7))


def test_accuracy_of_the_baseline_equals_the_majority_frequency():
    y_train = np.array([0, 0, 0, 1])
    y_test = np.array([0, 1, 0, 0, 0])
    prediction = majority_class_baseline(y_train, len(y_test))
    assert np.isclose(np.mean(prediction == y_test), 0.8)


def test_empty_training_labels_raise():
    assert _raises_value_error(majority_class_baseline, np.array([], dtype=int), 3)


def test_does_not_depend_on_the_order_of_the_training_labels():
    a = majority_class_baseline(np.array([1, 2, 2, 1, 2]), 3)
    b = majority_class_baseline(np.array([2, 1, 2, 2, 1]), 3)
    assert np.array_equal(a, b)


def test_does_not_modify_its_input():
    y = np.array([0, 1, 1])
    y_before = y.copy()
    majority_class_baseline(y, 2)
    assert np.array_equal(y, y_before)


def test_returns_a_numpy_array():
    assert isinstance(majority_class_baseline([0, 1, 1], 2), np.ndarray)


def test_three_way_tie_returns_the_smallest_label():
    y = np.array([4, 2, 9])
    assert np.array_equal(majority_class_baseline(y, 1), np.array([2]))
