"""
pytest data/app_data/12-research-papers/07-agentic-systems/01-react/01-parse-action/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-react-parse-action")
parse_action = _module.parse_action


def test_1_parses_name_and_argument():
    assert parse_action("Thought: look it up\nAction: Search[France]") == ("Search", "France")


def test_2_no_action_returns_none():
    assert parse_action("Thought: I know this already") is None


def test_3_empty_argument_is_allowed():
    assert parse_action("Action: Finish[]") == ("Finish", "")


def test_4_takes_the_first_action_only():
    assert parse_action("Action: A[1]\nAction: B[2]") == ("A", "1")


def test_5_returns_a_tuple():
    assert isinstance(parse_action("Action: X[y]"), tuple)


def test_6_ignores_text_after_the_bracket():
    assert parse_action("Action: Lookup[cat] and more words") == ("Lookup", "cat")

