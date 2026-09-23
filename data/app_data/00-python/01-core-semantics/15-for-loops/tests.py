"""
pytest data/app_data/00-python/01-core-semantics/15-for-loops/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
sum_with_index = _module.sum_with_index
manual_iteration_trace = _module.manual_iteration_trace


def test_sum_with_index_correct_running_totals():
    assert sum_with_index([10, 20, 30]) == {0: 10, 1: 30, 2: 60}


def test_sum_with_index_empty_list():
    assert sum_with_index([]) == {}


def test_manual_iteration_trace_matches_for_loop_behavior():
    items = [1, 2, 3, "four", 5.0]
    assert manual_iteration_trace(items) == items


def test_manual_iteration_trace_handles_stop_iteration_correctly():
    assert manual_iteration_trace([]) == []
    assert manual_iteration_trace([42]) == [42]
