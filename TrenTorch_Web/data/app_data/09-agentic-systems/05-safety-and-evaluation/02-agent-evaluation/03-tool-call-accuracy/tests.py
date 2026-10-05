"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import math

tool_call_metrics = _module.tool_call_metrics


def test_1_perfect_match_regardless_of_key_order():
    pred = [("search", {"q": "x", "n": 1})]
    exp = [("search", {"n": 1, "q": "x"})]
    assert tool_call_metrics(pred, exp) == {"precision": 1.0, "recall": 1.0, "f1": 1.0, "name_f1": 1.0}


def test_2_wrong_arguments_hurt_exact_but_not_name_scores():
    m = tool_call_metrics([("search", {"q": "y"})], [("search", {"q": "x"})])
    assert m["f1"] == 0.0 and m["name_f1"] == 1.0


def test_3_extra_call_lowers_precision_only():
    m = tool_call_metrics([("a", {}), ("b", {})], [("a", {})])
    assert m["precision"] == 0.5 and m["recall"] == 1.0 and math.isclose(m["f1"], 2 / 3)


def test_4_missing_call_lowers_recall_only():
    m = tool_call_metrics([("a", {})], [("a", {}), ("b", {})])
    assert m["precision"] == 1.0 and m["recall"] == 0.5


def test_5_repeated_calls_are_matched_as_a_multiset():
    m = tool_call_metrics([("a", {}), ("a", {})], [("a", {})])
    assert m["precision"] == 0.5 and m["recall"] == 1.0


def test_6_empty_cases():
    assert tool_call_metrics([], []) == {"precision": 1.0, "recall": 1.0, "f1": 1.0, "name_f1": 1.0}
    m = tool_call_metrics([], [("a", {})])
    assert m["precision"] == 0.0 and m["recall"] == 0.0 and m["f1"] == 0.0


def test_7_nested_arguments_and_inputs_untouched():
    pred = [("f", {"opts": {"b": [1, 2], "a": 1}})]
    exp = [("f", {"opts": {"a": 1, "b": [1, 2]}})]
    snap = [("f", {"opts": {"b": [1, 2], "a": 1}})]
    assert tool_call_metrics(pred, exp)["f1"] == 1.0 and pred == snap
