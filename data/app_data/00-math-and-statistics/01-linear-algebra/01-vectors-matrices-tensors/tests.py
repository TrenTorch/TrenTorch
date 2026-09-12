"""
pytest data/app_data/00-math-and-statistics/01-linear-algebra/01-vectors-matrices-tensors/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-math-and-statistics/01-linear-algebra/{Path(__file__).resolve().parent.name}"
)
shape_of = _module.shape_of
ndim_of = _module.ndim_of
elementwise_add = _module.elementwise_add
elementwise_multiply = _module.elementwise_multiply


def test_shape_of_scalar():
    assert shape_of(np.array(5.0)) == ()


def test_shape_of_vector():
    assert shape_of(np.array([1.0, 2.0, 3.0])) == (3,)


def test_shape_of_matrix():
    assert shape_of(np.zeros((2, 3))) == (2, 3)


def test_shape_of_higher_rank_tensor():
    assert shape_of(np.zeros((4, 3, 2))) == (4, 3, 2)


def test_ndim_of_matches_shape_length():
    for shape in [(), (3,), (2, 3), (4, 3, 2)]:
        x = np.zeros(shape)
        assert ndim_of(x) == len(shape)


def test_elementwise_add_matches_hand_computation():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([10.0, 20.0, 30.0])
    assert np.allclose(elementwise_add(a, b), [11.0, 22.0, 33.0])


def test_elementwise_add_preserves_shape():
    a = np.zeros((3, 4))
    b = np.ones((3, 4))
    assert elementwise_add(a, b).shape == (3, 4)


def test_elementwise_multiply_matches_hand_computation():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([10.0, 20.0, 30.0])
    assert np.allclose(elementwise_multiply(a, b), [10.0, 40.0, 90.0])


def test_elementwise_multiply_is_not_matrix_multiplication():
    # Directly targets a mutant that confuses elementwise multiply with
    # a dot-product / matmul-style reduction: elementwise multiply on
    # two length-3 vectors returns a length-3 array, not a scalar.
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([10.0, 20.0, 30.0])
    result = elementwise_multiply(a, b)
    assert result.shape == (3,)
    assert np.allclose(result, [10.0, 40.0, 90.0])


def test_elementwise_multiply_on_matrices():
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[5.0, 6.0], [7.0, 8.0]])
    assert np.allclose(elementwise_multiply(a, b), [[5.0, 12.0], [21.0, 32.0]])
