"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/02-seq2seq/02-teacher-forcing-inputs/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-seq2seq-teacher-forcing")
decoder_inputs = _module.decoder_inputs


def test_1_shifts_targets_right_with_bos():
    assert decoder_inputs(["x", "y", "z"], "<s>") == ["<s>", "x", "y"]


def test_2_single_target_gives_only_bos():
    assert decoder_inputs(["x"], "<s>") == ["<s>"]


def test_3_length_matches_targets():
    assert len(decoder_inputs(["a", "b", "c", "d"], "<s>")) == 4


def test_4_empty_targets_give_only_bos():
    assert decoder_inputs([], "<s>") == ["<s>"]


def test_5_does_not_mutate_the_targets():
    targets = ["x", "y"]
    decoder_inputs(targets, "<s>")
    assert targets == ["x", "y"]


def test_6_last_target_is_not_an_input():
    assert "z" not in decoder_inputs(["x", "y", "z"], "<s>")

