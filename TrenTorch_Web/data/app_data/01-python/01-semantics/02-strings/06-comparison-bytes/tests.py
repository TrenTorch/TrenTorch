"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
compare_strings = _module.compare_strings
compare_ignoring_case = _module.compare_ignoring_case
caesar_shift = _module.caesar_shift
utf8_byte_length = _module.utf8_byte_length
roundtrip = _module.roundtrip
is_ascii_only = _module.is_ascii_only
first_byte_values = _module.first_byte_values


def test_decision_at_first_differing_character():
    assert compare_strings("apple", "banana") == -1
    assert compare_strings("b", "a") == 1


def test_prefix_ordering_and_equality():
    assert compare_strings("app", "apple") == -1
    assert compare_strings("apple", "app") == 1
    assert compare_strings("apple", "apple") == 0


def test_uppercase_before_lowercase():
    assert compare_strings("Zebra", "apple") == -1


def test_digits_compare_as_text():
    assert compare_strings("10", "9") == -1


def test_compare_ignoring_case():
    assert compare_ignoring_case("Zebra", "apple") == 1
    assert compare_ignoring_case("APPLE", "apple") == 0


def test_caesar_shift_wrap_case_and_non_letters():
    assert caesar_shift("Abc, xyz!", 3) == "Def, abc!"
    assert caesar_shift("Hello", 0) == "Hello"
    assert caesar_shift("Hello", 26) == "Hello"
    assert caesar_shift("Def, abc!", -3) == "Abc, xyz!"


def test_byte_length_for_various_widths():
    assert utf8_byte_length("a") == 1
    assert utf8_byte_length("é") == 2
    assert utf8_byte_length("日") == 3
    assert utf8_byte_length("😀") == 4


def test_round_trip_preserves_text():
    assert roundtrip("naïve café 日本語", "utf-8") == "naïve café 日本語"


def test_lossy_encoding_does_not_raise():
    result = roundtrip("café", "ascii")
    assert "?" in result
    assert result.startswith("caf")


def test_is_ascii_only_empty_ascii_non_ascii():
    assert is_ascii_only("") is True
    assert is_ascii_only("hello") is True
    assert is_ascii_only("é") is False


def test_first_byte_values_returns_ints_and_respects_length():
    values = first_byte_values("Aé", 3)
    assert values == [65, 195, 169]
    assert all(isinstance(v, int) for v in values)
    assert first_byte_values("A", 10) == [65]
