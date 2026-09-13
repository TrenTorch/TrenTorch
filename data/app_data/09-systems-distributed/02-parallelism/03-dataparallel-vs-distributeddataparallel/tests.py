"""
pytest data/app_data/09-systems-distributed/02-parallelism/03-dataparallel-vs-distributeddataparallel/tests.py
"""

import sys
from pathlib import Path

import math

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"09-systems-distributed/02-parallelism/{Path(__file__).resolve().parent.name}")
dp_communication_volume = _module.dp_communication_volume
ddp_communication_volume = _module.ddp_communication_volume
dp_gpu0_memory_multiplier = _module.dp_gpu0_memory_multiplier
ddp_gpu0_memory_multiplier = _module.ddp_gpu0_memory_multiplier
communication_reduction_factor = _module.communication_reduction_factor


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_dp_moves_more_data_than_ddp_for_same_setup():
    dp = dp_communication_volume(1000.0, 4)
    ddp = ddp_communication_volume(1000.0, 4)
    assert dp > ddp


def test_02_communication_reduction_factor_equals_num_gpus():
    for n in (2, 4, 8):
        assert math.isclose(communication_reduction_factor(1000.0, n), n)


# --- General-case coverage --------------------------------------------


def test_03_dp_volume_formula():
    assert math.isclose(dp_communication_volume(500.0, 4), 2 * 3 * 500.0)


def test_04_ddp_volume_formula():
    assert math.isclose(ddp_communication_volume(500.0, 4), 2 * 3 / 4 * 500.0)


def test_05_reduction_factor_grows_with_gpu_count():
    small = communication_reduction_factor(1000.0, 2)
    large = communication_reduction_factor(1000.0, 16)
    assert large > small


# --- Parameter handling -------------------------------------------------


def test_06_gpu0_memory_multiplier_asymmetry():
    assert dp_gpu0_memory_multiplier(8) == 8.0
    assert ddp_gpu0_memory_multiplier(8) == 1.0
    assert dp_gpu0_memory_multiplier(8) > ddp_gpu0_memory_multiplier(8)


def test_07_gpu0_memory_multiplier_scales_linearly_for_dp():
    assert math.isclose(dp_gpu0_memory_multiplier(4), 4.0)
    assert math.isclose(dp_gpu0_memory_multiplier(16), 16.0)


# --- Edge cases ---------------------------------------------------------


def test_08_single_gpu_has_zero_communication():
    assert dp_communication_volume(1000.0, 1) == 0.0
    assert ddp_communication_volume(1000.0, 1) == 0.0
    assert communication_reduction_factor(1000.0, 1) == 1.0


def test_09_ddp_multiplier_constant_regardless_of_gpu_count():
    assert ddp_gpu0_memory_multiplier(2) == ddp_gpu0_memory_multiplier(32)


# --- Independent correctness oracle -----------------------------------


def test_10_reduction_factor_scales_with_model_size_only_through_ratio():
    # Directly targets a mutant that hardcodes model_size_bytes into
    # the ratio instead of it canceling out algebraically: the
    # reduction factor must depend ONLY on num_gpus, not on the actual
    # model size passed in.
    small_model = communication_reduction_factor(10.0, 6)
    large_model = communication_reduction_factor(1_000_000.0, 6)
    assert math.isclose(small_model, large_model)
    assert math.isclose(small_model, 6.0)
