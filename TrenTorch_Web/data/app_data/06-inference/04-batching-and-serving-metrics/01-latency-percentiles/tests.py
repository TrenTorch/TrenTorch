"""
pytest data/app_data/06-inference/04-batching-and-serving-metrics/01-latency-percentiles/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

latency_percentiles = load_solution(
    f"06-inference/04-batching-and-serving-metrics/{Path(__file__).resolve().parent.name}"
).latency_percentiles


def test_exact_rank_no_interpolation():
    result = latency_percentiles([10, 20, 30, 40, 50], percentiles=[50])
    assert result["p50"] == 30


def test_interpolated_rank():
    result = latency_percentiles([10, 20, 30, 40], percentiles=[50])
    assert result["p50"] == 25


def test_p95_p99_on_larger_sample():
    result = latency_percentiles(list(range(1, 101)), percentiles=[50, 95, 99])
    assert result["p50"] == 50.5
    assert abs(result["p95"] - 95.05) < 1e-6
    assert abs(result["p99"] - 99.01) < 1e-6


def test_single_sample():
    result = latency_percentiles([42], percentiles=[1, 50, 99])
    assert result == {"p1": 42.0, "p50": 42.0, "p99": 42.0}


def test_unsorted_input_handled():
    result = latency_percentiles([50, 10, 30, 20, 40], percentiles=[50])
    assert result["p50"] == 30


def test_p0_and_p100_are_min_and_max():
    result = latency_percentiles([5, 1, 9, 3], percentiles=[0, 100])
    assert result["p0"] == 1
    assert result["p100"] == 9
