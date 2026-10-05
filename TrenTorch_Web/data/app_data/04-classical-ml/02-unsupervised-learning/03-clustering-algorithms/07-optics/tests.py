"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

optics = load_solution(__file__).optics


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _two_groups():
    a = np.array([[0.0, 0.0], [0.2, 0.0], [0.0, 0.2], [0.2, 0.2]])
    b = np.array([[10.0, 10.0], [10.2, 10.0], [10.0, 10.2], [10.2, 10.2]])
    return np.vstack([a, b])


def test_ordering_is_a_permutation_of_all_points():
    X = _two_groups()
    order, _ = optics(X, 3)
    assert sorted(order.tolist()) == list(range(len(X)))


def test_first_point_in_ordering_has_infinite_reachability():
    order, reach = optics(_two_groups(), 3)
    assert np.isinf(reach[order[0]])


def test_one_group_is_visited_before_the_other():
    order, _ = optics(_two_groups(), 3)
    first_half = set(order[:4].tolist())
    assert first_half == {0, 1, 2, 3} or first_half == {4, 5, 6, 7}


def test_jump_between_groups_is_large_and_inside_groups_small():
    order, reach = optics(_two_groups(), 3)
    finite_inside = [reach[i] for i in range(8) if np.isfinite(reach[i]) and i not in (order[0],)]
    assert max(finite_inside) > 5.0
    within = [reach[i] for i in (1, 2, 3, 5, 6, 7) if np.isfinite(reach[i])]
    assert max(within) < 1.0


def test_reachability_matches_hand_computed_values():
    X = np.array([[0.0], [1.0], [2.5]])
    order, reach = optics(X, 2)
    assert order.tolist() == [0, 1, 2]
    assert np.isinf(reach[0])
    assert np.isclose(reach[1], 1.0)
    assert np.isclose(reach[2], 1.5)


def test_isolated_point_beyond_max_eps_keeps_infinite_reachability():
    X = np.vstack([_two_groups(), [[100.0, 100.0]]])
    _, reach = optics(X, 3, max_eps=2.0)
    assert np.isinf(reach[8])


def test_single_point_gives_trivial_ordering():
    order, reach = optics(np.array([[1.0, 2.0]]), 1)
    assert order.tolist() == [0]
    assert np.isinf(reach[0])


def test_min_samples_out_of_range_raises():
    assert _raises_value_error(optics, _two_groups(), 0)
    assert _raises_value_error(optics, _two_groups(), 9)


def test_reachability_has_one_entry_per_point():
    _, reach = optics(_two_groups(), 3)
    assert reach.shape == (8,)


def test_same_input_gives_same_ordering():
    X = _two_groups()
    o1, _ = optics(X, 3)
    o2, _ = optics(X, 3)
    assert np.array_equal(o1, o2)


def test_does_not_modify_the_data():
    X = _two_groups()
    before = X.copy()
    optics(X, 3)
    assert np.array_equal(X, before)
