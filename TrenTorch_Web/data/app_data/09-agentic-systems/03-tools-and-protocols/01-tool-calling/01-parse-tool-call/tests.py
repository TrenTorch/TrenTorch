"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
import pytest

parse_tool_call = _module.parse_tool_call


def test_1_plain_json():
    assert parse_tool_call('{"name": "search", "arguments": {"q": "cats"}}') == ("search", {"q": "cats"})


def test_2_prose_and_code_fence_around_the_call():
    text = 'Sure, I will look that up:\n```json\n{"name": "search", "arguments": {"q": "x"}}\n```\nDone.'
    assert parse_tool_call(text) == ("search", {"q": "x"})


def test_3_arguments_given_as_a_json_string():
    assert parse_tool_call('{"name": "add", "arguments": "{\\"a\\": 1, \\"b\\": 2}"}') == ("add", {"a": 1, "b": 2})


def test_4_decoy_json_before_the_real_call_is_skipped():
    text = 'Example: {"x": 1} but actually {"name": "go", "arguments": {}}'
    assert parse_tool_call(text) == ("go", {})


def test_5_nested_braces_inside_arguments():
    text = 'Call: {"name": "f", "arguments": {"obj": {"k": [1, {"z": 2}]}}} thanks'
    assert parse_tool_call(text) == ("f", {"obj": {"k": [1, {"z": 2}]}})


def test_6_no_call_raises():
    for bad in ["no json here", '{"name": "x"}', '{"foo": 1}', "{ broken"]:
        with pytest.raises(ValueError):
            parse_tool_call(bad)


def test_7_invalid_arguments_string_raises():
    with pytest.raises(ValueError):
        parse_tool_call('{"name": "f", "arguments": "not json"}')
    with pytest.raises(ValueError):
        parse_tool_call('{"name": "f", "arguments": [1, 2]}')
