"""
pytest data/app_data/06-inference/04-batching-and-serving-metrics/05-chunked-prefill-scheduling/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

chunked_prefill_scheduling = load_solution(
    f"06-inference/04-batching-and-serving-metrics/{Path(__file__).resolve().parent.name}"
).chunked_prefill_scheduling


def test_example_from_description():
    result = chunked_prefill_scheduling(
        token_budget=5, n_decode_tokens_each=2,
        requests=[[0, "decode0", 1]],
    )
    assert result["prefill_done_step"] == {"decode0": 0}
    assert result["completed_step"] == {"decode0": 2}


def test_single_long_prefill_no_concurrent_decode():
    result = chunked_prefill_scheduling(
        token_budget=4, n_decode_tokens_each=3,
        requests=[[0, "A", 10]],
    )
    assert result["prefill_done_step"]["A"] == 2  # ceil(10/4) - 1 chunks needed, done on the 3rd
    assert result["completed_step"]["A"] == 5


def test_two_requests_one_arrives_later():
    result = chunked_prefill_scheduling(
        token_budget=3, n_decode_tokens_each=2,
        requests=[[0, "A", 5], [1, "B", 2]],
    )
    assert result["prefill_done_step"] == {"A": 1, "B": 2}
    assert result["completed_step"] == {"A": 3, "B": 4}


def test_decode_requests_always_prioritized_over_prefill():
    # A finishes prefill and starts decoding; a second request's prefill
    # must never starve A's decode step once A is decoding.
    result = chunked_prefill_scheduling(
        token_budget=2, n_decode_tokens_each=1,
        requests=[[0, "A", 1], [0, "B", 100]],
    )
    # A's 1-token prefill finishes immediately at step 0.
    assert result["prefill_done_step"]["A"] == 0
    # A starts decoding at step 1 and must get its 1 decode token then,
    # regardless of B's huge pending prefill.
    assert result["completed_step"]["A"] == 1


def test_every_request_eventually_completes():
    result = chunked_prefill_scheduling(
        token_budget=3, n_decode_tokens_each=2,
        requests=[[0, "A", 4], [0, "B", 4], [2, "C", 2]],
    )
    for rid in ("A", "B", "C"):
        assert rid in result["prefill_done_step"]
        assert rid in result["completed_step"]
