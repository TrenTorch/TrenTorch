"""
pytest data/app_data/12-research-papers/07-agentic-systems/10-self-refine/02-first-ok/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-selfrefine-first-ok")
first_ok_index = _module.first_ok_index


def test_1_finds_the_first_ok():
    assert first_ok_index(["bad", "OK", "OK"]) == 1


def test_2_no_ok_returns_none():
    assert first_ok_index(["bad", "worse"]) is None


def test_3_empty_feedback_returns_none():
    assert first_ok_index([]) is None


def test_4_ok_in_first_round():
    assert first_ok_index(["OK"]) == 0


def test_5_match_is_exact():
    assert first_ok_index(["ok", "OK!"]) is None


def test_6_returns_an_int_when_found():
    assert isinstance(first_ok_index(["OK"]), int)

