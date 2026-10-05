"""
pytest data/app_data/12-research-papers/09-sequence-models-and-attention/10-adaptive-computation-time/03-act-output/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-act-output")
act_output = _module.act_output


import numpy as np


def test_1_single_step_returns_its_output():
    assert abs(act_output([5.0], [1.0]) - 5.0) < 1e-12


def test_2_two_equal_halts_average_the_outputs():
    assert abs(act_output([1.0, 3.0], [0.5, 0.5]) - 2.0) < 1e-12


def test_3_weights_come_from_halts_and_remainder():
    # weights: 0.2, then 1 - 0.2 = 0.8
    assert abs(act_output([0.0, 10.0], [0.2, 0.3]) - 8.0) < 1e-12


def test_4_constant_outputs_return_that_constant():
    assert abs(act_output([2.0, 2.0, 2.0], [0.3, 0.3, 0.4]) - 2.0) < 1e-12


def test_5_returns_a_python_float():
    assert isinstance(act_output([1.0], [1.0]), float)


def test_6_does_not_mutate_halts():
    h = [0.5, 0.5]
    act_output([1.0, 2.0], h)
    assert h == [0.5, 0.5]

