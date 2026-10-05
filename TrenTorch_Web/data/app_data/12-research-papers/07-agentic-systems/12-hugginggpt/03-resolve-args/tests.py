"""
pytest data/app_data/12-research-papers/07-agentic-systems/12-hugginggpt/03-resolve-args/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-hugginggpt-resolve-args")
resolve_args = _module.resolve_args


def test_1_replaces_a_placeholder():
    assert resolve_args("image=<t1>", {"t1": "cat.png"}) == "image=cat.png"


def test_2_unknown_placeholder_is_left_alone():
    assert resolve_args("x=<t9>", {"t1": "a"}) == "x=<t9>"


def test_3_multiple_placeholders_are_all_replaced():
    assert resolve_args("<a>+<b>", {"a": "1", "b": "2"}) == "1+2"


def test_4_no_placeholders_returns_input():
    assert resolve_args("plain", {"t1": "x"}) == "plain"


def test_5_numeric_results_are_converted_to_text():
    assert resolve_args("n=<t1>", {"t1": 7}) == "n=7"


def test_6_does_not_mutate_results():
    r = {"t1": "a"}
    resolve_args("<t1>", r)
    assert r == {"t1": "a"}

