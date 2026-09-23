"""pytest data/app_data/15-reliability-safety-and-evaluation/02-agent-security/04-sanitize-tool-output/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

sanitize_tool_output = load_solution(
    f"15-reliability-safety-and-evaluation/02-agent-security/{Path(__file__).resolve().parent.name}"
).sanitize_tool_output


def test_1_no_forbidden_patterns_present():
    assert sanitize_tool_output("the weather is sunny today", ["password", "ssn"]) == (
        "the weather is sunny today"
    )


def test_2_single_pattern_redacted():
    assert sanitize_tool_output("api_key=sk-12345 is active", ["sk-12345"]) == (
        "api_key=[REDACTED] is active"
    )


def test_3_multiple_patterns_redacted():
    result = sanitize_tool_output("user ssn is 123-45-6789, email is a@b.com", ["123-45-6789", "a@b.com"])
    assert result == "user ssn is [REDACTED], email is [REDACTED]"


def test_4_repeated_pattern_redacted_every_occurrence():
    assert sanitize_tool_output("secret secret secret", ["secret"]) == (
        "[REDACTED] [REDACTED] [REDACTED]"
    )


def test_5_patterns_applied_in_given_order():
    # "ab" gets redacted first, so a later pattern "a" can no longer match
    # inside the already-redacted text -- order matters.
    assert sanitize_tool_output("ab", ["ab", "a"]) == "[REDACTED]"


def test_6_empty_forbidden_list_returns_unchanged():
    assert sanitize_tool_output("nothing to hide here", []) == "nothing to hide here"
