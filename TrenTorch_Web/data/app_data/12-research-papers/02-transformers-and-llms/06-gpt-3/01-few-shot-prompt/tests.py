"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/06-gpt-3/01-few-shot-prompt/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gpt3-few-shot-prompt")
build_few_shot_prompt = _module.build_few_shot_prompt


def test_1_zero_examples_gives_only_the_query():
    assert build_few_shot_prompt([], "cat") == "cat =>"


def test_2_one_example_is_formatted_then_the_query():
    assert build_few_shot_prompt([("dog", "chien")], "cat", sep=" | ") == "dog => chien | cat =>"


def test_3_examples_keep_their_order():
    out = build_few_shot_prompt([("a", "1"), ("b", "2")], "c", sep=";")
    assert out == "a => 1;b => 2;c =>"


def test_4_default_separator_is_a_blank_line():
    out = build_few_shot_prompt([("a", "1")], "b")
    assert "\n\n" in out


def test_5_query_is_the_last_line():
    out = build_few_shot_prompt([("a", "1"), ("b", "2")], "c")
    assert out.endswith("c =>")


def test_6_does_not_mutate_examples():
    examples = [("a", "1")]
    build_few_shot_prompt(examples, "b")
    assert examples == [("a", "1")]

