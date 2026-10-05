"""
pytest data/app_data/12-research-papers/07-agentic-systems/01-react/03-first-finish/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-react-first-finish")
first_finish_index = _module.first_finish_index


def test_1_finds_the_finish_action():
    assert first_finish_index([("Search", "a"), ("Finish", "b")]) == 1


def test_2_no_finish_returns_none():
    assert first_finish_index([("Search", "a")]) is None


def test_3_empty_trace_returns_none():
    assert first_finish_index([]) is None


def test_4_returns_the_first_of_several_finishes():
    assert first_finish_index([("Finish", "x"), ("Finish", "y")]) == 0


def test_5_action_name_must_match_exactly():
    assert first_finish_index([("finish", "x")]) is None


def test_6_returns_an_int_when_found():
    assert isinstance(first_finish_index([("Finish", "")]), int)

