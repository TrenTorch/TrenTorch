"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
Shape = _module.Shape
Circle = _module.Circle
Rectangle = _module.Rectangle
Square = _module.Square
total_area = _module.total_area
total_length = _module.total_length
Countdown = _module.Countdown
describe_capabilities = _module.describe_capabilities
first_or_none = _module.first_or_none
add_all = _module.add_all


def test_overridden_area_is_used():
    assert Circle(1).area() == 3.14159
    assert Rectangle(3, 4).area() == 12
    assert Square(3).area() == 9
    assert Shape().area() == 0.0


def test_describe_is_inherited_and_polymorphic():
    assert Circle(1).describe() == "Circle with area 3.14"
    assert Square(3).describe() == "Square with area 9.00"


def test_square_uses_super_init():
    s = Square(4)
    assert s.width == 4
    assert s.height == 4
    assert "area" not in Square.__dict__


def test_class_relationships():
    s = Square(2)
    assert isinstance(s, Rectangle) is True
    assert isinstance(s, Shape) is True
    assert isinstance(Circle(1), Rectangle) is False


def test_total_area_mixed_shapes_and_empty():
    shapes = [Circle(1), Rectangle(2, 3), Square(2)]
    assert round(total_area(shapes), 5) == round(3.14159 + 6 + 4, 5)
    assert total_area([]) == 0.0


def test_total_length_across_many_types():
    containers = [[1, 2], "abc", (1,), {"a": 1}, {1, 2, 3}, range(5), Countdown(4)]
    assert total_length(containers) == 2 + 3 + 1 + 1 + 3 + 5 + 4


def test_countdown_sequence_behavior():
    c = Countdown(3)
    assert len(c) == 3
    assert c[0] == 3
    assert c[1] == 2
    assert list(c) == [3, 2, 1]
    assert list(iter(c)) == [3, 2, 1]
    import pytest

    with pytest.raises(IndexError):
        c[-1]
    with pytest.raises(IndexError):
        c[3]


def test_describe_capabilities_on_several_objects():
    assert describe_capabilities(5) == ["add"]
    assert describe_capabilities([1, 2]) == ["add", "index", "iter", "len"]
    assert "add" not in describe_capabilities({"a": 1})
    assert describe_capabilities(lambda: None) == ["call"]
    assert describe_capabilities(Countdown(3)) == ["index", "len"]


def test_first_or_none_for_varied_inputs():
    assert first_or_none([1, 2]) == 1
    assert first_or_none([]) is None
    assert first_or_none({"x": 1}) is None
    assert first_or_none(5) is None
    assert first_or_none({0: "zero"}) == "zero"


def test_add_all_generality_and_order():
    assert add_all([1, 2, 3], 0) == 6
    assert add_all(["b", "c"], "a") == "abc"
    assert add_all([[2], [3]], [1]) == [1, 2, 3]
    assert add_all([], 5) == 5
