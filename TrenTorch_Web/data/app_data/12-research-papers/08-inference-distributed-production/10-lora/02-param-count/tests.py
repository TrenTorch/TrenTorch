"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/10-lora/02-param-count/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-lora-param-count")
lora_param_count = _module.lora_param_count


def test_1_hand_value():
    assert lora_param_count(8, 16, 2) == 48


def test_2_rank_one_is_the_sum_of_dimensions():
    assert lora_param_count(4, 6, 1) == 10


def test_3_full_rank_would_be_much_larger():
    assert lora_param_count(100, 100, 2) < 100 * 100


def test_4_scales_linearly_with_rank():
    assert lora_param_count(10, 10, 4) == 2 * lora_param_count(10, 10, 2)


def test_5_returns_an_integer():
    assert isinstance(lora_param_count(3, 3, 1), int)


def test_6_zero_rank_has_no_parameters():
    assert lora_param_count(5, 5, 0) == 0

