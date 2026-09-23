"""
pytest data/app_data/00-python/04-tuples/01-tuple-objects-immutable/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/04-tuples/{Path(__file__).resolve().parent.name}")
make_singleton = _module.make_singleton
tuple_replace = _module.tuple_replace
count_and_first_index = _module.count_and_first_index


def test_make_singleton_produces_a_tuple():
    result = make_singleton(5)
    assert type(result) is tuple
    assert len(result) == 1
    assert result == (5,)
    result2 = make_singleton([1, 2])
    assert type(result2) is tuple
    assert len(result2) == 1


def test_tuple_replace_positions():
    assert tuple_replace((1, 2, 3), 0, 9) == (9, 2, 3)
    assert tuple_replace((1, 2, 3), 1, 9) == (1, 9, 3)
    assert tuple_replace((1, 2, 3), 2, 9) == (1, 2, 9)
    assert tuple_replace((1, 2, 3), -1, 9) == (1, 2, 9)


def test_tuple_replace_out_of_range_and_empty():
    assert tuple_replace((1, 2, 3), 3, 9) == (1, 2, 3)
    assert tuple_replace((1, 2, 3), -4, 9) == (1, 2, 3)
    assert tuple_replace((), 0, 9) == ()


def test_input_untouched_and_result_is_new():
    t = (1, 2, 3)
    before_id = id(t)
    result = tuple_replace(t, 0, 9)
    assert t == (1, 2, 3)
    assert id(t) == before_id
    assert id(result) != before_id


def test_count_and_first_index_absent_and_repeated():
    assert count_and_first_index((5, 3, 5), 5) == (2, 0)
    assert count_and_first_index((5, 3, 5), 9) == (0, -1)
