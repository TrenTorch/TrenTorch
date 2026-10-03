"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

repair_json = _module.repair_json


def test_1_valid_json_passes_through():
    assert repair_json('{"a": [1, 2]}') == {"a": [1, 2]}


def test_2_code_fence_and_prose_are_stripped():
    text = 'Here you go:\n```json\n{"a": 1}\n```\nHope that helps!'
    assert repair_json(text) == {"a": 1}


def test_3_trailing_commas_are_removed():
    assert repair_json('{"a": [1, 2,], "b": 3,}') == {"a": [1, 2], "b": 3}


def test_4_python_literals_are_converted():
    assert repair_json('{"ok": True, "bad": False, "none": None}') == {"ok": True, "bad": False, "none": None}


def test_5_strings_are_never_altered():
    text = '{"msg": "True, None, [1,]}", "n": 1,}'
    assert repair_json(text) == {"msg": "True, None, [1,]}", "n": 1}


def test_6_arrays_are_supported():
    assert repair_json("Result: [1, 2, 3,] done") == [1, 2, 3]


def test_7_unrepairable_text_raises():
    for bad in ["no json at all", '{"a": }', "{'a': 1}", '{"a": 1']:
        with pytest.raises(ValueError):
            repair_json(bad)
