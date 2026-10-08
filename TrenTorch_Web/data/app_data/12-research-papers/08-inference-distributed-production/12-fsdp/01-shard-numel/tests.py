"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/12-fsdp/01-shard-numel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fsdp-shard-numel")
fsdp_shard_numel = _module.fsdp_shard_numel


def test_1_even_split():
    assert fsdp_shard_numel(12, 4) == 3


def test_2_uneven_split_pads_up():
    assert fsdp_shard_numel(10, 4) == 3


def test_3_single_rank_stores_all():
    assert fsdp_shard_numel(9, 1) == 9


def test_4_zero_elements():
    assert fsdp_shard_numel(0, 8) == 0


def test_5_returns_an_integer():
    assert isinstance(fsdp_shard_numel(7, 2), int)


def test_6_shards_cover_all_elements():
    assert fsdp_shard_numel(10, 3) * 3 >= 10

