from collections import Counter


def get_pair_frequencies(corpus: list[list[str]]) -> Counter:
    """
    Counts how many times every ADJACENT pair of tokens appears across
    the whole corpus (a list of token-lists, e.g. each word already
    split into characters). Returns a Counter mapping (token_a, token_b)
    pairs to their total count.
    """
    pass


def merge_pair(corpus: list[list[str]], pair: tuple[str, str]) -> list[list[str]]:
    """
    Returns a NEW corpus where every adjacent occurrence of `pair` in
    every sequence has been replaced by a single merged token (the two
    original tokens concatenated together). Merges are applied
    left-to-right within each sequence, non-overlapping (once two tokens
    are merged, the merged result isn't itself immediately re-matched
    against the very next token in the same pass).
    """
    merged_token = pair[0] + pair[1]
    pass


def bpe_single_merge_step(corpus: list[list[str]]) -> tuple[list[list[str]], tuple[str, str]]:
    """
    One full step of the BPE algorithm: find the MOST frequent adjacent
    pair across the whole corpus (using get_pair_frequencies; ties
    broken by picking the alphabetically greater pair, for determinism),
    merge every occurrence of it (using merge_pair), and return
    (new_corpus, the_pair_that_was_merged).
    """
    pass
