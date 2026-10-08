"""
pytest data/app_data/12-research-papers/07-agentic-systems/01-react/02-prompt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-react-prompt")
build_react_prompt = _module.build_react_prompt


def test_1_no_steps_gives_only_the_question():
    assert build_react_prompt("Who?", []) == "Question: Who?"


def test_2_one_step_has_all_three_fields():
    out = build_react_prompt("Q", [("look", "Search[x]", "found")])
    assert "Thought: look" in out and "Action: Search[x]" in out and "Observation: found" in out


def test_3_steps_keep_their_order():
    out = build_react_prompt("Q", [("a", "A[]", "1"), ("b", "B[]", "2")])
    assert out.index("Observation: 1") < out.index("Observation: 2")


def test_4_thought_count_matches_steps():
    out = build_react_prompt("Q", [("a", "A", "1"), ("b", "B", "2"), ("c", "C", "3")])
    assert out.count("Thought:") == 3


def test_5_question_is_the_first_line():
    assert build_react_prompt("Hello", [("t", "a", "o")]).split("\n")[0] == "Question: Hello"


def test_6_returns_a_string():
    assert isinstance(build_react_prompt("q", []), str)

