"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
sentence_case = _module.sentence_case
swap_first_char_case = _module.swap_first_char_case
equal_ignoring_case = _module.equal_ignoring_case
case_kind = _module.case_kind
find_all = _module.find_all
count_overlapping = _module.count_overlapping
has_extension = _module.has_extension
classify_token = _module.classify_token
clean_field = _module.clean_field
remove_prefix_once = _module.remove_prefix_once
replace_first_n = _module.replace_first_n


def test_sentence_case_lowercases_the_tail():
    assert sentence_case("pyTHON") == "Python"
    assert sentence_case("hELLO wORLD") == "Hello world"


def test_swap_first_char_case_leaves_rest_untouched():
    assert swap_first_char_case("python") == "Python"
    assert swap_first_char_case("PYthon") == "pYthon"
    assert swap_first_char_case("") == ""


def test_equal_ignoring_case_handles_sharp_s():
    assert equal_ignoring_case("Straße", "STRASSE") is True
    assert equal_ignoring_case("Hello", "HELLO") is True
    assert equal_ignoring_case("Hello", "World") is False


def test_case_kind_classification():
    assert case_kind("ABC") == "upper"
    assert case_kind("abc") == "lower"
    assert case_kind("Hello World") == "title"
    assert case_kind("hELLo") == "mixed"
    assert case_kind("123") == "mixed"
    assert case_kind("") == "mixed"


def test_originals_unchanged():
    s = "pyTHON"
    sentence_case(s)
    swap_first_char_case(s)
    assert s == "pyTHON"


def test_overlapping_matches_found():
    assert find_all("aaaa", "aa") == [0, 1, 2]


def test_no_matches_and_empty_substring():
    assert find_all("hello", "xyz") == []
    assert find_all("hello", "") == []
    assert count_overlapping("hello", "") == 0
    assert count_overlapping("aaaa", "aa") == 3


def test_has_extension_needs_a_real_dot():
    assert has_extension("Report.PDF", "pdf") is True
    assert has_extension("pdf", "pdf") is False
    assert has_extension("apdf", "pdf") is False


def test_classify_token_ordering():
    assert classify_token("123") == "digits"
    assert classify_token("abc123") == "alnum"
    assert classify_token("  ") == "space"
    assert classify_token("a-b") == "other"
    assert classify_token("") == "other"
    assert classify_token("abc") == "letters"


def test_search_does_not_misuse_negative_one():
    # Last character of "hello" is "o" -- searching for an absent
    # substring must not accidentally resolve via -1 indexing.
    assert find_all("hello", "z") == []
    assert has_extension("file.o", "xyz") is False


def test_clean_field_step_order():
    assert clean_field("  a b.. ") == "a b"
    assert clean_field("  total ; ") == "total"


def test_remove_prefix_once_removes_exactly_one():
    assert remove_prefix_once("ababab", "ab") == "abab"


def test_prefix_absent_returns_unchanged():
    assert remove_prefix_once("hello", "xyz") == "hello"
    assert remove_prefix_once("ab", "abcdef") == "ab"


def test_replace_first_n_limits():
    assert replace_first_n("a-b-c-d", "-", "+", 0) == "a-b-c-d"
    assert replace_first_n("a-b-c-d", "-", "+", 1) == "a+b-c-d"
    assert replace_first_n("a-b-c-d", "-", "+", 100) == "a+b+c+d"
    assert replace_first_n("a-b-c-d", "-", "+", -1) == "a+b+c+d"


def test_original_unchanged():
    s = "  a b.. "
    clean_field(s)
    assert s == "  a b.. "
