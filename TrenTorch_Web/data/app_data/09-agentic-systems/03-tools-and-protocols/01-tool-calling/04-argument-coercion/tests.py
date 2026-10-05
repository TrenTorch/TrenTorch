"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
coerce_arguments = _module.coerce_arguments
SCHEMA = {
    "n": {"type": "integer", "default": 10},
    "x": {"type": "number"},
    "flag": {"type": "boolean", "default": False},
    "name": {"type": "string"},
}


def test_1_string_numbers_are_coerced():
    assert coerce_arguments({"n": "3", "x": "2.5"}, SCHEMA) == {"n": 3, "x": 2.5, "flag": False}


def test_2_boolean_words():
    assert coerce_arguments({"flag": "Yes"}, SCHEMA)["flag"] is True
    assert coerce_arguments({"flag": "no"}, SCHEMA)["flag"] is False


def test_3_unparseable_values_are_left_for_validation():
    out = coerce_arguments({"n": "three", "flag": "maybe"}, SCHEMA)
    assert out["n"] == "three" and out["flag"] == "maybe"


def test_4_defaults_fill_only_missing_arguments():
    assert coerce_arguments({}, SCHEMA) == {"n": 10, "flag": False}
    assert coerce_arguments({"n": 1}, SCHEMA)["n"] == 1


def test_5_integral_floats_become_ints_but_fractions_do_not():
    assert coerce_arguments({"n": 3.0}, SCHEMA)["n"] == 3 and isinstance(coerce_arguments({"n": 3.0}, SCHEMA)["n"], int)
    assert coerce_arguments({"n": 3.5}, SCHEMA)["n"] == 3.5


def test_6_bool_is_not_turned_into_an_integer_and_strings_pass_through():
    assert coerce_arguments({"n": True}, SCHEMA)["n"] is True
    assert coerce_arguments({"name": "42"}, SCHEMA)["name"] == "42"


def test_7_unknown_arguments_are_kept_and_input_untouched():
    args = {"n": "5", "extra": "1"}
    snap = dict(args)
    out = coerce_arguments(args, SCHEMA)
    assert out["extra"] == "1" and args == snap
