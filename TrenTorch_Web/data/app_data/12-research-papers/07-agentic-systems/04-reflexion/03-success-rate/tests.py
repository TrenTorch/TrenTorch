"""
pytest data/app_data/12-research-papers/07-agentic-systems/04-reflexion/03-success-rate/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-reflexion-success-rate")
success_rate = _module.success_rate


def test_1_all_success_gives_one():
    assert success_rate([True, True]) == 1.0


def test_2_all_failure_gives_zero():
    assert success_rate([False, False]) == 0.0


def test_3_mixed_results():
    assert abs(success_rate([True, False, True, True]) - 0.75) < 1e-12


def test_4_empty_list_gives_zero():
    assert success_rate([]) == 0.0


def test_5_returns_a_float():
    assert isinstance(success_rate([True]), float)


def test_6_accepts_truthy_values():
    assert success_rate([1, 0]) == 0.5

