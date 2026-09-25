"""
pytest data/app_data/00-python/10-object-oriented-programming/07-assemble-matrix-hierarchy/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(
    f"00-python/10-object-oriented-programming/{Path(__file__).resolve().parent.name}"
)
Matrix = _module.Matrix
IdentityMatrix = _module.IdentityMatrix


def test_constructor_copies_its_input():
    source = [[1, 2], [3, 4]]
    m = Matrix(source)
    source.append([5, 6])
    source[0].append(99)
    assert m.rows == [[1, 2], [3, 4]]


def test_shape_len_and_repr():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    assert m.shape() == (2, 3)
    assert len(m) == 2
    assert repr(m) == "Matrix([[1, 2, 3], [4, 5, 6]])"


def test_eq_and_foreign_types():
    a = Matrix([[1, 2], [3, 4]])
    b = Matrix([[1, 2], [3, 4]])
    c = Matrix([[9, 9], [9, 9]])
    assert a == b
    assert a != c
    assert (a == [[1, 2], [3, 4]]) is False
    assert a.__eq__([[1]]) is NotImplemented


def test_getitem_returns_a_copy():
    m = Matrix([[1, 2], [3, 4]])
    row = m[0]
    row.append(99)
    assert m.rows == [[1, 2], [3, 4]]
    assert m[-1] == [3, 4]


def test_transpose_and_scale_return_new_matrices():
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    t = m.transpose()
    assert t.shape() == (3, 2)
    assert t == Matrix([[1, 4], [2, 5], [3, 6]])
    assert m.shape() == (2, 3)
    assert t.transpose() == m

    s = m.scale(2)
    assert s == Matrix([[2, 4, 6], [8, 10, 12]])
    assert m == Matrix([[1, 2, 3], [4, 5, 6]])


def test_class_level_counter_counts_every_construction():
    Matrix.instances_created = 0
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = IdentityMatrix(2)
    m3 = m1.transpose()
    m4 = m1.scale(2)
    assert Matrix.instances_created == 4
    assert m2 is not None and m3 is not None and m4 is not None


def test_identity_matrix_inherits_and_is_a_matrix():
    identity = IdentityMatrix(3)
    assert identity == Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    assert isinstance(identity, Matrix)
    assert "transpose" not in IdentityMatrix.__dict__
    assert identity.scale(2) == Matrix([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
