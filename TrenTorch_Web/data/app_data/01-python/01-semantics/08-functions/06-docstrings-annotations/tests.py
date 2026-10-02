"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
percentage = _module.percentage
repeat_text = _module.repeat_text
make_pair = _module.make_pair
function_metadata = _module.function_metadata


def test_docstring_presence():
    assert percentage.__doc__
    assert repeat_text.__doc__
    assert make_pair.__doc__


def test_annotation_metadata():
    assert percentage.__annotations__.get("value") is float
    assert percentage.__annotations__.get("return") is float
    assert repeat_text.__annotations__.get("count") is int


def test_behavior_independent_of_annotations():
    assert percentage(25, 200) == 12.5
    assert repeat_text("ab", 3) == "ababab"
    assert make_pair(1, "x") == (1, "x")


def test_function_metadata_from_function_object():
    result = function_metadata()
    assert result["doc"] == function_metadata.__doc__
    assert result["annotations"] == function_metadata.__annotations__
    assert set(result.keys()) == {"doc", "annotations"}


def test_exact_function_behavior():
    assert repeat_text("x", 0) == ""
    assert make_pair("a", "b") == ("a", "b")
