"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
minkowski = _module.minkowski


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_p_one_is_manhattan_distance():
    assert np.isclose(minkowski([0.0, 0.0], [3.0, -4.0], 1), 7.0)


def test_p_two_is_euclidean_distance():
    assert np.isclose(minkowski([0.0, 0.0], [3.0, -4.0], 2), 5.0)


def test_p_infinity_is_largest_coordinate_gap():
    assert np.isclose(minkowski([0.0, 0.0], [3.0, -4.0], float("inf")), 4.0)


def test_p_three_matches_hand_computation():
    # (|1 - 0|^3 + |2 - 0|^3)^(1/3) = 9^(1/3)
    assert np.isclose(minkowski([1.0, 2.0], [0.0, 0.0], 3), 9 ** (1 / 3))


def test_p_two_agrees_with_numpy_norm_on_random_vectors():
    rng = np.random.default_rng(0)
    x, y = rng.normal(size=6), rng.normal(size=6)
    assert np.isclose(minkowski(x, y, 2), np.linalg.norm(x - y))


def test_identical_points_have_zero_distance():
    x = np.array([1.5, -2.0, 0.0])
    assert minkowski(x, x, 2) == 0.0


def test_distance_is_symmetric():
    rng = np.random.default_rng(1)
    x, y = rng.normal(size=5), rng.normal(size=5)
    assert np.isclose(minkowski(x, y, 1.5), minkowski(y, x, 1.5))


def test_triangle_inequality_holds_for_p_at_least_one():
    rng = np.random.default_rng(2)
    for _ in range(30):
        x, y, z = rng.normal(size=(3, 4))
        assert minkowski(x, z, 1.5) <= minkowski(x, y, 1.5) + minkowski(y, z, 1.5) + 1e-12


def test_scaling_both_points_scales_the_distance():
    x = np.array([1.0, 2.0])
    y = np.array([-3.0, 0.5])
    assert np.isclose(minkowski(4 * x, 4 * y, 3), 4 * minkowski(x, y, 3))


def test_translating_both_points_leaves_distance_unchanged():
    x = np.array([1.0, 2.0])
    y = np.array([-3.0, 0.5])
    shift = np.array([10.0, -7.0])
    assert np.isclose(minkowski(x + shift, y + shift, 2), minkowski(x, y, 2))


def test_distance_shrinks_as_p_grows():
    x = np.array([0.0, 0.0, 0.0])
    y = np.array([1.0, 2.0, 3.0])
    values = [minkowski(x, y, p) for p in [1, 2, 4, float("inf")]]
    assert all(b <= a + 1e-12 for a, b in zip(values, values[1:]))


def test_p_below_one_raises():
    assert _raises_value_error(minkowski, [0.0, 1.0], [1.0, 0.0], 0.5)


def test_shape_mismatch_raises():
    assert _raises_value_error(minkowski, [0.0, 1.0], [1.0], 2)


def test_non_vector_input_raises():
    assert _raises_value_error(minkowski, np.zeros((2, 2)), np.zeros((2, 2)), 2)


def test_inputs_are_not_modified():
    x = np.array([1.0, 2.0])
    y = np.array([3.0, -1.0])
    minkowski(x, y, 2)
    assert np.array_equal(x, [1.0, 2.0]) and np.array_equal(y, [3.0, -1.0])
