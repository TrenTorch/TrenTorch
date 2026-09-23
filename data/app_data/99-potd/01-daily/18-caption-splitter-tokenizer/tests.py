"""
pytest data/app_data/99-potd/01-daily/18-caption-splitter-tokenizer/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"99-potd/01-daily/{Path(__file__).resolve().parent.name}")
tokenize = _module.tokenize

VOCAB = {"the": 2, "cat": 3, "sat": 4}


def test_example_matches_the_specs_worked_tokens():
    assert tokenize(VOCAB, "the cat sat on mat") == [2, 3, 4, 1, 1]


def test_multiple_consecutive_spaces_do_not_produce_empty_tokens():
    assert tokenize(VOCAB, "the   cat  sat") == [2, 3, 4]


def test_tab_separated_caption_splits_correctly():
    assert tokenize(VOCAB, "the\tcat\tsat") == [2, 3, 4]


def test_every_word_out_of_vocabulary_is_all_unk():
    assert tokenize(VOCAB, "foo bar baz") == [1, 1, 1]


def test_empty_caption_returns_an_empty_list():
    assert tokenize(VOCAB, "") == []
    assert tokenize(VOCAB, "   ") == []


def test_leading_and_trailing_whitespace_is_ignored():
    assert tokenize(VOCAB, "  the cat  ") == [2, 3]


def test_repeated_words_map_independently():
    assert tokenize(VOCAB, "the the the") == [2, 2, 2]
