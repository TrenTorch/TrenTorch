"""
pytest data/app_data/00-python/04-tuples/05-assemble-analyze-route/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"00-python/04-tuples/{Path(__file__).resolve().parent.name}")
analyze_route = _module.analyze_route


def test_visit_counts_merge_equal_tuples():
    route = [tuple([0, 0]), (1, 0), tuple([0, 0])]
    result = analyze_route(route)
    assert result[0] == {(0, 0): 2, (1, 0): 1}


def test_bounding_box_with_negative_coordinates():
    route = [(-3, -1), (2, 4), (-1, 0)]
    result = analyze_route(route)
    assert type(result[1]) is tuple
    assert result[1] == ((-3, -1), (2, 4))


def test_path_length_across_many_moves():
    route = [(0, 0), (2, 3), (0, 0)]
    result = analyze_route(route)
    assert result[2] == 5 + 5
    assert result[3] == 0


def test_net_displacement_with_extended_unpacking():
    assert analyze_route([(0, 0), (3, 4)])[3] == 7
    assert analyze_route([(0, 0), (1, 1), (3, 4)])[3] == 7
    assert analyze_route([(5, 5)])[3] == 0


def test_revisit_count():
    assert analyze_route([(0, 0), (1, 0), (2, 0)])[4] == 0
    assert analyze_route([(0, 0), (0, 0), (0, 0)])[4] == 2


def test_empty_and_single_point_routes():
    assert analyze_route([]) == ({}, None, 0, 0, 0)
    point = (5, 5)
    assert analyze_route([point]) == ({point: 1}, (point, point), 0, 0, 0)


def test_immutability_of_results_and_inputs():
    route = [(0, 0), (1, 1)]
    result = analyze_route(route)
    assert route == [(0, 0), (1, 1)]
    assert type(result[1]) is tuple
