"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/02-flashattention-2/03-num-blocks/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fa2-num-blocks")
num_blocks = _module.num_blocks


def test_1_exact_division():
    assert num_blocks(8, 4) == 2


def test_2_partial_last_block_is_counted():
    assert num_blocks(9, 4) == 3


def test_3_single_block():
    assert num_blocks(3, 128) == 1


def test_4_zero_rows_need_no_blocks():
    assert num_blocks(0, 4) == 0


def test_5_returns_an_integer():
    assert isinstance(num_blocks(10, 3), int)


def test_6_block_size_one_gives_n():
    assert num_blocks(7, 1) == 7

