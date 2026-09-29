"""
pytest data/app_data/00-python/10-object-oriented-programming/04-class-vs-instance-attributes/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
Tracker = _module.Tracker
where_is_attribute = _module.where_is_attribute
shadow_count = _module.shadow_count


def test_tracker_count_increases_per_instance():
    Tracker.count = 0
    Tracker("a")
    Tracker("b")
    Tracker("c")
    assert Tracker.count == 3


def test_tracker_instances_keep_separate_labels():
    a = Tracker("a")
    b = Tracker("b")
    assert a.label != b.label
    assert "label" not in Tracker.__dict__


def test_where_is_attribute_distinguishes_all_three():
    Tracker.count = 0
    a = Tracker("a")
    assert where_is_attribute(a, "label") == "instance"
    assert where_is_attribute(a, "count") == "class"
    assert where_is_attribute(a, "nonexistent") == "missing"


def test_shadow_count_creates_instance_attribute_only():
    Tracker.count = 5
    a = Tracker("a")
    b = Tracker("b")
    shadow_count(a, 99)
    assert a.count == 99
    assert Tracker.count == 7
    assert b.count == 7


def test_where_is_attribute_after_shadowing():
    Tracker.count = 0
    a = Tracker("a")
    b = Tracker("b")
    shadow_count(a, 42)
    assert where_is_attribute(a, "count") == "instance"
    assert where_is_attribute(b, "count") == "class"
