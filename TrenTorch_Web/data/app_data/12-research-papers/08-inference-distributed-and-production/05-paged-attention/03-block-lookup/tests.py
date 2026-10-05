"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/05-paged-attention/03-block-lookup/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-vllm-block-lookup")
block_table_lookup = _module.block_table_lookup


def test_1_token_in_first_block():
    assert block_table_lookup([7, 3, 9], 1, 2) == (7, 1)


def test_2_token_in_second_block_uses_its_table_entry():
    assert block_table_lookup([7, 3, 9], 5, 2) == (9, 1)


def test_3_first_token_has_offset_zero():
    assert block_table_lookup([4], 0, 16) == (4, 0)


def test_4_block_boundary_starts_a_new_block():
    assert block_table_lookup([1, 2], 4, 4) == (2, 0)


def test_5_returns_a_tuple():
    assert isinstance(block_table_lookup([0], 0, 1), tuple)


def test_6_does_not_mutate_table():
    table = [1, 2]
    block_table_lookup(table, 0, 1)
    assert table == [1, 2]

