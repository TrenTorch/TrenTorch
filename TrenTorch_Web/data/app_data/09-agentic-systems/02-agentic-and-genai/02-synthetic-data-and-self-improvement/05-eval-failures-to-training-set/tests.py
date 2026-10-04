"""pytest tests.py"""

from _load import load_solution

failures_to_training_examples = load_solution(__file__).failures_to_training_examples


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
