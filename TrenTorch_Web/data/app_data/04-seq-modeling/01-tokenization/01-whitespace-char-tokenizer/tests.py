"""
pytest data/app_data/04-seq-modeling/01-tokenization/01-whitespace-char-tokenizer/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"04-seq-modeling/01-tokenization/{Path(__file__).resolve().parent.name}")
whitespace_tokenize = _module.whitespace_tokenize
char_tokenize = _module.char_tokenize


def test_whitespace_tokenize_splits_on_single_spaces():
    assert whitespace_tokenize("the cat sat") == ["the", "cat", "sat"]


def test_whitespace_tokenize_collapses_multiple_spaces():
    assert whitespace_tokenize("the   cat  sat") == ["the", "cat", "sat"]


def test_whitespace_tokenize_strips_leading_and_trailing_whitespace():
    assert whitespace_tokenize("  hello world  ") == ["hello", "world"]


def test_whitespace_tokenize_handles_tabs_and_newlines():
    assert whitespace_tokenize("hello\tworld\nagain") == ["hello", "world", "again"]


def test_whitespace_tokenize_empty_string_returns_empty_list():
    assert whitespace_tokenize("") == []


def test_whitespace_tokenize_all_whitespace_returns_empty_list():
    assert whitespace_tokenize("   \t\n  ") == []


def test_char_tokenize_splits_every_character():
    assert char_tokenize("cat") == ["c", "a", "t"]


def test_char_tokenize_includes_whitespace_as_its_own_token():
    assert char_tokenize("a b") == ["a", " ", "b"]


def test_char_tokenize_includes_punctuation():
    assert char_tokenize("hi!") == ["h", "i", "!"]


def test_char_tokenize_empty_string_returns_empty_list():
    assert char_tokenize("") == []


def test_char_tokenize_length_matches_string_length():
    text = "hello world, this is a test."
    assert len(char_tokenize(text)) == len(text)


def test_whitespace_tokenize_does_not_split_words_into_characters():
    # Directly targets a mutant that accidentally calls char_tokenize's
    # logic (list(text)) instead of a real whitespace split, which would
    # silently pass a naive length check but produce completely wrong
    # tokens.
    result = whitespace_tokenize("cat dog")
    assert result == ["cat", "dog"]
    assert "c" not in result
