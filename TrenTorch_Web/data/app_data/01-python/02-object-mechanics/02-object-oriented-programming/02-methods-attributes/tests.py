"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
Accumulator = _module.Accumulator
add_via_class = _module.add_via_class
bound_method_target = _module.bound_method_target
chain_adds = _module.chain_adds
Tracker = _module.Tracker
where_is_attribute = _module.where_is_attribute
shadow_count = _module.shadow_count


def test_add_returns_same_instance_and_chains():
    a = Accumulator()
    result = a.add(1)
    assert result is a
    assert a.add(1).add(2).value() == 4


def test_instances_keep_separate_totals():
    a = Accumulator()
    b = Accumulator()
    a.add(10)
    assert b.value() == 0


def test_add_via_class_equals_ordinary_call():
    a = Accumulator()
    add_via_class(a, 5)
    assert a.value() == 5


def test_bound_method_target_returns_instance():
    a = Accumulator()
    assert bound_method_target(a.add) is a


def test_chain_adds_and_empty_input():
    a = Accumulator()
    result = chain_adds(a, [1, 2, 3])
    assert result is a
    assert a.value() == 6

    b = Accumulator()
    chain_adds(b, [])
    assert b.value() == 0


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
