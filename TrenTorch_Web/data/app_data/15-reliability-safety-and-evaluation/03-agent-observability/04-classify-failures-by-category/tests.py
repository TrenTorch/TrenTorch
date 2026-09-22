"""pytest data/app_data/15-reliability-safety-and-evaluation/03-agent-observability/04-classify-failures-by-category/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

classify_failures = load_solution(
    f"15-reliability-safety-and-evaluation/03-agent-observability/{Path(__file__).resolve().parent.name}"
).classify_failures


CATEGORIES = {
    "timeout": ["timed out", "deadline exceeded"],
    "auth": ["401", "unauthorized", "invalid api key"],
    "rate_limit": ["429", "rate limit"],
}


def test_1_single_matching_failure():
    result = classify_failures(["request timed out after 30s"], CATEGORIES)
    assert result["timeout"] == 1
    assert result["auth"] == 0
    assert result["rate_limit"] == 0
    assert result["UNCATEGORIZED"] == 0


def test_2_multiple_failures_across_categories():
    failures = ["401 unauthorized", "429 rate limit hit", "deadline exceeded on tool call"]
    result = classify_failures(failures, CATEGORIES)
    assert result == {"timeout": 1, "auth": 1, "rate_limit": 1, "UNCATEGORIZED": 0}


def test_3_unmatched_failure_goes_to_uncategorized():
    result = classify_failures(["disk full", "out of memory"], CATEGORIES)
    assert result["UNCATEGORIZED"] == 2


def test_4_first_matching_category_wins_on_dict_order():
    # "invalid api key" contains no timeout/rate_limit keyword, only matches "auth".
    categories = {"timeout": ["timed out"], "auth": ["invalid api key"]}
    result = classify_failures(["invalid api key error"], categories)
    assert result["auth"] == 1
    assert result["timeout"] == 0


def test_5_empty_failures_returns_all_zero_counts():
    result = classify_failures([], CATEGORIES)
    assert result == {"timeout": 0, "auth": 0, "rate_limit": 0, "UNCATEGORIZED": 0}
