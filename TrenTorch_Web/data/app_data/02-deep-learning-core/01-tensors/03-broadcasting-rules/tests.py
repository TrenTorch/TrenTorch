"""
pytest data/app_data/02-deep-learning-core/01-tensors/03-broadcasting-rules/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

broadcast_shapes = load_solution(
    f"02-deep-learning-core/01-tensors/{Path(__file__).resolve().parent.name}"
).broadcast_shapes


def test_same_shapes():
    assert broadcast_shapes((3, 4), (3, 4)) == (3, 4)


def test_scalar_against_array():
    assert broadcast_shapes((3, 4), ()) == (3, 4)


def test_trailing_dimension_stretch():
    assert broadcast_shapes((3, 4), (4,)) == (3, 4)


def test_both_have_size_one_dims_to_stretch():
    assert broadcast_shapes((3, 1), (1, 4)) == (3, 4)


def test_different_ndims_aligned_from_the_right():
    assert broadcast_shapes((5, 3, 4), (4,)) == (5, 3, 4)


def test_multiple_stretching_dimensions():
    assert broadcast_shapes((8, 1, 6, 1), (7, 1, 5)) == (8, 7, 6, 5)


def test_incompatible_trailing_dims_returns_none():
    assert broadcast_shapes((3, 4), (5,)) is None


def test_incompatible_matrix_shapes_returns_none():
    assert broadcast_shapes((2, 3), (3, 2)) is None


def test_padding_is_on_the_left_not_the_right():
    # Directly targets a mutant that pads the shorter shape on the
    # RIGHT instead of the left: (3,4) vs (3,) should align (3,) under
    # the trailing 4, which is incompatible (3 != 4, neither is 1) --
    # padding on the right would instead align (3,) under the leading
    # 3, which WOULD look compatible, a real, distinguishable
    # difference.
    assert broadcast_shapes((3, 4), (3,)) is None
