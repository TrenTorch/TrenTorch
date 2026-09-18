"""
pytest data/app_data/06-inference/04-batching-and-serving-metrics/03-dynamic-request-batching/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

dynamic_request_batching = load_solution(
    f"06-inference/04-batching-and-serving-metrics/{Path(__file__).resolve().parent.name}"
).dynamic_request_batching


def test_example_from_description():
    result = dynamic_request_batching(
        max_batch_size=2, max_wait_time=1.0,
        arrivals=[(0, "a"), (0.3, "b"), (0.4, "c")],
    )
    assert result["batches"] == [["a", "b"], ["c"]]
    assert result["close_times"] == [0.3, 1.4]


def test_never_fills_always_times_out():
    result = dynamic_request_batching(
        max_batch_size=10, max_wait_time=0.5,
        arrivals=[(0, "a"), (0.6, "b"), (1.3, "c")],
    )
    assert result["batches"] == [["a"], ["b"], ["c"]]
    assert result["close_times"] == [0.5, 1.1, 1.8]


def test_single_request_batch_size_one():
    result = dynamic_request_batching(
        max_batch_size=1, max_wait_time=5.0,
        arrivals=[(0, "a"), (1, "b")],
    )
    assert result["batches"] == [["a"], ["b"]]
    assert result["close_times"] == [0, 1]


def test_all_requests_fit_in_one_batch():
    result = dynamic_request_batching(
        max_batch_size=5, max_wait_time=1.0,
        arrivals=[(0, "a"), (0.1, "b"), (0.2, "c")],
    )
    assert result["batches"] == [["a", "b", "c"]]
    assert result["close_times"] == [1.0]
