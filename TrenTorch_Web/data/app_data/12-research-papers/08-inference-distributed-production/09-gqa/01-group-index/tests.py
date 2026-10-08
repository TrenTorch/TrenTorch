"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/09-gqa/01-group-index/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-gqa-group-index")
group_index = _module.group_index


def test_1_first_group_covers_the_first_heads():
    assert group_index(0, 8, 2) == 0 and group_index(3, 8, 2) == 0


def test_2_second_group_starts_halfway():
    assert group_index(4, 8, 2) == 1


def test_3_multi_query_puts_every_head_in_group_zero():
    assert all(group_index(h, 8, 1) == 0 for h in range(8))


def test_4_standard_attention_gives_one_head_per_group():
    assert [group_index(h, 4, 4) for h in range(4)] == [0, 1, 2, 3]


def test_5_returns_an_integer():
    assert isinstance(group_index(5, 8, 2), int)


def test_6_last_head_is_in_last_group():
    assert group_index(7, 8, 2) == 1

