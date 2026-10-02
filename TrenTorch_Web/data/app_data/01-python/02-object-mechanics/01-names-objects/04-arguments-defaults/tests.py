"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
append_in_place = _module.append_in_place
attempt_reassign = _module.attempt_reassign
add_one = _module.add_one
add_item_fixed = _module.add_item_fixed
is_vulnerable_to_mutable_default = _module.is_vulnerable_to_mutable_default


def test_append_in_place_visible_to_caller():
    caller_list = [1, 2, 3]
    before_id = id(caller_list)
    append_in_place(caller_list, 4)
    assert caller_list == [1, 2, 3, 4]
    assert id(caller_list) == before_id


def test_attempt_reassign_invisible_to_caller():
    caller_list = [1, 2, 3]
    before_id = id(caller_list)
    attempt_reassign(caller_list)
    assert caller_list == [1, 2, 3]
    assert id(caller_list) == before_id


def test_add_one_does_not_mutate_input():
    x = 5
    result = add_one(x)
    assert result == 6
    assert x == 5


def test_combined_trace():
    caller_list = [1, 2, 3]
    append_in_place(caller_list, 4)
    attempt_reassign(caller_list)
    assert caller_list == [1, 2, 3, 4]


def test_repeated_calls_without_bucket_stay_independent():
    first = add_item_fixed("a")
    second = add_item_fixed("b")
    assert first == ["a"]
    assert second == ["b"]


def test_explicit_bucket_is_still_mutated_correctly():
    my_bucket = ["existing"]
    result = add_item_fixed("new", my_bucket)
    assert result is my_bucket
    assert my_bucket == ["existing", "new"]


def test_vulnerability_detector_catches_mutable_defaults():
    def vulnerable_list(item, bucket=[]):
        pass

    def vulnerable_dict(item, cache={}):
        pass

    def vulnerable_set(item, seen=set()):
        pass

    assert is_vulnerable_to_mutable_default(vulnerable_list) is True
    assert is_vulnerable_to_mutable_default(vulnerable_dict) is True
    assert is_vulnerable_to_mutable_default(vulnerable_set) is True


def test_vulnerability_detector_passes_clean_functions():
    def clean_with_none(item, bucket=None):
        pass

    def clean_with_no_default(item, bucket):
        pass

    assert is_vulnerable_to_mutable_default(clean_with_none) is False
    assert is_vulnerable_to_mutable_default(clean_with_no_default) is False
