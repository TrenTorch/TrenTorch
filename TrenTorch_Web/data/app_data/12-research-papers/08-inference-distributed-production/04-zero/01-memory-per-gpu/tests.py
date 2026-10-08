"""
pytest data/app_data/12-research-papers/08-inference-distributed-and-production/04-zero/01-memory-per-gpu/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zero-memory-per-gpu")
zero_memory_per_gpu = _module.zero_memory_per_gpu


def test_1_stage_zero_is_sixteen_bytes_per_parameter():
    assert zero_memory_per_gpu(10, 4, 0) == 160


def test_2_stage_one_shards_only_optimizer_state():
    assert abs(zero_memory_per_gpu(4, 4, 1) - 28.0) < 1e-12


def test_3_stage_three_shards_everything():
    assert abs(zero_memory_per_gpu(8, 4, 3) - 32.0) < 1e-12


def test_4_single_gpu_is_the_same_for_all_stages():
    assert abs(zero_memory_per_gpu(5, 1, 1) - zero_memory_per_gpu(5, 1, 0)) < 1e-12


def test_5_higher_stage_uses_less_memory_on_many_gpus():
    assert zero_memory_per_gpu(10, 8, 3) < zero_memory_per_gpu(10, 8, 1)


def test_6_memory_scales_with_parameters():
    assert zero_memory_per_gpu(20, 4, 2) == 2 * zero_memory_per_gpu(10, 4, 2)

