"""
pytest data/app_data/00-python/10-object-oriented-programming/06-inheritance-overriding/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
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
