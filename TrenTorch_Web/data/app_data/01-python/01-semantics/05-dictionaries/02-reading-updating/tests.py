"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
word_frequencies = _module.word_frequencies
safe_lookup = _module.safe_lookup
increment = _module.increment
dict_from_two_lists = _module.dict_from_two_lists
merge_prefer_second = _module.merge_prefer_second
merge_counts = _module.merge_counts
group_by_first_letter = _module.group_by_first_letter
add_defaults = _module.add_defaults
remove_keys = _module.remove_keys
take_last = _module.take_last
remove_and_return = _module.remove_and_return
clear_and_report = _module.clear_and_report


def test_word_frequencies_counts_and_case():
    assert word_frequencies("a b a") == {"a": 2, "b": 1}
    assert word_frequencies("The the") == {"The": 1, "the": 1}
    assert word_frequencies("") == {}


def test_safe_lookup_does_not_insert():
    d = {"a": 1}
    result = safe_lookup(d, "z", 99)
    assert result == 99
    assert d == {"a": 1}


def test_safe_lookup_with_stored_none():
    d = {"a": None}
    assert safe_lookup(d, "a", 99) is None


def test_increment_mutates_in_place():
    d = {"a": 5}
    before_id = id(d)
    increment(d, "a", 3)
    assert d["a"] == 8
    assert id(d) == before_id
    increment(d, "b", -2)
    assert d["b"] == -2


def test_dict_from_two_lists_repeated_keys_and_empty():
    assert dict_from_two_lists(["a", "a"], [1, 2]) == {"a": 2}
    assert dict_from_two_lists([], []) == {}
    assert dict_from_two_lists(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def test_merge_prefer_second_precedence_and_purity():
    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 3}
    result = merge_prefer_second(a, b)
    assert result == {"x": 1, "y": 20, "z": 3}
    assert a == {"x": 1, "y": 2}
    assert b == {"y": 20, "z": 3}
    assert id(result) != id(a)
    assert id(result) != id(b)


def test_merge_counts_sums_correctly():
    a = {"x": 1, "y": 2}
    b = {"y": 3, "z": 4}
    result = merge_counts(a, b)
    assert result == {"x": 1, "y": 5, "z": 4}
    assert a == {"x": 1, "y": 2}
    assert b == {"y": 3, "z": 4}


def test_group_by_first_letter_grouping_and_order():
    result = group_by_first_letter(["Apple", "avocado", "Bean", ""])
    assert result == {"a": ["Apple", "avocado"], "b": ["Bean"]}


def test_group_by_first_letter_independent_lists():
    result = group_by_first_letter(["Apple", "Bean"])
    result["a"].append("extra")
    assert result["b"] == ["Bean"]


def test_add_defaults_never_overwrites():
    config = {"lr": 0.1, "verbose": None, "epochs": 0}
    add_defaults(config, {"lr": 0.001, "verbose": True, "epochs": 5, "batch_size": 32})
    assert config == {"lr": 0.1, "verbose": None, "epochs": 0, "batch_size": 32}


def test_remove_keys_returns_exact_count():
    d = {"a": 1, "b": 2}
    result = remove_keys(d, ["a", "z", "a"])
    assert result == 1
    assert d == {"b": 2}


def test_remove_keys_mutates_in_place():
    d = {"a": 1, "b": 2}
    before_id = id(d)
    remove_keys(d, ["a"])
    assert id(d) == before_id


def test_take_last_respects_insertion_order():
    d = {"a": 1, "b": 2}
    assert take_last(d) == ("b", 2)
    d["a_again"] = 3
    d.pop("a")
    d["a"] = 4
    assert take_last(d) == ("a", 4)


def test_take_last_on_empty_dictionary():
    assert take_last({}) is None


def test_remove_and_return_with_stored_none_and_absent():
    d = {"a": None}
    assert remove_and_return(d, "a", "missing") is None
    assert "a" not in d
    d2 = {"a": 1}
    assert remove_and_return(d2, "z", "missing") == "missing"
    assert d2 == {"a": 1}


def test_clear_and_report_counts_before_clearing():
    d = {"a": 1, "b": 2}
    before_id = id(d)
    count = clear_and_report(d)
    assert count == 2
    assert d == {}
    assert id(d) == before_id
