"""
pytest data/app_data/01-numpy/05-broadcasting/02-the-broadcasting-rule/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/05-broadcasting/{Path(__file__).resolve().parent.name}")
are_broadcastable = _module.are_broadcastable
broadcast_result_shape = _module.broadcast_result_shape


def test_equal_shapes_are_always_compatible():
    assert are_broadcastable((2, 3), (2, 3)) is True
    assert broadcast_result_shape((2, 3), (2, 3)) == (2, 3)


def test_size_1_dimension_stretching_in_various_positions():
    assert are_broadcastable((2, 3), (1, 3)) is True
    assert broadcast_result_shape((2, 3), (1, 3)) == (2, 3)
    assert are_broadcastable((5, 1), (5, 4)) is True
    assert broadcast_result_shape((5, 1), (5, 4)) == (5, 4)


def test_shorter_shape_correctly_padded_on_left():
    assert are_broadcastable((2, 3), (3,)) is True
    assert broadcast_result_shape((2, 3), (3,)) == (2, 3)
    assert are_broadcastable((8, 1, 6, 1), (7, 1, 5)) is True
    assert broadcast_result_shape((8, 1, 6, 1), (7, 1, 5)) == (8, 7, 6, 5)


def test_genuinely_incompatible_shapes_correctly_rejected():
    assert are_broadcastable((2, 3), (2, 4)) is False
    assert are_broadcastable((6,), (2, 3)) is False


def test_higher_dimensional_shape_compatibility():
    assert are_broadcastable((2, 1, 4, 1), (1, 3, 1, 5)) is True
    assert broadcast_result_shape((2, 1, 4, 1), (1, 3, 1, 5)) == (2, 3, 4, 5)
    assert are_broadcastable((3, 4, 5), (4, 6)) is False
