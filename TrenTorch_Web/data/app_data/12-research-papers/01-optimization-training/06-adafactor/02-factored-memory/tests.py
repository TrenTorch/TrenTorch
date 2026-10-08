"""
pytest data/app_data/12-research-papers/01-optimization-and-training/06-adafactor/02-factored-memory/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adafactor-factored-memory")
factored_memory = _module.factored_memory


def test_1_hand_case():
    assert factored_memory(4, 8) == 12


def test_2_is_smaller_than_full_matrix_for_large_dims():
    assert factored_memory(1024, 1024) < 1024 * 1024


def test_3_square_matrix_stores_two_n():
    assert factored_memory(5, 5) == 10


def test_4_one_by_one_stores_two():
    assert factored_memory(1, 1) == 2


def test_5_grows_linearly():
    assert factored_memory(10, 10) - factored_memory(9, 9) == 2


def test_6_returns_an_int():
    assert isinstance(factored_memory(3, 7), int)

