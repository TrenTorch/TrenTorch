"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
validate_arguments = _module.validate_arguments
SCHEMA = {
    "properties": {
        "city": {"type": "string"},
        "days": {"type": "integer", "minimum": 1, "maximum": 14},
        "unit": {"type": "string", "enum": ["c", "f"]},
        "verbose": {"type": "boolean"},
        "tags": {"type": "array"},
        "score": {"type": "number"},
    },
    "required": ["city"],
}


def test_1_valid_call():
    assert validate_arguments({"city": "Pune", "days": 3, "unit": "c"}, SCHEMA) == []


def test_2_missing_and_unexpected():
    assert validate_arguments({"zip": "x"}, SCHEMA) == ["missing: city", "unexpected: zip"]


def test_3_wrong_types():
    assert validate_arguments({"city": 5, "days": "3", "verbose": "yes", "tags": "a"}, SCHEMA) == [
        "type: city", "type: days", "type: tags", "type: verbose",
    ]


def test_4_bool_is_not_an_integer_or_number():
    assert validate_arguments({"city": "x", "days": True, "score": False}, SCHEMA) == ["type: days", "type: score"]


def test_5_enum_and_range():
    assert validate_arguments({"city": "x", "unit": "k", "days": 99}, SCHEMA) == ["enum: unit", "range: days"]
    assert validate_arguments({"city": "x", "days": 0}, SCHEMA) == ["range: days"]


def test_6_number_accepts_int_and_float():
    assert validate_arguments({"city": "x", "score": 3}, SCHEMA) == [] and validate_arguments({"city": "x", "score": 2.5}, SCHEMA) == []


def test_7_one_error_per_argument_and_input_untouched():
    args = {"city": "x", "unit": 5}
    snap = dict(args)
    assert validate_arguments(args, SCHEMA) == ["type: unit"] and args == snap
