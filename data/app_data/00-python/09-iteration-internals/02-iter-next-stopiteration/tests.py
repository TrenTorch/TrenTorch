"""
pytest data/app_data/00-python/09-iteration-internals/02-iter-next-stopiteration/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/09-iteration-internals/{Path(__file__).resolve().parent.name}")
consume_iterator = _module.consume_iterator
take_first = _module.take_first
next_or_default = _module.next_or_default


def test_complete_manual_consumption():
    assert consume_iterator([1, 2, 3]) == [1, 2, 3]


def test_correct_exhaustion_handling():
    assert consume_iterator([]) == []


def test_partial_consumption():
    assert take_first([10, 20, 30], 2) == [10, 20]
    assert take_first([10], 5) == [10]
    assert take_first([1, 2, 3], 0) == []
    assert take_first([1, 2, 3], -1) == []


def test_already_exhausted_iterator():
    iterator = iter([1])
    next(iterator)
    assert next_or_default(iterator, "done") == "done"


def test_falsy_values_are_real_values():
    iterator = iter([None, 0, False, ""])
    assert next_or_default(iterator, "sentinel") is None
    assert next_or_default(iterator, "sentinel") == 0
    assert next_or_default(iterator, "sentinel") is False
    assert next_or_default(iterator, "sentinel") == ""
    assert next_or_default(iterator, "sentinel") == "sentinel"
