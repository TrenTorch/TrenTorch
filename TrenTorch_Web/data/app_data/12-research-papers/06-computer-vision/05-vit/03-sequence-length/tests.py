"""
pytest data/app_data/12-research-papers/06-computer-vision/05-vit/03-sequence-length/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vit-seq-length")
vit_seq_length = _module.vit_seq_length


def test_1_standard_vit_sequence_is_197():
    assert vit_seq_length(224, 16) == 197


def test_2_always_one_more_than_patch_count():
    assert vit_seq_length(64, 8) == 64 + 1


def test_3_single_patch_gives_two_tokens():
    assert vit_seq_length(16, 16) == 2


def test_4_returns_an_integer():
    assert isinstance(vit_seq_length(32, 8), int)


def test_5_longer_sequences_for_smaller_patches():
    assert vit_seq_length(32, 4) > vit_seq_length(32, 8)


def test_6_matches_patch_count_plus_class_token_definition():
    assert vit_seq_length(48, 12) == (48 // 12) ** 2 + 1

