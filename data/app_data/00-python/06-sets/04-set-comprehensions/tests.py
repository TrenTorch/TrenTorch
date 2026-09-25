"""
pytest data/app_data/00-python/06-sets/04-set-comprehensions/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
squared_unique = _module.squared_unique
positive_unique = _module.positive_unique
word_lengths = _module.word_lengths
coordinate_sums = _module.coordinate_sums


def test_transformation():
    assert squared_unique([1, 2, 3]) == {1, 4, 9}


def test_duplicate_collapse():
    assert squared_unique([-2, -1, 1, 2]) == {1, 4}


def test_filtering_boundary():
    assert positive_unique([-2, 3, 3, 0, 5, -1]) == {3, 5}
    assert 0 not in positive_unique([-1, 0, 1])


def test_empty_input():
    assert squared_unique([]) == set()
    assert positive_unique([]) == set()
    assert word_lengths([]) == set()
    assert coordinate_sums([]) == set()


def test_input_preservation():
    values = [-2, -1, 1, 2]
    squared_unique(values)
    positive_unique(values)
    assert values == [-2, -1, 1, 2]

    words = ["cat", "dog", "house"]
    assert word_lengths(words) == {3, 5}
    assert words == ["cat", "dog", "house"]

    points = [(1, 2), (3, 4), (0, 3)]
    assert coordinate_sums(points) == {3, 7}
    assert points == [(1, 2), (3, 4), (0, 3)]
