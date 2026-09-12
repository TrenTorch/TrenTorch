"""
pytest data/app_data/00-math-and-statistics/05-data-preprocessing/03-one-hot-encoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/05-data-preprocessing/{Path(__file__).resolve().parent.name}"
)
get_unique_categories = _module.get_unique_categories
one_hot_encode = _module.one_hot_encode


def test_get_unique_categories_returns_sorted_distinct_values():
    column = np.array(["dog", "cat", "dog", "bird", "cat"])
    result = get_unique_categories(column)
    assert list(result) == ["bird", "cat", "dog"]


def test_one_hot_encode_shape():
    column = np.array(["cat", "dog", "bird", "dog"])
    result = one_hot_encode(column)
    assert result.shape == (4, 3)


def test_one_hot_encode_matches_hand_computation():
    column = np.array(["cat", "dog", "bird"])
    # categories (sorted): bird=0, cat=1, dog=2
    result = one_hot_encode(column)
    expected = np.array(
        [
            [0.0, 1.0, 0.0],  # cat
            [0.0, 0.0, 1.0],  # dog
            [1.0, 0.0, 0.0],  # bird
        ]
    )
    assert np.array_equal(result, expected)


def test_one_hot_encode_every_row_sums_to_one():
    column = np.array(["a", "b", "c", "a", "b"])
    result = one_hot_encode(column)
    assert np.allclose(result.sum(axis=1), 1.0)


def test_one_hot_encode_respects_explicit_category_order():
    # Explicit categories passed in a DIFFERENT order than np.unique's
    # default sort, the encoding must follow the given order exactly.
    column = np.array(["dog", "cat"])
    categories = np.array(["dog", "cat", "bird"])  # not alphabetically sorted
    result = one_hot_encode(column, categories=categories)
    assert np.array_equal(result, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])


def test_one_hot_encode_with_explicit_categories_does_not_recompute_them():
    # Directly targets a mutant that ignores the passed `categories`
    # argument and always recomputes fresh from `column` via
    # get_unique_categories. Supplying MORE categories than appear in
    # `column` should still produce that wider shape.
    column = np.array(["cat", "dog"])
    categories = np.array(["bird", "cat", "dog", "fish"])  # "bird"/"fish" absent from column
    result = one_hot_encode(column, categories=categories)
    assert result.shape == (2, 4)
    assert np.array_equal(result, [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]])


def test_one_hot_encode_of_integer_categories():
    column = np.array([2, 0, 1, 0])
    result = one_hot_encode(column)
    expected = np.array(
        [
            [0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 0.0],
        ]
    )
    assert np.array_equal(result, expected)
