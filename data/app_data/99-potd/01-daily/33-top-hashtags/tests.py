"""
pytest data/app_data/99-potd/01-daily/33-top-hashtags/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
top_k_hashtags = _module.top_k_hashtags


def test_example_matches_the_specs_worked_ranking():
    captions = ["#fyp #dance #fyp #comedy #fyp #dance #viral"]
    assert top_k_hashtags(2, captions) == [("#fyp", 3), ("#dance", 2)]


def test_tie_broken_by_earliest_first_appearance_not_alphabetical():
    # #b and #a both end at count 1; #b appears first in the input, so it
    # must win the tie even though "#a" would sort first alphabetically.
    captions = ["#b #a #c #c"]
    result = top_k_hashtags(2, captions)
    assert result[0] == ("#c", 2)
    assert result[1] == ("#b", 1)


def test_k_larger_than_distinct_hashtags_returns_fewer_lines():
    captions = ["#only #only"]
    result = top_k_hashtags(5, captions)
    assert result == [("#only", 2)]


def test_case_sensitivity_treats_different_case_as_distinct():
    captions = ["#FYP #fyp #FYP"]
    result = top_k_hashtags(2, captions)
    tags = dict(result)
    assert tags["#FYP"] == 2
    assert tags["#fyp"] == 1


def test_non_hashtag_words_are_ignored():
    captions = ["just a caption with #one hashtag and #two"]
    result = top_k_hashtags(5, captions)
    assert dict(result) == {"#one": 1, "#two": 1}


def test_hashtags_spread_across_multiple_captions():
    captions = ["#a #b", "#b #b", "#a"]
    result = top_k_hashtags(2, captions)
    assert result[0] == ("#b", 3)
    assert result[1] == ("#a", 2)
