"""pytest data/app_data/16-production-and-advanced-ai-systems/02-streaming-and-real-time-agents/02-detect-early-tool-call-in-stream/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

detect_early_tool_call = load_solution(
    f"16-production-and-advanced-ai-systems/02-streaming-and-real-time-agents/{Path(__file__).resolve().parent.name}"
).detect_early_tool_call


def test_1_marker_appears_within_a_single_chunk():
    chunks = ["Sure, let me ", "<tool_call>search", "</tool_call>"]
    assert detect_early_tool_call(chunks, "<tool_call>") == 1


def test_2_marker_never_appears_returns_none():
    chunks = ["Just a ", "plain text ", "answer."]
    assert detect_early_tool_call(chunks, "<tool_call>") is None


def test_3_marker_split_across_chunk_boundary_detected():
    chunks = ["prefix <tool_", "call>rest"]
    assert detect_early_tool_call(chunks, "<tool_call>") == 1


def test_4_marker_in_first_chunk():
    chunks = ["<tool_call>", "more text"]
    assert detect_early_tool_call(chunks, "<tool_call>") == 0


def test_5_empty_chunks_returns_none():
    assert detect_early_tool_call([], "<tool_call>") is None
