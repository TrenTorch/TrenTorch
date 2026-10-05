"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/01-rnn-regularization/03-bptt-chunks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zaremba-bptt-chunks")
bptt_chunks = _module.bptt_chunks


import math


def test_1_even_split():
    assert bptt_chunks(12, 4) == 3


def test_2_partial_last_chunk_is_counted():
    assert bptt_chunks(10, 3) == 4


def test_3_truncation_longer_than_sequence_gives_one():
    assert bptt_chunks(5, 100) == 1


def test_4_returns_an_integer():
    assert isinstance(bptt_chunks(9, 2), int)


def test_5_bptt_one_gives_one_chunk_per_step():
    assert bptt_chunks(7, 1) == 7


def test_6_matches_math_ceil():
    assert bptt_chunks(11, 4) == math.ceil(11 / 4)

