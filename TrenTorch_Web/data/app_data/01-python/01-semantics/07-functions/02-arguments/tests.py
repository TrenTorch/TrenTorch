"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
build_point = _module.build_point
configure_model = _module.configure_model
format_record = _module.format_record
power = _module.power
make_label = _module.make_label
append_value = _module.append_value
describe_config = _module.describe_config
sum_all = _module.sum_all
collect_types = _module.collect_types
build_options = _module.build_options
summarize = _module.summarize
call_with_options = _module.call_with_options


def test_all_positional_calls():
    assert build_point(3, 4) == (3, 4)
    assert configure_model("db", 128, "cosine") == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_all_keyword_calls():
    assert build_point(x=3, y=4) == (3, 4)
    assert format_record(identifier=7, value=3.5, label="score") == "7=3.5 [score]"


def test_mixed_calls():
    assert configure_model("db", dimensions=128, metric="cosine") == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_keyword_order_does_not_matter():
    assert build_point(y=4, x=3) == (3, 4)
    assert configure_model(metric="cosine", name="db", dimensions=128) == {
        "name": "db",
        "dimensions": 128,
        "metric": "cosine",
    }


def test_returned_structure():
    assert format_record(7, 3.5, "score") == "7=3.5 [score]"
    result = configure_model("db", 128, "cosine")
    assert type(result) is dict


def test_default_usage():
    assert power(5) == 25
    assert make_label(7) == "item:7"
    assert describe_config("server") == ("server", True, 3)


def test_explicit_override():
    assert power(2, 3) == 8
    assert make_label(7, "id") == "id:7"
    assert describe_config("server", False, 5) == ("server", False, 5)


def test_default_binding_not_affected_by_external_reassignment():
    x = 10

    def show(value=x):
        return value

    x = 20
    assert show() == 10


def test_fresh_mutable_default_behavior():
    result1 = append_value(1)
    result2 = append_value(2)
    assert result1 == [1]
    assert result2 == [2]


def test_supplied_mutable_object_is_mutated_and_returned():
    xs = [10]
    result = append_value(20, xs)
    assert xs == [10, 20]
    assert result is xs


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
