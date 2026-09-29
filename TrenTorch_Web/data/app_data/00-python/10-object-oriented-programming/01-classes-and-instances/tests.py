"""
pytest data/app_data/00-python/10-object-oriented-programming/01-classes-and-instances/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
build_instances = _module.build_instances
attach_point = _module.attach_point
same_class = _module.same_class
attribute_snapshot = _module.attribute_snapshot


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
