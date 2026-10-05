"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/07-scaling-laws/01-power-law-loss/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-scaling-power-law-loss")
power_law_loss = _module.power_law_loss


import numpy as np


def test_1_equal_size_and_scale_gives_one():
    assert abs(float(power_law_loss(1e6, 1e6, 0.076)) - 1.0) < 1e-12


def test_2_ten_times_larger_model_gives_ten_to_minus_alpha():
    assert abs(float(power_law_loss(1e7, 1e6, 0.5)) - 10 ** -0.5) < 1e-12


def test_3_loss_decreases_with_model_size():
    out = power_law_loss(np.array([1e5, 1e6, 1e7]), 1e6, 0.1)
    assert out[0] > out[1] > out[2]


def test_4_array_input_keeps_shape():
    assert power_law_loss(np.ones((2, 3)) * 1e6, 1e6, 0.1).shape == (2, 3)


def test_5_larger_alpha_drops_faster():
    assert power_law_loss(1e7, 1e6, 0.5) < power_law_loss(1e7, 1e6, 0.1)


def test_6_does_not_mutate_inputs():
    N = np.array([1e6, 1e7])
    power_law_loss(N, 1e6, 0.1)
    np.testing.assert_array_equal(N, [1e6, 1e7])

