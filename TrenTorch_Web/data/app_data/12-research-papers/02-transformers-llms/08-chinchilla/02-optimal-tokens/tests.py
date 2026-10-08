"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/08-chinchilla/02-optimal-tokens/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-chinchilla-optimal-tokens")
chinchilla_optimal_tokens = _module.chinchilla_optimal_tokens


def test_1_twenty_tokens_per_parameter():
    assert chinchilla_optimal_tokens(1) == 20.0


def test_2_seventy_billion_parameters_need_about_one_point_four_trillion_tokens():
    assert abs(chinchilla_optimal_tokens(70e9) - 1.4e12) < 1e6


def test_3_scales_linearly():
    assert abs(chinchilla_optimal_tokens(10) - 2 * chinchilla_optimal_tokens(5)) < 1e-9


def test_4_zero_parameters_need_zero_tokens():
    assert chinchilla_optimal_tokens(0) == 0.0


def test_5_returns_a_float():
    assert isinstance(chinchilla_optimal_tokens(3), float)


def test_6_matches_a_hand_value():
    assert chinchilla_optimal_tokens(5e8) == 1e10

