"""
pytest data/app_data/15-reliability-safety-and-evaluation/01-guardrails-retry-and-evaluation/01-enforce-valid-format-retry/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

enforce_format_with_retry = load_solution(
    f"15-reliability-safety-and-evaluation/01-guardrails-retry-and-evaluation/{Path(__file__).resolve().parent.name}"
).enforce_format_with_retry

LABELS = {"POSITIVE", "NEGATIVE", "NEUTRAL"}


def test_1_first_attempt_already_valid():
    assert enforce_format_with_retry(3, ["POSITIVE"], LABELS) == "SUCCESS 1"


def test_2_second_attempt_recovers():
    assert enforce_format_with_retry(3, ["maybe positive?", "POSITIVE"], LABELS) == "SUCCESS 2"


def test_3_budget_exhausted_before_a_valid_attempt():
    attempts = ["bad", "bad", "POSITIVE"]
    assert enforce_format_with_retry(1, attempts, LABELS) == "FAILURE 2"


def test_4_whitespace_around_a_valid_label_is_stripped():
    assert enforce_format_with_retry(3, ["  NEUTRAL  "], LABELS) == "SUCCESS 1"


def test_5_case_sensitive_matching():
    assert enforce_format_with_retry(3, ["positive"], LABELS) == "FAILURE 1"


def test_6_budget_larger_than_the_log():
    assert enforce_format_with_retry(10, ["bad", "bad"], LABELS) == "FAILURE 2"


def test_7_never_valid_exhausts_the_full_budget():
    attempts = ["x", "y", "z"]
    assert enforce_format_with_retry(2, attempts, LABELS) == "FAILURE 3"
