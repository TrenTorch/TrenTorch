"""
pytest data/app_data/14-agentic-systems-and-orchestration/02-multi-agent-orchestration/03-handoff-route-to-right-agent/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

route_handoff = load_solution(
    f"14-agentic-systems-and-orchestration/02-multi-agent-orchestration/{Path(__file__).resolve().parent.name}"
).route_handoff

RULES = [
    ("refund", "billing_agent"),
    ("bug", "engineering_agent"),
    ("cancel", "billing_agent"),
]


def test_1_keyword_match_routes_to_target():
    assert route_handoff("general_agent", "I want a refund please", RULES) == "billing_agent"


def test_2_no_keyword_match_stays_with_current_agent():
    assert route_handoff("general_agent", "what are your hours?", RULES) == "general_agent"


def test_3_first_matching_rule_wins_when_multiple_match():
    rules = [("issue", "support_agent"), ("bug", "engineering_agent")]
    assert route_handoff("general_agent", "I found a bug, it's an issue", rules) == "support_agent"


def test_4_case_insensitive_matching():
    assert route_handoff("general_agent", "Please REFUND my order", RULES) == "billing_agent"


def test_5_two_different_keywords_route_to_the_same_agent():
    assert route_handoff("general_agent", "I want to cancel", RULES) == "billing_agent"


def test_6_keyword_as_substring_of_a_larger_word_still_matches():
    assert route_handoff("general_agent", "debugging this issue", RULES) == "engineering_agent"


def test_7_empty_routing_rules_always_stays():
    assert route_handoff("general_agent", "a bug and a refund", []) == "general_agent"


def test_8_already_with_the_target_agent_no_effective_change():
    assert route_handoff("billing_agent", "another refund request", RULES) == "billing_agent"
