"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/08-chinchilla/01-training-flops/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-chinchilla-flops")
training_flops = _module.training_flops


def test_1_one_parameter_one_token_is_six_flops():
    assert training_flops(1, 1) == 6.0


def test_2_seventy_billion_by_one_trillion():
    assert abs(training_flops(70e9, 1.4e12) - 6 * 70e9 * 1.4e12) < 1e-3


def test_3_scales_linearly_in_parameters():
    assert abs(training_flops(20, 5) - 2 * training_flops(10, 5)) < 1e-9


def test_4_scales_linearly_in_tokens():
    assert abs(training_flops(7, 40) - 2 * training_flops(7, 20)) < 1e-9


def test_5_returns_a_float():
    assert isinstance(training_flops(3, 4), float)


def test_6_matches_a_hand_value():
    assert abs(training_flops(1e9, 2e10) - 1.2e20) < 1e10

