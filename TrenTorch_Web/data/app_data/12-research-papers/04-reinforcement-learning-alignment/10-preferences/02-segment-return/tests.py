"""
pytest data/app_data/12-research-papers/04-reinforcement-learning-and-alignment/10-preferences/02-segment-return/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-preference-segment-return")
segment_return = _module.segment_return


import numpy as np


def test_1_sums_the_rewards():
    assert abs(segment_return([1.0, 2.0, 3.0]) - 6.0) < 1e-12


def test_2_empty_segment_has_zero_return():
    assert segment_return([]) == 0.0


def test_3_negative_rewards_are_summed():
    assert abs(segment_return([-1.0, 0.5]) - (-0.5)) < 1e-12


def test_4_returns_a_python_float():
    assert isinstance(segment_return(np.array([1, 2])), float)


def test_5_order_does_not_matter():
    assert segment_return([1.0, 5.0]) == segment_return([5.0, 1.0])


def test_6_does_not_mutate_input():
    r = np.array([1.0, 2.0])
    segment_return(r)
    np.testing.assert_array_equal(r, [1.0, 2.0])

