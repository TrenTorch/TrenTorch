"""
pytest data/app_data/00-python/04-tuples/02-packing-unpacking/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/04-tuples/{Path(__file__).resolve().parent.name}")
rotate_three = _module.rotate_three
head_and_tail = _module.head_and_tail
ends_and_middle = _module.ends_and_middle
sum_pairs = _module.sum_pairs


def test_rotate_three_order_and_type():
    result = rotate_three(1, 2, 3)
    assert type(result) is tuple
    assert result == (2, 3, 1)
    assert rotate_three(5, 5, 5) == (5, 5, 5)


def test_head_and_tail_on_tuple_list_string():
    assert head_and_tail((1, 2, 3)) == (1, [2, 3])
    assert head_and_tail([1, 2, 3]) == (1, [2, 3])
    assert head_and_tail("abc") == ("a", ["b", "c"])
    assert head_and_tail([1]) == (1, [])


def test_head_and_tail_on_empty_input():
    assert head_and_tail([]) == (None, [])
    assert head_and_tail(()) == (None, [])


def test_ends_and_middle_with_various_lengths():
    assert ends_and_middle([1, 2]) == (1, [], 2)
    assert ends_and_middle([1, 2, 3]) == (1, [2], 3)
    assert ends_and_middle([1, 2, 3, 4]) == (1, [2, 3], 4)
    assert ends_and_middle("ab") == ("a", [], "b")


def test_sum_pairs_empty_and_mixed_numbers():
    assert sum_pairs([]) == []
    assert sum_pairs([(1, 2), (3, 4)]) == [3, 7]
    assert sum_pairs([(-1, 1), (1.5, 2.5)]) == [0, 4.0]
