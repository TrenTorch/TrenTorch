"""pytest tests.py"""

from _load import load_solution

assemble_stream = load_solution(__file__).assemble_stream


def test_1_single_chunk():
    assert assemble_stream(["Hello"]) == ["Hello"]


def test_2_multiple_chunks_cumulative():
    assert assemble_stream(["Hel", "lo, ", "world"]) == ["Hel", "Hello, ", "Hello, world"]


def test_3_empty_chunks_list():
    assert assemble_stream([]) == []


def test_4_empty_string_chunks_do_not_break_accumulation():
    assert assemble_stream(["a", "", "b"]) == ["a", "a", "ab"]


def test_5_many_single_char_chunks():
    result = assemble_stream(list("abcd"))
    assert result == ["a", "ab", "abc", "abcd"]
