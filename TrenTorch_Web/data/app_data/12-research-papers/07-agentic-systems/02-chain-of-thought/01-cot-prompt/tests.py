"""
pytest data/app_data/12-research-papers/07-agentic-systems/02-chain-of-thought/01-cot-prompt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-cot-prompt")
build_cot_prompt = _module.build_cot_prompt


def test_1_zero_examples_gives_only_the_question():
    assert build_cot_prompt([], "2+2?") == "Q: 2+2?\nA:"


def test_2_example_contains_reasoning_then_answer():
    out = build_cot_prompt([("1+1?", "One and one.", "2")], "3+3?")
    assert "One and one. The answer is 2." in out


def test_3_examples_are_separated_by_blank_lines():
    out = build_cot_prompt([("a", "r1", "1"), ("b", "r2", "2")], "c")
    assert "\n\n" in out


def test_4_ends_with_an_open_answer():
    assert build_cot_prompt([("a", "r", "1")], "b").endswith("Q: b\nA:")


def test_5_examples_keep_their_order():
    out = build_cot_prompt([("first", "r", "1"), ("second", "r", "2")], "x")
    assert out.index("first") < out.index("second")


def test_6_returns_a_string():
    assert isinstance(build_cot_prompt([], "q"), str)

