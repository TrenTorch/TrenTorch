"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
add_item_fixed = _module.add_item_fixed
is_vulnerable_to_mutable_default = _module.is_vulnerable_to_mutable_default


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
