"""
pytest data/app_data/12-research-papers/07-agentic-systems/06-tree-of-thoughts/03-total-thoughts/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-tot-total-thoughts")
total_thoughts = _module.total_thoughts


def test_1_branching_two_depth_three_gives_fourteen():
    assert total_thoughts(2, 3) == 14


def test_2_zero_depth_generates_nothing():
    assert total_thoughts(5, 0) == 0


def test_3_single_branch_generates_one_per_depth():
    assert total_thoughts(1, 4) == 4


def test_4_grows_exponentially_with_depth():
    assert total_thoughts(3, 4) > total_thoughts(3, 3) * 2


def test_5_returns_an_integer():
    assert isinstance(total_thoughts(2, 2), int)


def test_6_branching_three_depth_two():
    assert total_thoughts(3, 2) == 3 + 9

