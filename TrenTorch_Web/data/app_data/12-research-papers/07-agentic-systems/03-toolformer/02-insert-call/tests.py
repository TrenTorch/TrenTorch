"""
pytest data/app_data/12-research-papers/07-agentic-systems/03-toolformer/02-insert-call/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-toolformer-insert-call")
insert_call = _module.insert_call


def test_1_inserts_at_the_position():
    assert insert_call("ab", 1, "[X]") == "a[X]b"


def test_2_inserting_at_the_start():
    assert insert_call("hi", 0, "[X]") == "[X]hi"


def test_3_inserting_at_the_end():
    assert insert_call("hi", 2, "[X]") == "hi[X]"


def test_4_empty_text_gets_the_call():
    assert insert_call("", 0, "[X]") == "[X]"


def test_5_original_text_is_preserved_around_the_call():
    out = insert_call("hello world", 5, "[C]")
    assert out.replace("[C]", "") == "hello world"


def test_6_returns_a_string():
    assert isinstance(insert_call("a", 0, "b"), str)

