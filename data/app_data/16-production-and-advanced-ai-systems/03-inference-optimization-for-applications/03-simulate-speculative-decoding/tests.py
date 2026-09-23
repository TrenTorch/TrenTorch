"""pytest data/app_data/16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/03-simulate-speculative-decoding/tests.py"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

simulate_speculative_decoding = load_solution(
    f"16-production-and-advanced-ai-systems/03-inference-optimization-for-applications/{Path(__file__).resolve().parent.name}"
).simulate_speculative_decoding


def test_1_full_draft_accepted_no_bonus_beyond_target_length():
    assert simulate_speculative_decoding(["a", "b", "c"], ["a", "b", "c"]) == (3, ["a", "b", "c"])


def test_2_mismatch_partway_stops_acceptance_and_appends_correction():
    assert simulate_speculative_decoding(["a", "x", "c"], ["a", "b", "c"]) == (1, ["a", "b"])


def test_3_mismatch_on_first_token():
    assert simulate_speculative_decoding(["x", "y"], ["a", "b"]) == (0, ["a"])


def test_4_draft_shorter_than_target_gets_one_bonus_token():
    assert simulate_speculative_decoding(["a", "b"], ["a", "b", "c", "d"]) == (2, ["a", "b", "c"])


def test_5_empty_draft_still_yields_one_target_token():
    assert simulate_speculative_decoding([], ["a"]) == (0, ["a"])


def test_6_empty_target_yields_no_output():
    assert simulate_speculative_decoding(["a"], []) == (0, [])
