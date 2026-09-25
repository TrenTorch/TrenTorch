"""
pytest data/app_data/00-python/06-sets/03-set-operations/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
combine_sets = _module.combine_sets
common_values = _module.common_values
only_in_first = _module.only_in_first
in_exactly_one = _module.in_exactly_one
relationship = _module.relationship


def test_union():
    a, b = {1, 2}, {2, 3}
    assert combine_sets(a, b) == {1, 2, 3}
    assert a == {1, 2}
    assert b == {2, 3}


def test_intersection():
    assert common_values({1, 2, 3}, {2, 3, 4}) == {2, 3}
    assert common_values({1, 2}, {3, 4}) == set()
    assert common_values({1, 2}, {1, 2}) == {1, 2}


def test_directional_difference():
    a, b = {1, 2, 3}, {2, 4}
    assert only_in_first(a, b) == {1, 3}
    assert only_in_first(b, a) == {4}


def test_symmetric_difference():
    assert in_exactly_one({1, 2, 3}, {2, 3, 4}) == {1, 4}


def test_relationship_methods():
    assert relationship({1, 2}, {1, 2, 3}) == (True, False, False)
    assert relationship({1, 2, 3}, {1, 2}) == (False, True, False)
    assert relationship({1, 2}, {3, 4}) == (False, False, True)
    assert relationship(set(), set()) == (True, True, True)


def test_input_immutability():
    a, b = {1, 2, 3}, {2, 4}
    only_in_first(a, b)
    in_exactly_one(a, b)
    relationship(a, b)
    assert a == {1, 2, 3}
    assert b == {2, 4}
