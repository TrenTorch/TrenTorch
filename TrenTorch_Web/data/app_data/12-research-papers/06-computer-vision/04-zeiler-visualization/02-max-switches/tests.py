"""
pytest data/app_data/12-research-papers/06-computer-vision/04-zeiler-visualization/02-max-switches/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zeiler-max-switches")
max_pool_switches = _module.max_pool_switches


import numpy as np


def test_1_records_the_offset_of_each_maximum():
    np.testing.assert_array_equal(max_pool_switches(np.array([1.0, 5.0, 2.0, 0.0]), 2), [1, 0])


def test_2_ties_pick_the_first_offset():
    np.testing.assert_array_equal(max_pool_switches(np.array([3.0, 3.0]), 2), [0])


def test_3_output_has_one_switch_per_window():
    assert max_pool_switches(np.arange(12.0), 3).shape == (4,)


def test_4_returns_integers():
    assert max_pool_switches(np.arange(4.0), 2).dtype.kind == "i"


def test_5_single_window_of_size_one_is_always_zero():
    np.testing.assert_array_equal(max_pool_switches(np.array([7.0, -1.0]), 1), [0, 0])


def test_6_does_not_mutate_input():
    x = np.array([1.0, 2.0])
    max_pool_switches(x, 2)
    np.testing.assert_array_equal(x, [1.0, 2.0])

