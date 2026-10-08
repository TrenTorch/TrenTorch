"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/01-flashattention/03-hbm-bytes/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-flash-hbm-bytes")
naive_attention_hbm_bytes = _module.naive_attention_hbm_bytes


def test_1_sequence_of_1024_in_fp16():
    assert naive_attention_hbm_bytes(1024, 2) == 2_097_152


def test_2_default_is_two_bytes():
    assert naive_attention_hbm_bytes(4) == 32


def test_3_quadratic_in_sequence_length():
    assert naive_attention_hbm_bytes(8) == 4 * naive_attention_hbm_bytes(4)


def test_4_zero_length_needs_no_memory():
    assert naive_attention_hbm_bytes(0) == 0


def test_5_returns_an_integer():
    assert isinstance(naive_attention_hbm_bytes(3), int)


def test_6_four_byte_scores_double_the_cost():
    assert naive_attention_hbm_bytes(10, 4) == 2 * naive_attention_hbm_bytes(10, 2)

