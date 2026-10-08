"""
pytest data/app_data/12-research-papers/07-agentic-systems/03-toolformer/01-call-format/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-toolformer-call-format")
format_api_call = _module.format_api_call


def test_1_formats_the_three_parts():
    assert format_api_call("Calc", "2+2", "4") == "[Calc(2+2) -> 4]"


def test_2_empty_arguments_are_allowed():
    assert format_api_call("Now", "", "2024") == "[Now() -> 2024]"


def test_3_starts_and_ends_with_brackets():
    out = format_api_call("A", "x", "y")
    assert out.startswith("[") and out.endswith("]")


def test_4_contains_the_arrow_to_the_result():
    assert "->" in format_api_call("A", "x", "y")


def test_5_result_can_be_any_text():
    assert format_api_call("Wiki", "Paris", "a city") == "[Wiki(Paris) -> a city]"


def test_6_returns_a_string():
    assert isinstance(format_api_call("A", "", ""), str)

