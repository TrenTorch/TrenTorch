"""
pytest data/app_data/12-research-papers/07-agentic-systems/12-hugginggpt/02-valid-plan/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-hugginggpt-valid-plan")
is_valid_plan = _module.is_valid_plan


def test_1_simple_chain_is_valid():
    assert is_valid_plan({"b": ["a"], "a": []}) is True


def test_2_missing_dependency_is_invalid():
    assert is_valid_plan({"b": ["ghost"]}) is False


def test_3_cycle_is_invalid():
    assert is_valid_plan({"a": ["b"], "b": ["a"]}) is False


def test_4_empty_plan_is_valid():
    assert is_valid_plan({}) is True


def test_5_self_dependency_is_invalid():
    assert is_valid_plan({"a": ["a"]}) is False


def test_6_returns_a_bool():
    assert isinstance(is_valid_plan({"a": []}), bool)

