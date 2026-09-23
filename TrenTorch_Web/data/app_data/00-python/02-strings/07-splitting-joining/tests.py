"""
pytest data/app_data/00-python/02-strings/07-splitting-joining/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
word_count = _module.word_count
reverse_word_order = _module.reverse_word_order
last_field = _module.last_field
count_nonblank_lines = _module.count_nonblank_lines
make_csv_line = _module.make_csv_line


def test_whitespace_splitting_tolerance():
    assert word_count("a\tb\nc") == 3
    assert word_count("  a   b  ") == 2


def test_word_count_empty_and_whitespace_only():
    assert word_count("") == 0
    assert word_count("   \t\n  ") == 0


def test_reverse_word_order():
    assert reverse_word_order("  one  two three ") == "three two one"


def test_last_field_adjacent_separators_and_absent():
    assert last_field("a//b", "/") == "b"
    assert last_field("a/b/c.txt", "/") == "c.txt"
    assert last_field("noseparator", "/") == "noseparator"


def test_count_nonblank_lines_trailing_newline_and_blanks():
    assert count_nonblank_lines("a\nb\n") == 2
    assert count_nonblank_lines("a\n\n   \nb") == 2


def test_make_csv_line_quoting():
    assert make_csv_line(["a", "b,c", "d"]) == 'a,"b,c",d'
    assert make_csv_line([]) == ""
    assert make_csv_line(["a", "b"]) == "a,b"
