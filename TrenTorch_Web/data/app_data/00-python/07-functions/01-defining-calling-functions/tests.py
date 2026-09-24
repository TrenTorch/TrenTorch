"""
pytest data/app_data/00-python/07-functions/01-defining-calling-functions/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/07-functions/{Path(__file__).resolve().parent.name}")
square = _module.square
min_max = _module.min_max
describe_pair = _module.describe_pair
absolute_value = _module.absolute_value


def test_basic_return_values():
    assert square(5) == 25
    assert square(0) == 0
    assert square(-3) == 9


def test_multiple_return_values():
    result = min_max([4, 1, 7, 2])
    assert result == (1, 7)
    result2 = describe_pair(6, 2)
    assert result2 == (8, 4, 12)


def test_no_unintended_mutation():
    values = [4, 1, 7, 2]
    min_max(values)
    assert values == [4, 1, 7, 2]


def test_boundary_values():
    assert min_max([5]) == (5, 5)
    assert absolute_value(-7) == 7
    assert absolute_value(4) == 4
    assert absolute_value(0) == 0


def test_return_versus_printing(capsys):
    result = square(4)
    captured = capsys.readouterr()
    assert result == 16
    assert captured.out == ""
