"""
pytest tests.py
"""

import io
from contextlib import redirect_stdout
from _load import load_solution

_module = load_solution(__file__)
square = _module.square
min_max = _module.min_max
describe_pair = _module.describe_pair
absolute_value = _module.absolute_value
percentage = _module.percentage
repeat_text = _module.repeat_text
make_pair = _module.make_pair
function_metadata = _module.function_metadata


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


def test_return_versus_printing():
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = square(4)
    assert result == 16
    assert buffer.getvalue() == ""


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
