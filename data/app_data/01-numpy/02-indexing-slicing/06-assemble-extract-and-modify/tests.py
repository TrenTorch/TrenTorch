"""
pytest data/app_data/01-numpy/02-indexing-slicing/06-assemble-extract-and-modify/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/02-indexing-slicing/{Path(__file__).resolve().parent.name}")
clean_and_reorder = _module.clean_and_reorder


def _sample_data():
    return np.array(
        [
            [1, -2, 3, 4],
            [-5, 6, 7, -8],
            [9, 10, -11, 12],
            [13, 14, 15, 16],
        ]
    )


def test_correct_region_extraction():
    data = _sample_data()
    result = clean_and_reorder(data, (1, 3), [0, 1, 2, 3])
    np.testing.assert_array_equal(result["region"], data[1:3, :])


def test_correct_cleaning_of_invalid_values():
    data = _sample_data()
    result = clean_and_reorder(data, (0, 2), [0, 1, 2, 3])
    np.testing.assert_array_equal(result["cleaned"], [[1, 0, 3, 4], [0, 6, 7, 0]])


def test_region_is_view_cleaned_is_not():
    data = _sample_data()
    result = clean_and_reorder(data, (0, 2), [0, 1, 2, 3])
    assert result["region_shares_memory_with_data"] is True
    assert result["cleaned_shares_memory_with_region"] is False


def test_correct_column_reordering():
    data = _sample_data()
    result = clean_and_reorder(data, (0, 2), [3, 0, 1])
    np.testing.assert_array_equal(result["reordered"], result["cleaned"][:, [3, 0, 1]])


def test_data_itself_is_unmodified_by_whole_pipeline():
    data = _sample_data()
    original = data.copy()
    clean_and_reorder(data, (0, 2), [0, 1, 2, 3])
    np.testing.assert_array_equal(data, original)
