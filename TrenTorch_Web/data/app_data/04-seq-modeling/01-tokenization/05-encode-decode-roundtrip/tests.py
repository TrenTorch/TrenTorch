"""
pytest data/app_data/04-seq-modeling/01-tokenization/05-encode-decode-roundtrip/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/01-tokenization/{Path(__file__).resolve().parent.name}")
encode = _module.encode
build_inverse_vocab = _module.build_inverse_vocab
decode = _module.decode

_build_vocabulary = load_solution(
    "04-seq-modeling/01-tokenization/02-vocabulary-building"
).build_vocabulary


def _sample_vocab():
    return _build_vocabulary([["the", "cat", "sat", "on", "the", "mat"]])


def test_encode_matches_hand_computation():
    vocab = {"<unk>": 0, "cat": 1, "dog": 2}
    result = encode("cat dog cat", vocab)
    assert result == [1, 2, 1]


def test_encode_maps_unknown_words_to_unk_id():
    vocab = {"<unk>": 0, "cat": 1}
    result = encode("cat elephant", vocab)
    assert result == [1, 0]


def test_build_inverse_vocab_correctly_inverts_every_entry():
    vocab = {"<unk>": 0, "cat": 1, "dog": 2}
    inverse = build_inverse_vocab(vocab)
    assert inverse == {0: "<unk>", 1: "cat", 2: "dog"}


def test_decode_matches_hand_computation():
    vocab = {"<unk>": 0, "cat": 1, "dog": 2}
    result = decode([1, 2, 1], vocab)
    assert result == "cat dog cat"


def test_decode_joins_tokens_with_single_spaces():
    vocab = {"<unk>": 0, "a": 1, "b": 2, "c": 3}
    result = decode([1, 2, 3], vocab)
    assert result == "a b c"
    assert "  " not in result  # no double spaces


def test_round_trip_reproduces_the_original_word_sequence_for_known_words():
    vocab = _sample_vocab()
    text = "the cat sat on the mat"
    ids = encode(text, vocab)
    result = decode(ids, vocab)
    assert result == text


def test_round_trip_handles_unknown_words_via_unk_token():
    vocab = _sample_vocab()
    ids = encode("the cat flew", vocab)
    result = decode(ids, vocab)
    assert result == "the cat <unk>"


def test_round_trip_normalizes_extra_whitespace():
    vocab = _sample_vocab()
    ids = encode("the    cat   sat", vocab)
    result = decode(ids, vocab)
    assert result == "the cat sat"


def test_decode_uses_the_inverse_vocab_correctly_for_every_id_including_zero():
    # Directly targets a mutant that builds the inverse vocab off-by-one
    # or skips id 0, which would silently corrupt decoding for the very
    # first vocabulary entry (commonly <unk>).
    vocab = {"<unk>": 0, "only_word": 1}
    result = decode([0], vocab)
    assert result == "<unk>"
