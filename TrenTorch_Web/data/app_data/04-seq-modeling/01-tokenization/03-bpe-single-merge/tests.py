"""
pytest data/app_data/04-seq-modeling/01-tokenization/03-bpe-single-merge/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/01-tokenization/{Path(__file__).resolve().parent.name}")
get_pair_frequencies = _module.get_pair_frequencies
merge_pair = _module.merge_pair
bpe_single_merge_step = _module.bpe_single_merge_step


def test_get_pair_frequencies_matches_hand_computation():
    corpus = [["a", "b", "c"]]
    counts = get_pair_frequencies(corpus)
    assert counts[("a", "b")] == 1
    assert counts[("b", "c")] == 1


def test_get_pair_frequencies_accumulates_across_sequences():
    corpus = [["a", "b"], ["a", "b"], ["a", "b"]]
    counts = get_pair_frequencies(corpus)
    assert counts[("a", "b")] == 3


def test_get_pair_frequencies_does_not_count_across_sequence_boundaries():
    corpus = [["a", "b"], ["c", "d"]]
    counts = get_pair_frequencies(corpus)
    assert ("b", "c") not in counts


def test_merge_pair_replaces_every_occurrence():
    corpus = [["s", "t", "a", "r", "s", "t"]]
    result = merge_pair(corpus, ("s", "t"))
    assert result == [["st", "a", "r", "st"]]


def test_merge_pair_leaves_non_matching_sequences_unchanged():
    corpus = [["x", "y", "z"]]
    result = merge_pair(corpus, ("a", "b"))
    assert result == [["x", "y", "z"]]


def test_merge_pair_does_not_overlap_merges():
    # "aaa" with pair ("a","a"): merges positions 0-1, then position 2 is
    # a leftover single "a" (not merged with the already-merged "aa").
    corpus = [["a", "a", "a"]]
    result = merge_pair(corpus, ("a", "a"))
    assert result == [["aa", "a"]]


def test_merge_pair_produces_concatenated_token():
    corpus = [["l", "o"]]
    result = merge_pair(corpus, ("l", "o"))
    assert result == [["lo"]]


def test_bpe_single_merge_step_picks_the_most_frequent_pair():
    corpus = [list("low")] * 5 + [list("lower")] * 2 + [list("newest")] * 6 + [list("widest")] * 3
    _, merged_pair = bpe_single_merge_step(corpus)
    assert merged_pair == ("s", "t")


def test_bpe_single_merge_step_actually_merges_in_the_returned_corpus():
    corpus = [["s", "t"], ["s", "t"], ["a", "b"]]
    new_corpus, merged_pair = bpe_single_merge_step(corpus)
    assert merged_pair == ("s", "t")
    assert new_corpus[0] == ["st"]
    assert new_corpus[1] == ["st"]
    assert new_corpus[2] == ["a", "b"]


def test_bpe_single_merge_step_breaks_ties_alphabetically_greater():
    # ("a","b") and ("c","d") both occur once: alphabetically ("c","d") > ("a","b")
    corpus = [["a", "b"], ["c", "d"]]
    _, merged_pair = bpe_single_merge_step(corpus)
    assert merged_pair == ("c", "d")


def test_merge_pair_scans_left_to_right_not_right_to_left():
    # Directly targets a mutant that scans the sequence in REVERSE
    # (right-to-left) instead of left-to-right: for "aaa" with pair
    # ("a","a"), scanning right-to-left would merge positions 1-2 first,
    # leaving a leftover "a" at the START instead of the end.
    corpus = [["a", "a", "a"]]
    result = merge_pair(corpus, ("a", "a"))
    assert result == [["aa", "a"]]
    assert result != [["a", "aa"]]
