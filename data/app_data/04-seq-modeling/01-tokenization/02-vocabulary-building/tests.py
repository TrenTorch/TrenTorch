"""
pytest data/app_data/04-seq-modeling/01-tokenization/02-vocabulary-building/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/01-tokenization/{Path(__file__).resolve().parent.name}")
build_vocabulary = _module.build_vocabulary
encode_with_unk = _module.encode_with_unk


def test_unk_token_is_always_id_zero():
    vocab = build_vocabulary([["the", "cat"]])
    assert vocab["<unk>"] == 0


def test_vocabulary_assigns_ids_by_descending_frequency():
    token_lists = [["a", "a", "a", "b", "b", "c"]]
    vocab = build_vocabulary(token_lists)
    assert vocab["a"] == 1  # most frequent -> first id after <unk>
    assert vocab["b"] == 2
    assert vocab["c"] == 3


def test_ties_are_broken_alphabetically():
    token_lists = [["z", "a", "m"]]  # all frequency 1
    vocab = build_vocabulary(token_lists)
    assert vocab["a"] == 1
    assert vocab["m"] == 2
    assert vocab["z"] == 3


def test_min_freq_excludes_rare_tokens():
    token_lists = [["common", "common", "common", "rare"]]
    vocab = build_vocabulary(token_lists, min_freq=2)
    assert "common" in vocab
    assert "rare" not in vocab


def test_min_freq_one_includes_everything():
    token_lists = [["a", "b", "c"]]
    vocab = build_vocabulary(token_lists, min_freq=1)
    assert "a" in vocab and "b" in vocab and "c" in vocab


def test_counts_are_accumulated_across_multiple_sequences():
    token_lists = [["cat", "dog"], ["cat"], ["cat", "dog", "dog", "dog"]]
    vocab = build_vocabulary(token_lists)
    # cat: 3 total, dog: 4 total -> dog should come first (more frequent)
    assert vocab["dog"] == 1
    assert vocab["cat"] == 2


def test_custom_unk_token_name_is_respected():
    vocab = build_vocabulary([["a", "b"]], unk_token="<missing>")
    assert vocab["<missing>"] == 0
    assert "<unk>" not in vocab


def test_encode_with_unk_maps_known_tokens_to_their_ids():
    vocab = {"<unk>": 0, "cat": 1, "dog": 2}
    result = encode_with_unk(["cat", "dog", "cat"], vocab)
    assert result == [1, 2, 1]


def test_encode_with_unk_maps_unknown_tokens_to_unk_id():
    vocab = {"<unk>": 0, "cat": 1}
    result = encode_with_unk(["cat", "elephant"], vocab)
    assert result == [1, 0]


def test_encode_with_unk_never_raises_a_key_error():
    vocab = {"<unk>": 0}
    result = encode_with_unk(["totally", "unseen", "words"], vocab)
    assert result == [0, 0, 0]


def test_full_pipeline_build_then_encode():
    token_lists = [["the", "cat", "sat"], ["the", "dog", "ran"]]
    vocab = build_vocabulary(token_lists)
    encoded = encode_with_unk(["the", "cat", "flew"], vocab)
    assert encoded[0] == vocab["the"]
    assert encoded[1] == vocab["cat"]
    assert encoded[2] == vocab["<unk>"]


def test_vocabulary_ordering_uses_count_first_not_alphabetical_first():
    # Directly targets a mutant that sorts by (token, -count) instead of
    # (-count, token), i.e. alphabetical order taking priority over
    # frequency: this would put a rare, alphabetically-early token before
    # a much more frequent, alphabetically-later one.
    token_lists = [["zzz", "zzz", "zzz", "aaa"]]
    vocab = build_vocabulary(token_lists)
    assert vocab["zzz"] == 1  # far more frequent, must come first
    assert vocab["aaa"] == 2
