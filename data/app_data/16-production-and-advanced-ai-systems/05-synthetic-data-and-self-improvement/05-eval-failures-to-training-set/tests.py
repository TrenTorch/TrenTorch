"""pytest data/app_data/16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/05-eval-failures-to-training-set/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

failures_to_training_examples = load_solution(
    f"16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/{Path(__file__).resolve().parent.name}"
).failures_to_training_examples


def test_1_only_failures_are_kept():
    results = [("2+2?", "4", True), ("3+3?", "7", False)]
    assert failures_to_training_examples(results) == [{"input": "3+3?", "expected_output": "7"}]


def test_2_all_passing_returns_empty_list():
    results = [("a", "1", True), ("b", "2", True)]
    assert failures_to_training_examples(results) == []


def test_3_all_failing_returns_all():
    results = [("a", "1", False), ("b", "2", False)]
    assert failures_to_training_examples(results) == [
        {"input": "a", "expected_output": "1"},
        {"input": "b", "expected_output": "2"},
    ]


def test_4_order_preserved():
    results = [("a", "1", False), ("b", "2", True), ("c", "3", False)]
    assert failures_to_training_examples(results) == [
        {"input": "a", "expected_output": "1"},
        {"input": "c", "expected_output": "3"},
    ]


def test_5_empty_results_returns_empty_list():
    assert failures_to_training_examples([]) == []
