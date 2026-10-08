"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/09-roformer/02-rope-rotate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-rope-rotate")
rope_rotate = _module.rope_rotate


import numpy as np


def test_1_position_zero_is_identity():
    x = np.array([1.0, 2.0, 3.0, 4.0])
    np.testing.assert_allclose(rope_rotate(x, 0), x, atol=1e-12)


def test_2_preserves_the_norm():
    x = np.array([1.0, 2.0, -3.0, 0.5])
    np.testing.assert_allclose(np.linalg.norm(rope_rotate(x, 7)), np.linalg.norm(x))


def test_3_matches_a_quarter_turn_for_the_first_pair():
    out = rope_rotate(np.array([1.0, 0.0]), np.pi / 2)
    np.testing.assert_allclose(out, [0.0, 1.0], atol=1e-12)


def test_4_keeps_the_input_shape():
    assert rope_rotate(np.ones(6), 3).shape == (6,)


def test_5_rotation_is_consistent_for_a_vector_of_zeros():
    np.testing.assert_allclose(rope_rotate(np.zeros(4), 9), np.zeros(4))


def test_6_does_not_mutate_the_input():
    x = np.array([1.0, 2.0])
    rope_rotate(x, 5)
    np.testing.assert_array_equal(x, [1.0, 2.0])

