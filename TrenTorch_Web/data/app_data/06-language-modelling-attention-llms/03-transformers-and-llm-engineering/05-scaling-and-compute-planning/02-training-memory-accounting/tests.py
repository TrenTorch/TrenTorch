"""
pytest tests.py
"""

import pytest
from _load import load_solution

_module = load_solution(__file__)
bytes_per_param = _module.bytes_per_param
training_memory_gib = _module.training_memory_gib


def test_1_no_sharding_is_16_bytes():
    assert bytes_per_param(0, 8) == 16.0


def test_2_stage_one_shards_optimizer_only():
    assert bytes_per_param(1, 4) == 2 + 2 + 12 / 4


def test_3_stage_two_also_shards_gradients():
    assert bytes_per_param(2, 4) == 2 + 2 / 4 + 12 / 4


def test_4_stage_three_shards_everything():
    assert bytes_per_param(3, 8) == 16 / 8


def test_5_each_stage_uses_less_for_more_than_one_gpu():
    vals = [bytes_per_param(s, 8) for s in range(4)]
    assert vals == sorted(vals, reverse=True) and len(set(vals)) == 4


def test_6_single_gpu_changes_nothing_and_bad_stage_raises():
    assert all(bytes_per_param(s, 1) == 16.0 for s in range(4))
    with pytest.raises(ValueError):
        bytes_per_param(4, 2)


def test_7_seven_billion_parameters_in_gib():
    assert abs(training_memory_gib(7e9, 0, 1) - 7e9 * 16 / 2 ** 30) < 1e-9
    assert training_memory_gib(7e9, 3, 8) < training_memory_gib(7e9, 0, 8)
