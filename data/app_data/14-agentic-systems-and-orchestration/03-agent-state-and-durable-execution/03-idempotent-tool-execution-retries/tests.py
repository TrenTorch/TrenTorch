"""
pytest data/app_data/14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/03-idempotent-tool-execution-retries/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

dedupe_idempotent_calls = load_solution(
    f"14-agentic-systems-and-orchestration/03-agent-state-and-durable-execution/{Path(__file__).resolve().parent.name}"
).dedupe_idempotent_calls


def test_1_no_repeats_everything_executes():
    assert dedupe_idempotent_calls(["a", "b", "c"]) == [("a", True), ("b", True), ("c", True)]


def test_2_immediate_retry_is_skipped():
    assert dedupe_idempotent_calls(["a", "a"]) == [("a", True), ("a", False)]


def test_3_retry_after_other_calls_in_between_still_skipped():
    assert dedupe_idempotent_calls(["a", "b", "a"]) == [
        ("a", True),
        ("b", True),
        ("a", False),
    ]


def test_4_many_retries_of_the_same_key():
    result = dedupe_idempotent_calls(["x", "x", "x", "x"])
    assert result == [("x", True), ("x", False), ("x", False), ("x", False)]


def test_5_empty_log():
    assert dedupe_idempotent_calls([]) == []


def test_6_single_call_no_retry():
    assert dedupe_idempotent_calls(["only"]) == [("only", True)]


def test_7_interleaved_retries_of_two_different_keys():
    result = dedupe_idempotent_calls(["a", "b", "a", "b", "a"])
    assert result == [
        ("a", True),
        ("b", True),
        ("a", False),
        ("b", False),
        ("a", False),
    ]
