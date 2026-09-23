"""
pytest data/app_data/00-python/01-core-semantics/07-reassignment-vs-mutation/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
mutate_list = _module.mutate_list
reassign_list = _module.reassign_list
observe_through_alias = _module.observe_through_alias


def test_mutate_list_preserves_address():
    caller_list = [1, 2, 3]
    before = id(caller_list)
    mutate_list(caller_list)
    assert id(caller_list) == before
    assert caller_list == [1, 2, 3, 4]


def test_reassign_list_does_not_touch_input():
    original = [1, 2, 3]
    result = reassign_list(original)
    assert original == [1, 2, 3]
    assert result == [9, 9, 9]
    assert id(result) != id(original)


def test_alias_sees_mutation_but_not_reassignment():
    result = observe_through_alias([1, 2, 3])
    assert result["alias_after_mutation"] == [1, 2, 3, 100]
    assert result["alias_after_reassignment"] == [1, 2, 3, 100]


def test_original_final_reflects_only_the_reassignment():
    result = observe_through_alias([1, 2, 3])
    assert result["original_final"] == [0, 0, 0]
