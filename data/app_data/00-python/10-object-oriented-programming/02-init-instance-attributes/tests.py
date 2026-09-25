"""
pytest data/app_data/00-python/10-object-oriented-programming/02-init-instance-attributes/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
Rectangle = _module.Rectangle
Account = _module.Account
make_rectangle = _module.make_rectangle
attributes_of = _module.attributes_of


def test_rectangle_stores_its_arguments():
    r1 = Rectangle(3, 4)
    r2 = Rectangle(5, 6)
    assert r1.width == 3
    assert r1.height == 4
    assert r2.width == 5


def test_account_defaults_do_not_leak_between_instances():
    a1 = Account("x")
    a2 = Account("y")
    a1.history.append(100)
    assert a2.history == []


def test_account_copies_a_supplied_history():
    caller_history = [1, 2]
    account = Account("x", history=caller_history)
    caller_history.append(3)
    assert account.history == [1, 2]


def test_account_attribute_set():
    attrs = attributes_of(Account("x"))
    assert set(attrs.keys()) == {"owner", "balance", "history"}
    assert attrs == {"owner": "x", "balance": 0, "history": []}


def test_make_rectangle_returns_rectangle_instance():
    r = make_rectangle(2, 3)
    assert isinstance(r, Rectangle)
    assert r.width == 2
    assert r.height == 3
