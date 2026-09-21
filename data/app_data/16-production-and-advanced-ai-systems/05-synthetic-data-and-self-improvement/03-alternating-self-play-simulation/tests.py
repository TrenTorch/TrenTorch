"""pytest data/app_data/16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/03-alternating-self-play-simulation/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

simulate_self_play = load_solution(
    f"16-production-and-advanced-ai-systems/05-synthetic-data-and-self-improvement/{Path(__file__).resolve().parent.name}"
).simulate_self_play


def test_1_alternates_starting_with_a():
    result = simulate_self_play(["a1", "a2"], ["b1", "b2"], max_turns=4)
    assert result == [("A", "a1"), ("B", "b1"), ("A", "a2"), ("B", "b2")]


def test_2_max_turns_caps_the_transcript():
    result = simulate_self_play(["a1", "a2"], ["b1", "b2"], max_turns=2)
    assert result == [("A", "a1"), ("B", "b1")]


def test_3_stops_early_when_an_agent_runs_out_of_moves():
    result = simulate_self_play(["a1"], ["b1", "b2"], max_turns=10)
    assert result == [("A", "a1"), ("B", "b1")]


def test_4_zero_max_turns_returns_empty_list():
    assert simulate_self_play(["a1"], ["b1"], max_turns=0) == []


def test_5_no_moves_at_all_returns_empty_list():
    assert simulate_self_play([], [], max_turns=5) == []
