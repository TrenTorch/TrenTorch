"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
truncate_at_stop = _module.truncate_at_stop
safe_emit_length = _module.safe_emit_length


def test_1_truncate_hand_computed():
    assert truncate_at_stop("hello User: hi", ["User:"]) == ("hello ", True)


def test_2_no_stop_returns_text_unchanged():
    assert truncate_at_stop("hello", ["xyz"]) == ("hello", False)


def test_3_earliest_stop_among_several_wins():
    assert truncate_at_stop("a END b STOP c", ["STOP", "END"]) == ("a ", True)


def test_4_empty_stop_is_ignored():
    assert truncate_at_stop("abc", [""]) == ("abc", False)


def test_5_safe_length_holds_back_a_partial_stop():
    assert safe_emit_length("answer\n\nUs", ["\n\nUser:"]) == len("answer")


def test_6_safe_length_is_full_when_no_suffix_matches():
    assert safe_emit_length("hello world", ["User:"]) == 11
    assert safe_emit_length("", ["User:"]) == 0


def test_7_longest_matching_suffix_and_proper_prefix_rule():
    # suffix "ab" is a prefix of "abc"; "b" alone also matches "bd" -> hold the longest (2)
    assert safe_emit_length("xxab", ["abc", "bd"]) == 2
    # a complete stop is not a proper prefix of itself
    assert safe_emit_length("abc", ["abc"]) == 3
