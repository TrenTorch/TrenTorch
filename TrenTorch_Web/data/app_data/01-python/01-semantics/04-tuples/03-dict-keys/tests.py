"""
pytest tests.py
"""

from _load import load_solution

_module = load_solution(__file__)
edge_key = _module.edge_key
count_visits = _module.count_visits
group_points_by_cell = _module.group_points_by_cell


def test_edge_key_symmetry_and_equal_endpoints():
    assert edge_key(5, 2) == edge_key(2, 5)
    assert edge_key(5, 2) == (2, 5)
    assert edge_key(3, 3) == (3, 3)


def test_count_visits_merges_separately_created_equal_tuples():
    path = [tuple([0, 0]), tuple([1, 0]), tuple([0, 0])]
    result = count_visits(path)
    assert result == {(0, 0): 2, (1, 0): 1}


def test_count_visits_empty_path():
    assert count_visits([]) == {}


def test_group_points_by_cell_floor_division_with_negatives():
    result = group_points_by_cell([(-1, 0)], 5)
    assert result == {(-1, 0): [(-1, 0)]}


def test_group_points_by_cell_keeps_input_order():
    points = [(1, 1), (9, 1), (2, 3)]
    result = group_points_by_cell(points, 5)
    assert result == {(0, 0): [(1, 1), (2, 3)], (1, 0): [(9, 1)]}
    assert points == [(1, 1), (9, 1), (2, 3)]
