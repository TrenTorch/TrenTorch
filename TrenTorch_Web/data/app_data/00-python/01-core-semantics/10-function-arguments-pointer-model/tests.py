"""
pytest data/app_data/00-python/01-core-semantics/10-function-arguments-pointer-model/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
append_in_place = _module.append_in_place
attempt_reassign = _module.attempt_reassign
add_one = _module.add_one


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
