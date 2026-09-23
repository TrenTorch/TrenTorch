"""pytest data/app_data/16-production-and-advanced-ai-systems/02-streaming-and-real-time-agents/05-process-out-of-order-event-queue/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

process_event_queue = load_solution(
    f"16-production-and-advanced-ai-systems/02-streaming-and-real-time-agents/{Path(__file__).resolve().parent.name}"
).process_event_queue


HANDLERS = {"chunk": "text: {}", "tool_call": "calling tool {}"}


def test_1_already_in_order():
    events = [(1.0, "chunk", "Hel"), (2.0, "chunk", "lo")]
    assert process_event_queue(events, HANDLERS) == ["text: Hel", "text: lo"]


def test_2_out_of_order_events_are_sorted_by_timestamp():
    events = [(3.0, "chunk", "world"), (1.0, "chunk", "Hello, ")]
    assert process_event_queue(events, HANDLERS) == ["text: Hello, ", "text: world"]


def test_3_unhandled_event_type_is_skipped():
    events = [(1.0, "chunk", "a"), (2.0, "unknown_type", "b"), (3.0, "chunk", "c")]
    assert process_event_queue(events, HANDLERS) == ["text: a", "text: c"]


def test_4_mixed_event_types_formatted_by_their_own_handler():
    events = [(2.0, "tool_call", "search"), (1.0, "chunk", "thinking...")]
    assert process_event_queue(events, HANDLERS) == ["text: thinking...", "calling tool search"]


def test_5_empty_events_returns_empty_list():
    assert process_event_queue([], HANDLERS) == []
