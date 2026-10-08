"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/02-flashattention-2/02-attention-flops/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fa2-attention-flops")
attention_flops = _module.attention_flops


def test_1_non_causal_formula():
    assert attention_flops(2, 1) == 16


def test_2_causal_halves_the_work():
    assert attention_flops(2, 1, causal=True) == 8


def test_3_quadratic_in_sequence_length():
    assert attention_flops(8, 4) == 4 * attention_flops(4, 4)


def test_4_linear_in_head_dimension():
    assert attention_flops(4, 8) == 2 * attention_flops(4, 4)


def test_5_returns_an_integer():
    assert isinstance(attention_flops(3, 3), int)


def test_6_zero_length_costs_nothing():
    assert attention_flops(0, 16) == 0

