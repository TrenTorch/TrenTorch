"""
pytest data/app_data/06-inference/04-batching-and-serving-metrics/04-simulate-continuous-batching/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

simulate_continuous_batching = load_solution(
    f"06-inference/04-batching-and-serving-metrics/{Path(__file__).resolve().parent.name}"
).simulate_continuous_batching


def test_example_from_description():
    result = simulate_continuous_batching(
        max_batch_size=2,
        requests=[[0, "A", 3], [0, "B", 1], [0, "C", 2]],
    )
    # B finishes fastest (1 token), freeing a slot for C immediately.
    assert result["admitted_step"]["A"] == 0
    assert result["admitted_step"]["B"] == 0
    assert result["admitted_step"]["C"] == 1  # admitted the step B's slot freed
    assert result["finished_step"]["B"] == 0
    assert result["finished_step"]["A"] == 2
    assert result["finished_step"]["C"] == 2


def test_requests_arriving_over_time_never_oversubscribed():
    result = simulate_continuous_batching(
        max_batch_size=1,
        requests=[[0, "A", 2], [1, "B", 1]],
    )
    assert result["admitted_step"]["A"] == 0
    assert result["finished_step"]["A"] == 1
    assert result["admitted_step"]["B"] == 2  # A's slot frees at step 2
    assert result["finished_step"]["B"] == 2


def test_all_requests_same_length():
    result = simulate_continuous_batching(
        max_batch_size=3,
        requests=[[0, "A", 2], [0, "B", 2], [0, "C", 2]],
    )
    assert all(result["admitted_step"][r] == 0 for r in ("A", "B", "C"))
    assert all(result["finished_step"][r] == 1 for r in ("A", "B", "C"))
    assert result["total_steps"] == 2


def test_every_request_eventually_finishes():
    result = simulate_continuous_batching(
        max_batch_size=2,
        requests=[[0, "A", 5], [0, "B", 3], [2, "C", 1], [4, "D", 2]],
    )
    for rid in ("A", "B", "C", "D"):
        assert rid in result["finished_step"]
