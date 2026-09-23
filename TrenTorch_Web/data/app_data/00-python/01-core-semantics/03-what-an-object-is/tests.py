"""
pytest data/app_data/00-python/01-core-semantics/03-what-an-object-is/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/01-core-semantics/{Path(__file__).resolve().parent.name}")
describe_object = _module.describe_object


def test_type_correctness_across_categories():
    assert describe_object(1)["type"] == "int"
    assert describe_object(1.5)["type"] == "float"
    assert describe_object("hi")["type"] == "str"
    assert describe_object([1, 2])["type"] == "list"
    assert describe_object({"a": 1})["type"] == "dict"
    assert describe_object({1, 2})["type"] == "set"
    assert describe_object((1, 2))["type"] == "tuple"
    assert describe_object(True)["type"] == "bool"


def test_address_matches_id_directly():
    value = [1, 2, 3]
    assert describe_object(value)["address"] == id(value)


def test_different_objects_report_different_addresses():
    a = [1, 2, 3]
    b = [1, 2, 3]
    assert a == b
    assert describe_object(a)["address"] != describe_object(b)["address"]
