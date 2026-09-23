"""
pytest data/app_data/00-python/01-core-semantics/12-if-elif-else/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
classify_number = _module.classify_number


def test_each_branch_reachable():
    assert classify_number(-5) == "negative"
    assert classify_number(0) == "zero"
    assert classify_number(5) == "small"
    assert classify_number(20) == "large"


def test_boundary_values():
    assert classify_number(0) == "zero"
    assert classify_number(10) == "small"
    assert classify_number(10.0001) == "large"


def test_only_one_branch_executes():
    assert classify_number(5) == "small"


def test_float_inputs_handled_identically():
    assert classify_number(-2.5) == "negative"
    assert classify_number(2.5) == "small"
    assert classify_number(15.5) == "large"
