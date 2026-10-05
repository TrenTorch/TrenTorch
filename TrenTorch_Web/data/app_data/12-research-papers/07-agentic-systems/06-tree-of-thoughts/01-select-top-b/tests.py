"""
pytest data/app_data/12-research-papers/07-agentic-systems/06-tree-of-thoughts/01-select-top-b/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tot-select-top-b")
select_top_b = _module.select_top_b


def test_1_keeps_the_highest_scores():
    assert select_top_b(["a", "b", "c"], [0.1, 0.9, 0.5], 2) == ["b", "c"]


def test_2_beam_wider_than_candidates_keeps_all():
    assert select_top_b(["a"], [1.0], 5) == ["a"]


def test_3_beam_of_zero_keeps_nothing():
    assert select_top_b(["a", "b"], [1.0, 2.0], 0) == []


def test_4_output_is_best_first():
    assert select_top_b(["x", "y", "z"], [1.0, 3.0, 2.0], 3) == ["y", "z", "x"]


def test_5_does_not_mutate_inputs():
    states = ["a", "b"]
    select_top_b(states, [1.0, 2.0], 1)
    assert states == ["a", "b"]


def test_6_returns_a_list():
    assert isinstance(select_top_b(["a"], [0.0], 1), list)

