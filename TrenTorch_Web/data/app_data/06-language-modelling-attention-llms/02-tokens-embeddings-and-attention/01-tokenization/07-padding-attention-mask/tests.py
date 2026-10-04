"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
import pytest

pad_batch = _module.pad_batch


def test_1_right_padding_hand_computed():
    ids, mask = pad_batch([[1, 2, 3], [4]], pad_id=0)
    assert ids.tolist() == [[1, 2, 3], [4, 0, 0]]
    assert mask.tolist() == [[1, 1, 1], [1, 0, 0]]


def test_2_left_padding_for_generation():
    ids, mask = pad_batch([[1, 2, 3], [4]], pad_id=0, side="left")
    assert ids.tolist() == [[1, 2, 3], [0, 0, 4]]
    assert mask.tolist() == [[1, 1, 1], [0, 0, 1]]


def test_3_truncation_keeps_the_first_tokens():
    ids, mask = pad_batch([[1, 2, 3, 4, 5], [6]], pad_id=9, max_len=3)
    assert ids.tolist() == [[1, 2, 3], [6, 9, 9]] and mask.sum() == 4


def test_4_real_token_equal_to_pad_id_is_still_masked_in():
    ids, mask = pad_batch([[0, 5], [7]], pad_id=0)
    assert mask.tolist() == [[1, 1], [1, 0]]


def test_5_max_len_longer_than_all_sequences_pads_further():
    ids, _ = pad_batch([[1], [2, 3]], pad_id=0, max_len=4)
    assert ids.shape == (2, 4)


def test_6_bad_side_raises():
    with pytest.raises(ValueError):
        pad_batch([[1]], 0, side="middle")


def test_7_mask_row_sums_equal_clipped_lengths_and_input_untouched():
    seqs = [[1, 2, 3, 4], [1], [1, 2]]
    snap = [list(s) for s in seqs]
    _, mask = pad_batch(seqs, 0, max_len=3, side="left")
    assert mask.sum(axis=1).tolist() == [3, 1, 2]
    assert seqs == snap
