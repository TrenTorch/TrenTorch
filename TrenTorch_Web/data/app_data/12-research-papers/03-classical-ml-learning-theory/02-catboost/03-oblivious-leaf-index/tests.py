"""
pytest data/app_data/12-research-papers/03-classical-ml-and-learning-theory/02-catboost/03-oblivious-leaf-index/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-catboost-oblivious-leaf")
oblivious_leaf_index = _module.oblivious_leaf_index


def test_1_bits_one_zero_one_give_five():
    assert oblivious_leaf_index([1, 0, 1]) == 5


def test_2_no_splits_give_leaf_zero():
    assert oblivious_leaf_index([]) == 0


def test_3_all_zeros_give_zero():
    assert oblivious_leaf_index([0, 0, 0]) == 0


def test_4_first_bit_is_least_significant():
    assert oblivious_leaf_index([0, 1]) == 2


def test_5_all_ones_give_the_largest_index():
    assert oblivious_leaf_index([1, 1, 1]) == 7


def test_6_does_not_mutate_the_input():
    bits = [1, 0]
    oblivious_leaf_index(bits)
    assert bits == [1, 0]

