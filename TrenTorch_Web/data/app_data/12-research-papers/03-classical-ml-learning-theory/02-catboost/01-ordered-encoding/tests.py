"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/02-catboost/01-ordered-encoding/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-catboost-ordered-encoding")
ordered_target_encoding = _module.ordered_target_encoding


def test_1_first_occurrence_equals_the_prior():
    assert ordered_target_encoding(["a"], [1], 0.5) == [0.5]


def test_2_second_occurrence_uses_the_first_label():
    out = ordered_target_encoding(["a", "a"], [1, 0], 0.5, a=1.0)
    assert abs(out[1] - 0.75) < 1e-12


def test_3_categories_are_independent():
    out = ordered_target_encoding(["a", "b", "a"], [1, 0, 0], 0.5)
    assert abs(out[1] - 0.5) < 1e-12


def test_4_current_label_does_not_leak_into_its_own_encoding():
    first = ordered_target_encoding(["a", "a"], [0, 1], 0.5)
    other = ordered_target_encoding(["a", "a"], [1, 1], 0.5)
    assert first[0] == other[0]


def test_5_output_length_matches_input():
    assert len(ordered_target_encoding(["x", "y", "x"], [1, 0, 1], 0.2)) == 3


def test_6_does_not_mutate_inputs():
    cats = ["a", "a"]
    ordered_target_encoding(cats, [1, 0], 0.5)
    assert cats == ["a", "a"]

