"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
sum_all = _module.sum_all
collect_types = _module.collect_types
build_options = _module.build_options
summarize = _module.summarize
call_with_options = _module.call_with_options


def test_empty_args():
    assert sum_all() == 0
    assert collect_types() == ()


def test_many_positional_arguments():
    assert sum_all(1, 2, 3, 4) == 10
    assert collect_types(1, "x", 2.5) == (int, str, float)


def test_empty_kwargs():
    assert build_options() == {}


def test_keyword_collection():
    assert build_options(debug=True, retries=3) == {"debug": True, "retries": 3}


def test_combined_arguments():
    result = summarize("x", 1, 2, debug=True)
    assert result == {"required": "x", "values": (1, 2), "options": {"debug": True}}


def test_argument_unpacking():
    assert call_with_options(pow, (2, 3), {}) == 8

    def greet(name, greeting="Hi"):
        return f"{greeting}, {name}"

    assert call_with_options(greet, ("Sam",), {"greeting": "Hello"}) == "Hello, Sam"


def test_input_preservation():
    args = (2, 3)
    options = {}
    call_with_options(pow, args, options)
    assert args == (2, 3)
    assert options == {}
