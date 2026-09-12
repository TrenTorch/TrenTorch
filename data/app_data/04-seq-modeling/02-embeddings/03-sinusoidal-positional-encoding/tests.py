"""
pytest data/app_data/04-seq-modeling/02-embeddings/03-sinusoidal-positional-encoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/02-embeddings/{Path(__file__).resolve().parent.name}")
sinusoidal_positional_encoding = _module.sinusoidal_positional_encoding


def test_output_shape_is_seq_len_by_d_model():
    pe = sinusoidal_positional_encoding(seq_len=10, d_model=16)
    assert pe.shape == (10, 16)


def test_position_zero_is_alternating_zero_one():
    pe = sinusoidal_positional_encoding(seq_len=5, d_model=6)
    assert np.allclose(pe[0], [0.0, 1.0, 0.0, 1.0, 0.0, 1.0])


def test_even_columns_use_sin_odd_columns_use_cos():
    pe = sinusoidal_positional_encoding(seq_len=4, d_model=4)
    div_term = np.exp(np.arange(0, 4, 2) * -(np.log(10000.0) / 4))
    position = np.arange(4)[:, None]
    expected_sin = np.sin(position * div_term)
    expected_cos = np.cos(position * div_term)
    assert np.allclose(pe[:, 0::2], expected_sin)
    assert np.allclose(pe[:, 1::2], expected_cos)


def test_all_values_are_within_the_valid_sin_cos_range():
    pe = sinusoidal_positional_encoding(seq_len=20, d_model=32)
    assert np.all(pe >= -1.0)
    assert np.all(pe <= 1.0)


def test_different_positions_produce_different_encodings():
    pe = sinusoidal_positional_encoding(seq_len=10, d_model=8)
    for i in range(9):
        assert not np.allclose(pe[i], pe[i + 1])


def test_lowest_frequency_pair_varies_slower_than_the_highest_frequency_pair():
    # dimension pair 0 (columns 0,1) should oscillate FASTER across
    # positions than the LAST dimension pair (highest i, lowest frequency).
    pe = sinusoidal_positional_encoding(seq_len=50, d_model=16)
    fastest_pair_variation = np.abs(np.diff(pe[:, 0])).sum()
    slowest_pair_variation = np.abs(np.diff(pe[:, -2])).sum()
    assert fastest_pair_variation > slowest_pair_variation


def test_matches_hand_computed_values_for_a_known_position_and_dimension():
    # pos=1, i=0: sin(1 / 10000^0) = sin(1) ~ 0.8414709848
    pe = sinusoidal_positional_encoding(seq_len=2, d_model=4)
    assert np.isclose(pe[1, 0], np.sin(1.0))
    assert np.isclose(pe[1, 1], np.cos(1.0))


def test_reasonable_seq_len_and_d_model_produce_no_nan_or_inf():
    pe = sinusoidal_positional_encoding(seq_len=100, d_model=64)
    assert np.all(np.isfinite(pe))


def test_even_and_odd_columns_are_not_swapped():
    # Directly targets a mutant that swaps sin and cos between the even
    # and odd columns (pe[:, 0::2] = cos(...), pe[:, 1::2] = sin(...)):
    # position 0 would then come out as [1, 0, 1, 0, ...] instead of the
    # correct [0, 1, 0, 1, ...].
    pe = sinusoidal_positional_encoding(seq_len=3, d_model=4)
    assert np.isclose(pe[0, 0], 0.0)  # sin(0) = 0, must be in the EVEN column
    assert np.isclose(pe[0, 1], 1.0)  # cos(0) = 1, must be in the ODD column
