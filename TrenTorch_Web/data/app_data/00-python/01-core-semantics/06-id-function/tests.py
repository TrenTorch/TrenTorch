"""
pytest data/app_data/00-python/01-core-semantics/06-id-function/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
did_mutate_in_place = _module.did_mutate_in_place
are_same_object = _module.are_same_object


def test_in_place_methods_detected_correctly():
    assert did_mutate_in_place([1, 2], lambda l: l.append(99)) is True
    assert did_mutate_in_place([1, 2], lambda l: l.extend([3, 4])) is True
    assert did_mutate_in_place([3, 1, 2], lambda l: l.sort()) is True


def test_reassignment_style_operation_detected_correctly():
    assert did_mutate_in_place([1, 2], lambda l: l + [99]) is False


def test_are_same_object_diverges_from_equals():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert a == b
    assert are_same_object(a, b) is False


def test_are_same_object_on_identical_reference():
    a = [1, 2, 3]
    assert are_same_object(a, a) is True
