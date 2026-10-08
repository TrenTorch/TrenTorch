"""
pytest data/app_data/12-research-papers/02-transformers-and-llms/07-scaling-laws/02-fit-exponent/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-scaling-fit-exponent")
fit_power_law_exponent = _module.fit_power_law_exponent


import numpy as np


def test_1_recovers_the_exponent_of_an_exact_power_law():
    N = np.array([1e5, 1e6, 1e7, 1e8])
    L = 3.0 * N ** -0.076
    assert abs(fit_power_law_exponent(N, L) - 0.076) < 1e-9


def test_2_returns_a_python_float():
    assert isinstance(fit_power_law_exponent(np.array([1.0, 10.0]), np.array([1.0, 0.1])), float)


def test_3_two_points_give_the_exact_slope():
    assert abs(fit_power_law_exponent(np.array([1.0, 10.0]), np.array([1.0, 0.5])) - (-np.log10(0.5))) < 1e-9


def test_4_decreasing_losses_give_positive_alpha():
    assert fit_power_law_exponent(np.array([1e5, 1e6]), np.array([2.0, 1.0])) > 0


def test_5_scaling_the_losses_does_not_change_alpha():
    N = np.array([1e5, 1e6, 1e7])
    L = N ** -0.1
    assert abs(fit_power_law_exponent(N, L) - fit_power_law_exponent(N, 5 * L)) < 1e-9


def test_6_does_not_mutate_inputs():
    N = np.array([1.0, 10.0])
    fit_power_law_exponent(N, np.array([1.0, 0.5]))
    np.testing.assert_array_equal(N, [1.0, 10.0])

