"""
pytest data/app_data/00-python/01-core-semantics/16-assemble-variable-mutation-trace/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
process_batch = _module.process_batch


def test_zero_values_skipped_via_continue():
    result = process_batch([1, 0, 2, 0, 3])
    assert result["seen"] == [1, 2, 3]


def test_negative_value_stops_processing_via_break():
    result = process_batch([1, 2, -1, 3, 4])
    assert result["seen"] == [1, 2]


def test_no_mutable_default_reused_across_calls():
    first = process_batch([1, 2])
    second = process_batch([3, 4])
    assert second["seen"] == [3, 4]
    assert 1 not in second["seen"]


def test_explicit_seen_list_is_mutated_in_place_not_replaced():
    existing = [99]
    before_id = id(existing)
    result = process_batch([1, 2], seen=existing)
    assert id(existing) == before_id
    assert existing == [99, 1, 2]
    assert result["seen"] == [99, 1, 2]


def test_alias_correctly_reflects_the_same_object():
    result = process_batch([1, 2, 3])
    assert result["seen_alias_is_same_object"] is True

    before_id = id(result["seen"])
    result["seen"].append(4)
    assert id(result["seen"]) == before_id
    assert result["seen"] == [1, 2, 3, 4]


def test_count_processed_matches_actual_processed_count():
    result = process_batch([1, 0, 2, -1, 3])
    assert result["count_processed"] == 2
    assert result["count_processed"] == len(result["seen"])
