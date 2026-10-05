"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/04-zero/03-partition-bounds/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zero-partition-bounds")
partition_bounds = _module.partition_bounds


import numpy as np


def test_1_first_rank_starts_at_zero():
    assert partition_bounds(10, 4, 0)[0] == 0


def test_2_ranges_are_contiguous_and_cover_everything():
    bounds = [partition_bounds(10, 4, r) for r in range(4)]
    assert bounds[0][1] == bounds[1][0] and bounds[1][1] == bounds[2][0]
    assert bounds[-1][1] == 10


def test_3_hand_value_for_uneven_split():
    assert partition_bounds(10, 4, 0) == (0, 3)
    assert partition_bounds(10, 4, 3) == (8, 10)


def test_4_single_device_owns_everything():
    assert partition_bounds(5, 1, 0) == (0, 5)


def test_5_returns_a_tuple_of_ints():
    s, e = partition_bounds(9, 3, 1)
    assert isinstance(s, int) and isinstance(e, int)


def test_6_shard_sizes_differ_by_at_most_one():
    sizes = [e - s for s, e in (partition_bounds(11, 4, r) for r in range(4))]
    assert max(sizes) - min(sizes) <= 1

