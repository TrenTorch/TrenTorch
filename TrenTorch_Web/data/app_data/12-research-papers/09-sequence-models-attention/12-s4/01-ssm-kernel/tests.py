"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/12-s4/01-ssm-kernel/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-s4-ssm-kernel")
ssm_kernel = _module.ssm_kernel


def test_1_length_is_l():
    assert len(ssm_kernel(0.5, 1.0, 1.0, 6)) == 6


def test_2_first_entry_is_c_times_b():
    assert abs(ssm_kernel(0.5, 2.0, 3.0, 3)[0] - 6.0) < 1e-12


def test_3_entries_decay_geometrically():
    K = ssm_kernel(0.5, 1.0, 1.0, 4)
    assert abs(K[1] - 0.5) < 1e-12 and abs(K[2] - 0.25) < 1e-12


def test_4_zero_state_decay_gives_a_single_tap():
    assert ssm_kernel(0.0, 1.0, 1.0, 3) == [1.0, 0.0, 0.0]


def test_5_returns_a_list():
    assert isinstance(ssm_kernel(0.5, 1.0, 1.0, 2), list)


def test_6_scales_with_c():
    a = ssm_kernel(0.3, 1.0, 1.0, 4)
    b = ssm_kernel(0.3, 1.0, 2.0, 4)
    assert all(abs(y - 2 * x) < 1e-12 for x, y in zip(a, b))

