"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/01-flashattention/02-causal-block-skip/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-flash-causal-block-skip")
causal_block_needed = _module.causal_block_needed


def test_1_diagonal_block_is_needed():
    assert causal_block_needed(0, 0, 2, 2) is True


def test_2_block_entirely_in_the_future_is_skipped():
    assert causal_block_needed(0, 1, 2, 2) is False


def test_3_earlier_key_blocks_are_needed():
    assert causal_block_needed(3, 0, 4, 4) is True


def test_4_later_query_block_sees_the_next_key_block():
    assert causal_block_needed(1, 1, 2, 2) is True


def test_5_returns_a_bool():
    assert isinstance(causal_block_needed(0, 0, 1, 1), bool)


def test_6_skips_more_blocks_than_needed_is_false():
    assert causal_block_needed(0, 5, 4, 4) is False

