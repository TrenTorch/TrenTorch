"""
pytest data/app_data/12-research-papers/07-agentic-systems/03-toolformer/03-keep-call/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-toolformer-keep-call")
keep_call = _module.keep_call


def test_1_large_reduction_keeps_the_call():
    assert keep_call(2.0, 1.0, 0.5) is True


def test_2_small_reduction_drops_the_call():
    assert keep_call(1.0, 0.9, 0.5) is False


def test_3_exact_threshold_keeps_the_call():
    assert keep_call(1.5, 1.0, 0.5) is True


def test_4_increase_in_loss_drops_the_call():
    assert keep_call(1.0, 2.0, 0.1) is False


def test_5_zero_threshold_keeps_non_worsening_calls():
    assert keep_call(1.0, 1.0, 0.0) is True


def test_6_returns_a_bool():
    assert isinstance(keep_call(1.0, 0.0, 0.1), bool)

