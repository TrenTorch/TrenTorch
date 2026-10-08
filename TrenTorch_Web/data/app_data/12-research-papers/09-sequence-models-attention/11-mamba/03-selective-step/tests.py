"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/11-mamba/03-selective-step/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-mamba-selective-step")
selective_step = _module.selective_step


import math

import numpy as np


def test_1_softplus_of_zero_is_log_two():
    assert abs(selective_step(0.0) - math.log(2.0)) < 1e-12


def test_2_output_is_always_positive():
    assert all(selective_step(v) > 0 for v in [-30.0, -1.0, 0.0, 5.0])


def test_3_large_inputs_are_nearly_linear():
    assert abs(selective_step(40.0) - 40.0) < 1e-9


def test_4_very_negative_inputs_are_near_zero_but_positive():
    v = selective_step(-40.0)
    assert 0 < v < 1e-10


def test_5_returns_a_python_float():
    assert isinstance(selective_step(0.5), float)


def test_6_is_increasing():
    assert selective_step(1.0) > selective_step(0.0)

