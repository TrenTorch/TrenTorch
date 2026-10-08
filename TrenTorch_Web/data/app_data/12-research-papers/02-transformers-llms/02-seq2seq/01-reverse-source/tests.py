"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/02-seq2seq/01-reverse-source/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-seq2seq-reverse-source")
reverse_source = _module.reverse_source


def test_1_reverses_a_sentence():
    assert reverse_source(["a", "b", "c"]) == ["c", "b", "a"]


def test_2_empty_input_gives_empty_output():
    assert reverse_source([]) == []


def test_3_single_token_is_unchanged():
    assert reverse_source(["x"]) == ["x"]


def test_4_returns_a_new_list():
    original = ["a", "b"]
    out = reverse_source(original)
    assert out is not original


def test_5_does_not_mutate_the_input():
    original = ["a", "b", "c"]
    reverse_source(original)
    assert original == ["a", "b", "c"]


def test_6_accepts_a_tuple():
    assert reverse_source(("p", "q")) == ["q", "p"]

