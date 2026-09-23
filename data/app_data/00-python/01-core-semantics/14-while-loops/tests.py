"""
pytest data/app_data/00-python/01-core-semantics/14-while-loops/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
countdown_with_skip = _module.countdown_with_skip
find_first_negative = _module.find_first_negative


def test_countdown_with_skip_correct_sequence():
    assert countdown_with_skip(5) == [5, 4, 2, 1]


def test_countdown_with_skip_no_three_in_range():
    assert countdown_with_skip(2) == [2, 1]


def test_find_first_negative_finds_early_match_via_break():
    # -1 comes first; a later -99 must not be what's returned.
    assert find_first_negative([5, -1, 3, -99]) == -1


def test_find_first_negative_returns_none_via_loop_else():
    assert find_first_negative([1, 2, 3]) is None


def test_find_first_negative_edge_cases():
    assert find_first_negative([]) is None
    assert find_first_negative([-7]) == -7
    assert find_first_negative([7]) is None
