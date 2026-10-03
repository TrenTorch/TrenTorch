"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
one_hot_fit = _module.one_hot_fit
one_hot_transform = _module.one_hot_transform


def _raises_value_error(function, *args):
    try:
        function(*args)
    except ValueError:
        return True
    return False


def test_fit_returns_sorted_distinct_values():
    assert one_hot_fit(["red", "blue", "red", "green"]) == ["blue", "green", "red"]


def test_fit_on_integers_sorts_numerically():
    assert one_hot_fit([10, 2, 10, 1]) == [1, 2, 10]


def test_transform_marks_the_matching_column():
    result = one_hot_transform(["b", "a"], ["a", "b"])
    assert np.array_equal(result, np.array([[0.0, 1.0], [1.0, 0.0]]))


def test_each_row_sums_to_one():
    values = ["x", "y", "z", "x"]
    result = one_hot_transform(values, one_hot_fit(values))
    assert np.allclose(result.sum(axis=1), 1.0)


def test_output_shape_is_rows_by_categories():
    result = one_hot_transform(["a", "a", "b"], ["a", "b", "c"])
    assert result.shape == (3, 3)


def test_column_order_follows_the_supplied_categories():
    result = one_hot_transform(["a"], ["c", "b", "a"])
    assert np.array_equal(result, np.array([[0.0, 0.0, 1.0]]))


def test_empty_input_gives_zero_rows():
    result = one_hot_transform([], ["a", "b"])
    assert result.shape == (0, 2)


def test_unknown_category_raises():
    assert _raises_value_error(one_hot_transform, ["q"], ["a", "b"])


def test_argmax_recovers_the_original_category():
    values = ["dog", "cat", "bird", "cat"]
    categories = one_hot_fit(values)
    encoded = one_hot_transform(values, categories)
    recovered = [categories[i] for i in np.argmax(encoded, axis=1)]
    assert recovered == values


def test_output_dtype_is_float():
    assert one_hot_transform([1, 2], [1, 2]).dtype == np.float64


def test_integer_categories_are_encoded():
    result = one_hot_transform([3, 1], [1, 2, 3])
    assert np.array_equal(result, np.array([[0.0, 0.0, 1.0], [1.0, 0.0, 0.0]]))


def test_does_not_modify_the_input_values():
    values = ["a", "b"]
    before = list(values)
    one_hot_transform(values, ["a", "b"])
    assert values == before


def test_fit_then_transform_encodes_every_training_value():
    values = [2, 9, 2, 5]
    categories = one_hot_fit(values)
    encoded = one_hot_transform(values, categories)
    assert np.all(encoded.sum(axis=1) == 1.0)
    assert encoded.shape == (4, 3)
