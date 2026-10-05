"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/12-switch-transformer/03-expert-capacity/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-switch-capacity")
expert_capacity = _module.expert_capacity


import math


def test_1_exact_average_load_with_factor_one():
    assert expert_capacity(8, 4, 1.0) == 2


def test_2_slack_factor_rounds_up():
    assert expert_capacity(10, 4, 1.25) == 4


def test_3_returns_an_integer():
    assert isinstance(expert_capacity(10, 4, 1.0), int)


def test_4_capacity_is_at_least_the_average_load():
    assert expert_capacity(7, 3, 1.0) >= 7 / 3


def test_5_larger_factor_gives_larger_capacity():
    assert expert_capacity(100, 8, 2.0) > expert_capacity(100, 8, 1.0)


def test_6_single_expert_takes_everything():
    assert expert_capacity(9, 1, 1.0) == 9

