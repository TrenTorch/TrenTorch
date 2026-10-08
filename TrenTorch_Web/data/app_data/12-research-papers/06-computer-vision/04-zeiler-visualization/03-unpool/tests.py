"""
pytest data/app_data/12-research-papers/06-computer-vision/04-zeiler-visualization/03-unpool/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from _load import load_solution  # noqa: E402

_module = load_solution("research-zeiler-unpool")
unpool_with_switches = _module.unpool_with_switches


import numpy as np


def test_1_round_trip_recovers_the_maxima():
    out = unpool_with_switches(np.array([5.0, 2.0]), np.array([1, 0]), 2)
    np.testing.assert_allclose(out, [0.0, 5.0, 2.0, 0.0])


def test_2_non_maximal_positions_are_zero():
    out = unpool_with_switches(np.array([4.0]), np.array([2]), 3)
    np.testing.assert_allclose(out, [0.0, 0.0, 4.0])


def test_3_output_length_is_windows_times_size():
    assert len(unpool_with_switches(np.ones(4), np.zeros(4, dtype=int), 3)) == 12


def test_4_single_window_of_size_one_is_identity():
    np.testing.assert_allclose(unpool_with_switches(np.array([7.0]), np.array([0]), 1), [7.0])


def test_5_nonzero_count_equals_window_count():
    out = unpool_with_switches(np.array([1.0, 2.0, 3.0]), np.array([0, 1, 2]), 3)
    assert np.count_nonzero(out) == 3


def test_6_does_not_mutate_inputs():
    p = np.array([1.0])
    unpool_with_switches(p, np.array([0]), 2)
    np.testing.assert_array_equal(p, [1.0])

