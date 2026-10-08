"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/02-pointer-networks/02-select-input/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-ptr-select-input")
select_input = _module.select_input


import numpy as np


def test_1_returns_the_pointed_item():
    assert select_input(np.array([0.1, 0.9, 0.2]), ["a", "b", "c"]) == "b"


def test_2_ties_pick_the_first_position():
    assert select_input(np.array([1.0, 1.0]), ["x", "y"]) == "x"


def test_3_single_input_is_returned():
    assert select_input(np.array([5.0]), ["only"]) == "only"


def test_4_works_with_numbers():
    assert select_input(np.array([0.0, 2.0]), [10, 20]) == 20


def test_5_negative_scores_are_compared_correctly():
    assert select_input(np.array([-3.0, -1.0]), ["p", "q"]) == "q"


def test_6_does_not_mutate_inputs():
    items = ["a", "b"]
    select_input(np.array([0.0, 1.0]), items)
    assert items == ["a", "b"]

