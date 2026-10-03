"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
build_instances = _module.build_instances
attach_point = _module.attach_point
same_class = _module.same_class
attribute_snapshot = _module.attribute_snapshot
Rectangle = _module.Rectangle
Account = _module.Account
make_rectangle = _module.make_rectangle
attributes_of = _module.attributes_of


class Point:
    pass


class OtherPoint:
    pass


class DerivedPoint(Point):
    pass


def test_build_instances_creates_distinct_objects():
    instances = build_instances(Point, 3)
    assert len(instances) == 3
    assert all(isinstance(i, Point) for i in instances)
    ids = [id(i) for i in instances]
    assert len(ids) == len(set(ids))


def test_build_instances_zero_and_negative():
    assert build_instances(Point, 0) == []
    assert build_instances(Point, -5) == []


def test_attach_point_isolation():
    a, b = Point(), Point()
    attach_point(a, 1, 2)
    assert not hasattr(b, "x")


def test_same_class_exactness():
    a, b = Point(), Point()
    c = OtherPoint()
    d = DerivedPoint()
    assert same_class(a, b) is True
    assert same_class(a, c) is False
    assert same_class(a, d) is False


def test_attribute_snapshot_independence():
    p = Point()
    attach_point(p, 3, 4)
    snapshot = attribute_snapshot(p)
    snapshot["x"] = 999
    assert p.x == 3


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
