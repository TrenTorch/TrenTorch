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
