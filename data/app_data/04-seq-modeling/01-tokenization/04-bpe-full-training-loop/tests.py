"""
pytest data/app_data/04-seq-modeling/01-tokenization/04-bpe-full-training-loop/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/01-tokenization/{Path(__file__).resolve().parent.name}")
train_bpe = _module.train_bpe
apply_merges = _module.apply_merges


def _classic_corpus():
    return [list("low")] * 5 + [list("lower")] * 2 + [list("newest")] * 6 + [list("widest")] * 3


def test_train_bpe_returns_the_correct_number_of_merges():
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=6)
    assert len(merges) == 6


def test_train_bpe_first_merge_matches_the_known_classic_example():
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=1)
    assert merges[0] == ("s", "t")


def test_train_bpe_second_merge_builds_on_the_first():
    # After merging ("s","t") -> "st", the next most frequent pair
    # involving "st" is ("e", "st"), which only exists BECAUSE of the
    # first merge.
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=2)
    assert merges[1] == ("e", "st")


def test_train_bpe_final_corpus_reflects_all_merges_applied():
    corpus = _classic_corpus()
    final_corpus, _ = train_bpe(corpus, num_merges=6)
    # "low" (appears 5 times) should end up as a single merged token
    assert final_corpus[0] == ["low"]


def test_apply_merges_reproduces_the_final_training_corpus_on_a_seen_word():
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=6)
    result = apply_merges(list("low"), merges)
    assert result == ["low"]


def test_apply_merges_decomposes_an_unseen_word_gracefully():
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=6)
    # "lowest" was never seen during training, but shares the learned
    # "low" and "est" subword pieces with words that WERE seen.
    result = apply_merges(list("lowest"), merges)
    assert result == ["low", "est"]


def test_apply_merges_with_no_merges_returns_tokens_unchanged():
    result = apply_merges(["a", "b", "c"], merges=[])
    assert result == ["a", "b", "c"]


def test_apply_merges_applies_merges_in_the_given_order_not_reordered():
    # Directly targets a mutant that sorts `merges` (e.g. alphabetically)
    # before applying them instead of using the given order: for a
    # sequence where merge order changes the result, this produces a
    # different final tokenization than the correctly-ordered replay.
    tokens = list("abc")
    # Merge ("a","b") first -> "ab","c", then merge ("ab","c") -> "abc"
    merges_in_order = [("a", "b"), ("ab", "c")]
    result = apply_merges(tokens, merges_in_order)
    assert result == ["abc"]


def test_train_bpe_feeds_each_steps_output_into_the_next_step():
    # Directly targets a mutant that calls bpe_single_merge_step on the
    # ORIGINAL corpus every iteration instead of the updated one: this
    # would produce the SAME merged pair every single time (since nothing
    # ever changes between iterations), rather than distinct merges.
    corpus = _classic_corpus()
    _, merges = train_bpe(corpus, num_merges=3)
    assert len(set(merges)) == 3
