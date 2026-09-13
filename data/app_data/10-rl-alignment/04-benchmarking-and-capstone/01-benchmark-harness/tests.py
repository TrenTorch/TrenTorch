"""
pytest data/app_data/10-rl-alignment/04-benchmarking-and-capstone/01-benchmark-harness/tests.py
"""

import sys
from pathlib import Path

import math

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"10-rl-alignment/04-benchmarking-and-capstone/{Path(__file__).resolve().parent.name}")
time_function = _module.time_function
benchmark_statistics = _module.benchmark_statistics


# --- Basic correctness (the two the "Run" button samples) -----------------


def test_01_time_function_calls_fn_exactly_num_runs_times():
    call_count = {"n": 0}

    def fn():
        call_count["n"] += 1

    time_function(fn, num_runs=7)
    assert call_count["n"] == 7


def test_02_benchmark_statistics_matches_hand_computation():
    times = [1.0, 2.0, 3.0, 4.0, 5.0]
    stats = benchmark_statistics(times)
    assert math.isclose(stats["mean"], 3.0)
    assert math.isclose(stats["median"], 3.0)
    assert math.isclose(stats["min"], 1.0)
    assert math.isclose(stats["max"], 5.0)


# --- General-case coverage --------------------------------------------


def test_03_time_function_returns_a_list_of_the_right_length():
    result = time_function(lambda: None, num_runs=5)
    assert len(result) == 5


def test_04_time_function_measurements_are_never_negative():
    result = time_function(lambda: sum(range(1000)), num_runs=3)
    assert all(t >= 0.0 for t in result)


def test_05_benchmark_statistics_std_matches_numpy():
    times = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
    stats = benchmark_statistics(times)
    assert math.isclose(stats["std"], float(np.std(times)))


# --- Parameter handling -------------------------------------------------


def test_06_time_function_default_num_runs():
    call_count = {"n": 0}

    def fn():
        call_count["n"] += 1

    time_function(fn)
    assert call_count["n"] == 5  # documented default


def test_07_benchmark_statistics_returns_all_five_keys():
    stats = benchmark_statistics([1.0, 2.0, 3.0])
    assert set(stats.keys()) == {"mean", "median", "min", "max", "std"}


# --- Edge cases ---------------------------------------------------------


def test_08_single_measurement_has_zero_std():
    stats = benchmark_statistics([4.0])
    assert math.isclose(stats["std"], 0.0)
    assert math.isclose(stats["mean"], 4.0)


def test_09_single_run_returns_single_element_list():
    result = time_function(lambda: None, num_runs=1)
    assert len(result) == 1


# --- Independent correctness oracle -----------------------------------


def test_10_statistics_reflect_the_actual_spread_not_just_the_mean():
    # Directly targets a mutant that hardcodes min/max/std to the same
    # value as mean (a common "looks plausible but isn't real" bug):
    # a genuinely spread-out set of times must show min < mean < max
    # and a nonzero std.
    times = [0.001, 0.05, 0.1, 0.2, 0.5]
    stats = benchmark_statistics(times)
    assert stats["min"] < stats["mean"] < stats["max"]
    assert stats["std"] > 0.0
