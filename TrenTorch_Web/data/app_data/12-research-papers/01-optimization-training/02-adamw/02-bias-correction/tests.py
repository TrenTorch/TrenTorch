"""
pytest data/app_data/12-research-papers/01-optimization-and-training/02-adamw/02-bias-correction/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-adamw-bias-correction")
bias_corrected = _module.bias_corrected


def test_1_hand_value_at_first_step():
    m_hat, v_hat = bias_corrected(0.1, 0.001, 0.9, 0.999, 1)
    assert abs(m_hat - 1.0) < 1e-12 and abs(v_hat - 1.0) < 1e-12


def test_2_correction_vanishes_for_large_t():
    m_hat, _ = bias_corrected(0.5, 0.5, 0.9, 0.999, 1000)
    assert abs(m_hat - 0.5) < 1e-9


def test_3_returns_a_tuple_of_floats():
    out = bias_corrected(1.0, 1.0, 0.9, 0.999, 2)
    assert isinstance(out, tuple) and all(isinstance(x, float) for x in out)


def test_4_correction_increases_small_early_moments():
    m_hat, _ = bias_corrected(0.1, 0.1, 0.9, 0.999, 1)
    assert m_hat > 0.1


def test_5_hand_value_at_second_step():
    m_hat, _ = bias_corrected(0.19, 0.0, 0.9, 0.999, 2)
    assert abs(m_hat - 0.19 / 0.19) < 1e-12


def test_6_zero_moments_stay_zero():
    assert bias_corrected(0.0, 0.0, 0.9, 0.999, 3) == (0.0, 0.0)

