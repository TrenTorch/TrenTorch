"""
pytest data/app_data/00-python/05-dictionaries/05-update-setdefault/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/05-dictionaries/{Path(__file__).resolve().parent.name}")
merge_prefer_second = _module.merge_prefer_second
merge_counts = _module.merge_counts
group_by_first_letter = _module.group_by_first_letter
add_defaults = _module.add_defaults


def test_merge_prefer_second_precedence_and_purity():
    a = {"x": 1, "y": 2}
    b = {"y": 20, "z": 3}
    result = merge_prefer_second(a, b)
    assert result == {"x": 1, "y": 20, "z": 3}
    assert a == {"x": 1, "y": 2}
    assert b == {"y": 20, "z": 3}
    assert id(result) != id(a)
    assert id(result) != id(b)


def test_merge_counts_sums_correctly():
    a = {"x": 1, "y": 2}
    b = {"y": 3, "z": 4}
    result = merge_counts(a, b)
    assert result == {"x": 1, "y": 5, "z": 4}
    assert a == {"x": 1, "y": 2}
    assert b == {"y": 3, "z": 4}


def test_group_by_first_letter_grouping_and_order():
    result = group_by_first_letter(["Apple", "avocado", "Bean", ""])
    assert result == {"a": ["Apple", "avocado"], "b": ["Bean"]}


def test_group_by_first_letter_independent_lists():
    result = group_by_first_letter(["Apple", "Bean"])
    result["a"].append("extra")
    assert result["b"] == ["Bean"]


def test_add_defaults_never_overwrites():
    config = {"lr": 0.1, "verbose": None, "epochs": 0}
    add_defaults(config, {"lr": 0.001, "verbose": True, "epochs": 5, "batch_size": 32})
    assert config == {"lr": 0.1, "verbose": None, "epochs": 0, "batch_size": 32}
