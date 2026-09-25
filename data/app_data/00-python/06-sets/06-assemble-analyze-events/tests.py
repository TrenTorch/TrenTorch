"""
pytest data/app_data/00-python/06-sets/06-assemble-analyze-events/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/06-sets/{Path(__file__).resolve().parent.name}")
analyze_events = _module.analyze_events

BATCHES = [
    ["a", "b", "a", "c"],
    ["b", "c", "d"],
    ["b", "c", "e"],
]


def test_unique_ids_and_first_seen_order():
    result = analyze_events(BATCHES)
    assert result[0] == ["a", "b", "c", "d", "e"]


def test_ids_common_to_every_batch():
    result = analyze_events(BATCHES)
    assert result[1] == {"b", "c"}


def test_non_common_ids():
    result = analyze_events(BATCHES)
    assert result[2] == {"a", "d", "e"}


def test_empty_and_single_batch_inputs():
    assert analyze_events([]) == ([], set(), set(), 0)

    result = analyze_events([["x", "y", "x"]])
    assert result == (["x", "y"], {"x", "y"}, set(), 2)


def test_duplicate_heavy_batches():
    batches = [["a", "a", "a"], ["a", "a"]]
    result = analyze_events(batches)
    assert result[1] == {"a"}
    assert result[2] == set()


def test_set_and_list_structure():
    result = analyze_events(BATCHES)
    assert type(result[0]) is list
    assert type(result[1]) is set
    assert type(result[2]) is set
    assert result[3] == 5


def test_input_immutability():
    batches = [["a", "b"], ["b", "c"]]
    snapshot = [list(b) for b in batches]
    analyze_events(batches)
    assert batches == snapshot


def test_multiple_batch_sizes_including_empty_batch():
    batches = [["a", "b"], [], ["a"]]
    result = analyze_events(batches)
    assert result[0] == ["a", "b"]
    assert result[1] == set()
    assert result[3] == 2


def test_consistency_of_results():
    result = analyze_events(BATCHES)
    assert set(result[0]) == result[1] | result[2]
    assert len(result[0]) == result[3]
