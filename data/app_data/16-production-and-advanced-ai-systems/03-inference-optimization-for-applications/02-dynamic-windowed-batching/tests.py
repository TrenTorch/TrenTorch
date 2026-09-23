"""pytest data/app_data/16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/02-dynamic-windowed-batching/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

batch_requests = load_solution(
    f"16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/{Path(__file__).resolve().parent.name}"
).batch_requests


def test_1_all_within_window_and_size_form_one_batch():
    requests = [(0.0, "a"), (5.0, "b"), (10.0, "c")]
    assert batch_requests(requests, max_batch_size=4, max_wait_ms=20.0) == [["a", "b", "c"]]


def test_2_batch_closes_at_max_size():
    requests = [(0.0, "a"), (1.0, "b"), (2.0, "c"), (3.0, "d")]
    assert batch_requests(requests, max_batch_size=2, max_wait_ms=100.0) == [["a", "b"], ["c", "d"]]


def test_3_batch_closes_when_wait_exceeded():
    requests = [(0.0, "a"), (5.0, "b"), (50.0, "c")]
    assert batch_requests(requests, max_batch_size=10, max_wait_ms=20.0) == [["a", "b"], ["c"]]


def test_4_single_request_forms_its_own_batch():
    assert batch_requests([(0.0, "a")], max_batch_size=4, max_wait_ms=20.0) == [["a"]]


def test_5_empty_requests_returns_empty_list():
    assert batch_requests([], max_batch_size=4, max_wait_ms=20.0) == []
