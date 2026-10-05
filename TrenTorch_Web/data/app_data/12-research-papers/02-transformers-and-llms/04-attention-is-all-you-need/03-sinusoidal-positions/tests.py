"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/04-attention-is-all-you-need/03-sinusoidal-positions/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-sinusoidal-positional-encoding")
sinusoidal_positional_encoding = _module.sinusoidal_positional_encoding


import numpy as np


def test_1_output_shape():
    assert sinusoidal_positional_encoding(7, 6).shape == (7, 6)


def test_2_position_zero_is_sin_zero_cos_zero():
    pe = sinusoidal_positional_encoding(3, 4)
    np.testing.assert_allclose(pe[0], [0.0, 1.0, 0.0, 1.0])


def test_3_matches_a_hand_computed_position_one():
    pe = sinusoidal_positional_encoding(2, 2)
    np.testing.assert_allclose(pe[1], [np.sin(1.0), np.cos(1.0)])


def test_4_values_are_bounded():
    pe = sinusoidal_positional_encoding(50, 16)
    assert np.all(np.abs(pe) <= 1.0)


def test_5_different_positions_get_different_encodings():
    pe = sinusoidal_positional_encoding(10, 8)
    assert len({tuple(np.round(row, 9)) for row in pe}) == 10


def test_6_does_not_depend_on_sequence_length_for_a_prefix():
    short = sinusoidal_positional_encoding(4, 8)
    long = sinusoidal_positional_encoding(9, 8)
    np.testing.assert_allclose(long[:4], short)

