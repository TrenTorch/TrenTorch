"""
pytest data/app_data/01-numpy/09-performance-memory/04-measuring-vectorized-vs-loop-performance/tests.py
"""

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-numpy/09-performance-memory/{Path(__file__).resolve().parent.name}")
loop_sum_of_squares = _module.loop_sum_of_squares
vectorized_sum_of_squares = _module.vectorized_sum_of_squares
best_time = _module.best_time
benchmark_sum_of_squares = _module.benchmark_sum_of_squares


def test_both_implementations_are_correct():
    assert loop_sum_of_squares([]) == 0
    assert vectorized_sum_of_squares(np.array([], dtype=np.int64)) == 0
    assert loop_sum_of_squares([1, 2, 3]) == 14
    assert vectorized_sum_of_squares(np.array([1, 2, 3])) == 14
    assert loop_sum_of_squares([-2, 3, -4]) == 29
    assert vectorized_sum_of_squares(np.array([-2, 3, -4])) == 29


def test_vectorized_version_correct_on_large_array():
    n = 1_000_000
    arr = np.arange(n)
    expected = int((arr.astype(np.int64) ** 2).sum())
    assert vectorized_sum_of_squares(arr) == expected


def test_best_time_returns_the_minimum():
    durations = iter([0.05, 0.01, 0.03])

    def variable_sleep():
        time.sleep(next(durations))

    result = best_time(variable_sleep, (), 3)
    assert result < 0.02


def test_best_time_calls_function_exactly_repeats_times():
    calls = []

    def counter(x):
        calls.append(x)

    best_time(counter, (5,), 4)
    assert calls == [5, 5, 5, 5]


def test_benchmark_result_structure():
    result = benchmark_sum_of_squares(100, repeats=2)
    assert set(result.keys()) == {"loop_time", "vec_time", "speedup", "results_match"}
    assert result["loop_time"] > 0
    assert result["vec_time"] > 0
    assert result["speedup"] == result["loop_time"] / result["vec_time"]


def test_vectorization_measurably_faster_on_large_input():
    result = benchmark_sum_of_squares(200_000)
    assert result["speedup"] > 3
    assert result["results_match"] is True


def test_speedup_meaningful_at_scale():
    small = benchmark_sum_of_squares(100)
    large = benchmark_sum_of_squares(200_000)
    assert large["speedup"] > small["speedup"] * 0.5
