"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/04-zero/02-shard-size/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zero-shard-size")
shard_size = _module.shard_size


def test_1_even_split():
    assert shard_size(12, 4) == 3


def test_2_uneven_split_rounds_up():
    assert shard_size(10, 4) == 3


def test_3_single_device_holds_everything():
    assert shard_size(7, 1) == 7


def test_4_zero_elements_need_no_space():
    assert shard_size(0, 4) == 0


def test_5_returns_an_integer():
    assert isinstance(shard_size(9, 2), int)


def test_6_shards_cover_the_total():
    assert shard_size(10, 3) * 3 >= 10

