"""
pytest data/app_data/14-agentic-systems-and-orchestration/02-multi-agent-orchestration/02-message-passing-shared-state/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

process_message_log = load_solution(
    f"14-agentic-systems-and-orchestration/02-multi-agent-orchestration/{Path(__file__).resolve().parent.name}"
).process_message_log


def test_1_single_write_per_key():
    messages = [("agent_a", "status", "researching"), ("agent_b", "draft", "hello world")]
    assert process_message_log(messages) == {
        "status": ("researching", "agent_a"),
        "draft": ("hello world", "agent_b"),
    }


def test_2_later_write_overwrites_earlier_one_to_same_key():
    messages = [
        ("agent_a", "status", "researching"),
        ("agent_b", "status", "writing"),
    ]
    assert process_message_log(messages) == {"status": ("writing", "agent_b")}


def test_3_same_agent_can_overwrite_its_own_earlier_write():
    messages = [("agent_a", "status", "step1"), ("agent_a", "status", "step2")]
    assert process_message_log(messages) == {"status": ("step2", "agent_a")}


def test_4_multiple_keys_tracked_independently():
    messages = [
        ("agent_a", "k1", "v1"),
        ("agent_b", "k2", "v2"),
        ("agent_a", "k1", "v1b"),
    ]
    assert process_message_log(messages) == {
        "k1": ("v1b", "agent_a"),
        "k2": ("v2", "agent_b"),
    }


def test_5_empty_log_yields_empty_state():
    assert process_message_log([]) == {}


def test_6_three_agents_writing_to_the_same_key_in_sequence():
    messages = [
        ("a", "shared", "1"),
        ("b", "shared", "2"),
        ("c", "shared", "3"),
    ]
    assert process_message_log(messages) == {"shared": ("3", "c")}
