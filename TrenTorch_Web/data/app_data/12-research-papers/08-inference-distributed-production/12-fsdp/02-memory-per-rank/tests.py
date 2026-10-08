"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/12-fsdp/02-memory-per-rank/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-fsdp-memory-per-rank")
fsdp_memory_per_rank = _module.fsdp_memory_per_rank


def test_1_hand_value():
    assert fsdp_memory_per_rank(10, 4, 2) == 6


def test_2_full_replication_with_one_rank():
    assert fsdp_memory_per_rank(10, 1, 2) == 20


def test_3_more_ranks_means_less_per_rank():
    assert fsdp_memory_per_rank(100, 8, 2) < fsdp_memory_per_rank(100, 2, 2)


def test_4_bytes_scale_linearly():
    assert fsdp_memory_per_rank(8, 2, 4) == 2 * fsdp_memory_per_rank(8, 2, 2)


def test_5_returns_an_integer():
    assert isinstance(fsdp_memory_per_rank(5, 2, 2), int)


def test_6_zero_parameters_use_no_memory():
    assert fsdp_memory_per_rank(0, 4, 2) == 0

