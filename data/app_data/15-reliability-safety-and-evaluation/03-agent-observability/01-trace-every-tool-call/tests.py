"""pytest data/app_data/15-reliability-safety-and-evaluation/03-agent-observability/01-trace-every-tool-call/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

build_trace = load_solution(
    f"15-reliability-safety-and-evaluation/03-agent-observability/{Path(__file__).resolve().parent.name}"
).build_trace


def test_1_single_event_starts_at_zero():
    result = build_trace([("call_llm", "llm", 1.5)])
    assert result == [{"name": "call_llm", "kind": "llm", "start_offset": 0.0, "duration": 1.5}]


def test_2_second_event_offset_by_first_duration():
    result = build_trace([("call_llm", "llm", 1.5), ("search_web", "tool", 0.8)])
    assert result[1] == {"name": "search_web", "kind": "tool", "start_offset": 1.5, "duration": 0.8}


def test_3_three_events_cumulative_offsets():
    events = [("a", "llm", 1.0), ("b", "tool", 2.0), ("c", "tool", 0.5)]
    result = build_trace(events)
    assert [e["start_offset"] for e in result] == [0.0, 1.0, 3.0]


def test_4_empty_events_returns_empty_list():
    assert build_trace([]) == []


def test_5_zero_duration_event_does_not_shift_next_offset():
    events = [("a", "llm", 0.0), ("b", "tool", 1.0)]
    result = build_trace(events)
    assert result[1]["start_offset"] == 0.0
