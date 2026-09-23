"""
pytest data/app_data/00-python/02-strings/01-indexing-slicing/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/02-strings/{Path(__file__).resolve().parent.name}")
first_and_last = _module.first_and_last
reverse_string = _module.reverse_string
every_kth_from = _module.every_kth_from


def test_first_and_last_normal_one_char_empty():
    assert first_and_last("python") == "pn"
    assert first_and_last("x") == "xx"
    assert first_and_last("") == ""


def test_reverse_string_palindrome_empty_single():
    assert reverse_string("racecar") == "racecar"
    assert reverse_string("") == ""
    assert reverse_string("x") == "x"
    assert reverse_string("python") == "nohtyp"


def test_every_kth_from_negative_start():
    assert every_kth_from("abcdefgh", -3, 2) == "fh"


def test_every_kth_from_positive_case():
    assert every_kth_from("abcdefgh", 1, 3) == "beh"


def test_every_kth_from_start_past_end():
    assert every_kth_from("abc", 100, 1) == ""


def test_inputs_not_mutated_and_new_object():
    s = "python"
    result = reverse_string(s)
    assert s == "python"
    assert id(result) != id(s)
