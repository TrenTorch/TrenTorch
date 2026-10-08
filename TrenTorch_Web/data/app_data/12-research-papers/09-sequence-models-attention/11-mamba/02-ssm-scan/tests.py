"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/11-mamba/02-ssm-scan/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mamba-ssm-scan")
ssm_scan = _module.ssm_scan


def test_1_zero_transition_gives_input_scaled():
    assert ssm_scan(0.0, 2.0, [1.0, 3.0]) == [2.0, 6.0]


def test_2_unit_transition_is_a_running_sum():
    assert ssm_scan(1.0, 1.0, [1.0, 2.0, 3.0]) == [1.0, 3.0, 6.0]


def test_3_hand_value_with_decay():
    out = ssm_scan(0.5, 1.0, [4.0, 0.0])
    assert abs(out[0] - 4.0) < 1e-12 and abs(out[1] - 2.0) < 1e-12


def test_4_output_length_matches_input():
    assert len(ssm_scan(0.9, 0.1, [1.0] * 6)) == 6


def test_5_zero_input_keeps_zero_state():
    assert ssm_scan(0.7, 0.3, [0.0, 0.0]) == [0.0, 0.0]


def test_6_does_not_mutate_input():
    x = [1.0, 2.0]
    ssm_scan(0.5, 0.5, x)
    assert x == [1.0, 2.0]

