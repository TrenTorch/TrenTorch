"""
pytest data/app_data/03-dl-training/03-training-loop/04-metric-tracking/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"03-dl-training/03-training-loop/{Path(__file__).resolve().parent.name}")
MetricTracker = _module.MetricTracker


def test_record_and_get_history_round_trip():
    t = MetricTracker()
    t.record("loss", 1.0)
    t.record("loss", 0.5)
    t.record("loss", 0.25)
    assert t.get_history("loss") == [1.0, 0.5, 0.25]


def test_get_history_returns_empty_list_for_unknown_metric():
    t = MetricTracker()
    assert t.get_history("nonexistent") == []


def test_different_metrics_are_tracked_independently():
    t = MetricTracker()
    t.record("loss", 1.0)
    t.record("accuracy", 0.9)
    t.record("loss", 0.8)
    assert t.get_history("loss") == [1.0, 0.8]
    assert t.get_history("accuracy") == [0.9]


def test_moving_average_has_the_same_length_as_the_raw_history():
    t = MetricTracker()
    for v in [1.0, 2.0, 3.0, 4.0, 5.0]:
        t.record("loss", v)
    result = t.moving_average("loss", window=3)
    assert len(result) == 5


def test_moving_average_matches_hand_computation():
    t = MetricTracker()
    for v in [2.0, 4.0, 6.0, 8.0]:
        t.record("loss", v)
    result = t.moving_average("loss", window=2)
    # i=0: mean([2])=2; i=1: mean([2,4])=3; i=2: mean([4,6])=5; i=3: mean([6,8])=7
    assert np.allclose(result, [2.0, 3.0, 5.0, 7.0])


def test_moving_average_with_window_larger_than_history_averages_everything_available():
    t = MetricTracker()
    for v in [1.0, 2.0, 3.0]:
        t.record("loss", v)
    result = t.moving_average("loss", window=100)
    # every index averages ALL values seen so far
    assert np.allclose(result, [1.0, 1.5, 2.0])


def test_moving_average_window_one_returns_the_raw_values_unchanged():
    t = MetricTracker()
    for v in [5.0, 3.0, 9.0]:
        t.record("loss", v)
    result = t.moving_average("loss", window=1)
    assert np.allclose(result, [5.0, 3.0, 9.0])


def test_best_with_mode_min_returns_the_minimum():
    t = MetricTracker()
    for v in [3.0, 1.0, 4.0, 1.5]:
        t.record("loss", v)
    assert t.best("loss", mode="min") == 1.0


def test_best_with_mode_max_returns_the_maximum():
    t = MetricTracker()
    for v in [0.7, 0.9, 0.85]:
        t.record("accuracy", v)
    assert t.best("accuracy", mode="max") == 0.9


def test_best_returns_none_for_a_metric_that_was_never_recorded():
    t = MetricTracker()
    assert t.best("nonexistent") is None


def test_moving_average_uses_a_trailing_window_ending_at_i_not_a_centered_window():
    # Directly targets a mutant that computes a CENTERED window (using
    # future values not yet available at step i) instead of a trailing
    # one: at i=0 with window=3, a centered window might average
    # values[0:2] using a value from the future, while the correct
    # trailing window can only use values[0:1] (nothing before i=0 yet).
    t = MetricTracker()
    for v in [10.0, 0.0, 0.0, 0.0]:
        t.record("loss", v)
    result = t.moving_average("loss", window=3)
    # at i=0, only values[0]=10 is available: average must be exactly 10
    assert np.isclose(result[0], 10.0)
