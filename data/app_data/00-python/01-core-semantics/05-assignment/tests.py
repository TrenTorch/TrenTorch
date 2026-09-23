"""
pytest data/app_data/00-python/01-core-semantics/05-assignment/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
chain_assign = _module.chain_assign


def test_all_four_ids_identical():
    original = [1, 2, 3]
    result = chain_assign(original)
    assert result["a"] == result["b"] == result["c"] == result["original"]


def test_no_mutation_as_a_side_effect():
    original = [1, 2, 3]
    chain_assign(original)
    assert original == [1, 2, 3]


def test_works_for_non_list_objects_too():
    original = {"x": 1}
    result = chain_assign(original)
    assert result["a"] == result["b"] == result["c"] == result["original"]

    class Point:
        pass

    p = Point()
    result2 = chain_assign(p)
    assert result2["a"] == result2["b"] == result2["c"] == result2["original"]
