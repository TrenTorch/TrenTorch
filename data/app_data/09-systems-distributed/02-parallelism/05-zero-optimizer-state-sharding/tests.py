"""
pytest data/app_data/09-systems-distributed/02-parallelism/05-zero-optimizer-state-sharding/tests.py
"""

import sys
from pathlib import Path

import math

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
per_gpu_memory_bytes = _module.per_gpu_memory_bytes
memory_reduction_factor = _module.memory_reduction_factor


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_stage_zero_matches_the_known_sixteen_psi_figure():
    assert math.isclose(per_gpu_memory_bytes(1_000_000, num_gpus=8, zero_stage=0), 16_000_000.0)


def test_02_higher_zero_stages_use_strictly_less_memory():
    num_params, num_gpus = 1_000_000, 8
    stage0 = per_gpu_memory_bytes(num_params, num_gpus, 0)
    stage1 = per_gpu_memory_bytes(num_params, num_gpus, 1)
    stage2 = per_gpu_memory_bytes(num_params, num_gpus, 2)
    stage3 = per_gpu_memory_bytes(num_params, num_gpus, 3)
    assert stage0 > stage1 > stage2 > stage3


# --- General-case coverage --------------------------------------------


def test_03_stage_one_formula():
    assert math.isclose(per_gpu_memory_bytes(1_000_000, 8, 1), 5_500_000.0)


def test_04_stage_two_formula():
    assert math.isclose(per_gpu_memory_bytes(1_000_000, 8, 2), 3_750_000.0)


def test_05_stage_three_formula():
    assert math.isclose(per_gpu_memory_bytes(1_000_000, 8, 3), 2_000_000.0)


def test_06_stage_three_scales_inversely_with_gpu_count():
    p = 2_000_000
    assert math.isclose(
        per_gpu_memory_bytes(p, 4, 3) / per_gpu_memory_bytes(p, 8, 3), 2.0
    )


# --- Parameter handling -------------------------------------------------


def test_07_memory_reduction_factor_for_full_sharding_equals_gpu_count():
    for n in (2, 4, 16):
        assert math.isclose(memory_reduction_factor(5_000_000, n, zero_stage=3), n)


def test_08_invalid_zero_stage_raises():
    with pytest.raises(ValueError):
        per_gpu_memory_bytes(1_000_000, 8, zero_stage=4)


# --- Edge cases ---------------------------------------------------------


def test_09_single_gpu_stage_three_equals_stage_zero():
    p = 1_000_000
    assert math.isclose(per_gpu_memory_bytes(p, 1, 3), per_gpu_memory_bytes(p, 1, 0))
    assert math.isclose(memory_reduction_factor(p, 1, 3), 1.0)


# --- Independent correctness oracle -----------------------------------


def test_10_memory_scales_linearly_with_param_count():
    # Directly targets a mutant that hardcodes a fixed byte-per-param
    # constant regardless of num_params, or breaks proportionality
    # (e.g. adds a fixed offset instead of pure scaling).
    small = per_gpu_memory_bytes(1_000, 4, zero_stage=2)
    large = per_gpu_memory_bytes(10_000, 4, zero_stage=2)
    assert math.isclose(large / small, 10.0)
