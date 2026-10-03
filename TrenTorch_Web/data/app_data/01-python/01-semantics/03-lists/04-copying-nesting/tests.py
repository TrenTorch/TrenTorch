"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
shallow_copy = _module.shallow_copy
deep_copy = _module.deep_copy
shares_inner_objects = _module.shares_inner_objects
add_row_safely = _module.add_row_safely
make_grid = _module.make_grid
rows_are_independent = _module.rows_are_independent
transpose = _module.transpose


def test_shallow_copy_new_list_shares_elements():
    a = [[1, 2], [3]]
    b = shallow_copy(a)
    assert id(b) != id(a)
    b.append([4])
    assert a == [[1, 2], [3]]
    assert shares_inner_objects(a, shallow_copy(a)) is True


def test_shallow_copy_shows_shared_mutation():
    a = [[1, 2], [3]]
    b = shallow_copy(a)
    b[0].append(99)
    assert a == [[1, 2, 99], [3]]


def test_deep_copy_independence_at_depth():
    a = [[1, [2, 3]], [4]]
    b = deep_copy(a)
    b[0][1].append(99)
    assert a == [[1, [2, 3]], [4]]


def test_shares_inner_objects_distinguishes_equal_from_identical():
    a = [[1, 2], [3]]
    b = deep_copy(a)
    assert shares_inner_objects(a, b) is False
    assert shares_inner_objects([], []) is True


def test_add_row_safely_leaves_every_input_untouched():
    matrix = [[1, 2], [3, 4]]
    row = [5, 6]
    result = add_row_safely(matrix, row)
    assert result == [[1, 2], [3, 4], [5, 6]]

    result[0].append(99)
    result[2].append(7)
    assert matrix == [[1, 2], [3, 4]]
    assert row == [5, 6]


def test_make_grid_rows_are_independent():
    grid = make_grid(2, 3, 0)
    grid[0].append(99)
    assert grid[1] == [0, 0, 0]


def test_make_grid_shapes():
    assert make_grid(0, 3, 0) == []
    assert make_grid(3, 0, 0) == [[], [], []]
    assert make_grid(1, 1, "x") == [["x"]]
    assert make_grid(2, 3, 0) == [[0, 0, 0], [0, 0, 0]]


def test_rows_are_independent_detects_the_star_trap():
    shared = [[0]] * 3
    assert rows_are_independent(shared) is False
    built = [[0] for _ in range(3)]
    assert rows_are_independent(built) is True
    assert rows_are_independent([]) is True
    assert rows_are_independent([[1]]) is True


def test_transpose_shape_values_and_non_square():
    result = transpose([[1, 2, 3], [4, 5, 6]])
    assert result == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 2, 3]]) == [[1], [2], [3]]


def test_transpose_does_not_share_rows_and_leaves_input_intact():
    matrix = [[1, 2, 3], [4, 5, 6]]
    result = transpose(matrix)
    result[0].append(99)
    assert matrix == [[1, 2, 3], [4, 5, 6]]
