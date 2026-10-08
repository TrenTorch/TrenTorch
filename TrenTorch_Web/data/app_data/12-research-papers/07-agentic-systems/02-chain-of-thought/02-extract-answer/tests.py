"""
pytest data/app_data/12-research-papers/07-agentic-systems/02-chain-of-thought/02-extract-answer/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cot-extract-answer")
extract_final_answer = _module.extract_final_answer


def test_1_extracts_a_simple_answer():
    assert extract_final_answer("Steps... The answer is 42.") == "42"


def test_2_uses_the_last_occurrence():
    assert extract_final_answer("The answer is 1. Wait. The answer is 2.") == "2"


def test_3_missing_phrase_returns_none():
    assert extract_final_answer("I think it is 42.") is None


def test_4_strips_whitespace():
    assert extract_final_answer("The answer is    7 .") == "7"


def test_5_stops_at_newline():
    assert extract_final_answer("The answer is yes\nmore") == "yes"


def test_6_returns_a_string_when_found():
    assert isinstance(extract_final_answer("The answer is x."), str)

