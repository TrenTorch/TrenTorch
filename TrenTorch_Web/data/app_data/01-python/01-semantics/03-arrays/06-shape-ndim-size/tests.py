"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
describe_shape = _module.describe_shape
is_shape_valid_for_size = _module.is_shape_valid_for_size


def test_correct_reporting_across_dimensionalities():
    assert describe_shape(np.zeros(5)) == {"shape": (5,), "ndim": 1, "size": 5}
    assert describe_shape(np.zeros((3, 4))) == {"shape": (3, 4), "ndim": 2, "size": 12}
    assert describe_shape(np.zeros((2, 3, 4))) == {"shape": (2, 3, 4), "ndim": 3, "size": 24}


def test_size_matches_product_of_shape():
    for shape in [(5,), (3, 4), (1, 7), (2, 1, 3)]:
        result = describe_shape(np.zeros(shape))
        expected_size = 1
        for dim in shape:
            expected_size *= dim
        assert result["size"] == expected_size


def test_is_shape_valid_for_size_correctly_validates_and_rejects():
    assert is_shape_valid_for_size((3, 4), 12) is True
    assert is_shape_valid_for_size((3, 5), 12) is False
    assert is_shape_valid_for_size((12,), 12) is True


def test_zero_dimensional_edge_case():
    result = describe_shape(np.array(5))
    assert result == {"shape": (), "ndim": 0, "size": 1}
