"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
lvq1_step = _module.lvq1_step

P0 = np.array([[0.0, 0.0], [4.0, 0.0]])
L0 = np.array([0, 1])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def test_matching_label_moves_winner_toward_example():
    P, winner = lvq1_step(P0, L0, [1.0, 0.0], 0, 0.5)
    assert winner == 0
    assert np.allclose(P[0], [0.5, 0.0])


def test_mismatched_label_moves_winner_away_from_example():
    P, winner = lvq1_step(P0, L0, [1.0, 0.0], 1, 0.5)
    assert winner == 0
    assert np.allclose(P[0], [-0.5, 0.0])


def test_mismatch_increases_distance_to_the_example():
    x = np.array([1.0, 0.0])
    P, _ = lvq1_step(P0, L0, x, 1, 0.5)
    assert np.linalg.norm(P[0] - x) > np.linalg.norm(P0[0] - x)


def test_only_the_winner_moves():
    P, _ = lvq1_step(P0, L0, [1.0, 0.0], 0, 0.5)
    assert np.array_equal(P[1], P0[1])


def test_nearest_prototype_wins_even_when_it_is_not_first():
    P, winner = lvq1_step(P0, L0, [3.5, 0.0], 1, 0.5)
    assert winner == 1
    assert np.allclose(P[1], [3.75, 0.0])


def test_zero_learning_rate_leaves_prototypes_unchanged():
    P, _ = lvq1_step(P0, L0, [1.0, 2.0], 0, 0.0)
    assert np.array_equal(P, P0)


def test_tie_goes_to_the_lowest_index():
    P = np.array([[0.0, 0.0], [2.0, 0.0]])
    _, winner = lvq1_step(P, L0, [1.0, 0.0], 0, 0.5)
    assert winner == 0


def test_repeated_matching_steps_pull_the_prototype_closer():
    x = np.array([1.0, 1.0])
    P = P0.copy()
    distances = []
    for _ in range(5):
        P, _ = lvq1_step(P, L0, x, 0, 0.5)
        distances.append(np.linalg.norm(P[0] - x))
    assert all(b < a for a, b in zip(distances, distances[1:]))


def test_translating_data_and_prototypes_translates_the_result():
    shift = np.array([10.0, -3.0])
    P, _ = lvq1_step(P0, L0, [1.0, 0.0], 0, 0.5)
    Q, _ = lvq1_step(P0 + shift, L0, np.array([1.0, 0.0]) + shift, 0, 0.5)
    assert np.allclose(Q, P + shift)


def test_input_prototypes_are_not_modified():
    P = P0.copy()
    lvq1_step(P, L0, [1.0, 0.0], 0, 0.5)
    assert np.array_equal(P, P0)


def test_negative_learning_rate_raises():
    assert _raises_value_error(lvq1_step, P0, L0, [1.0, 0.0], 0, -0.1)


def test_example_length_mismatch_raises():
    assert _raises_value_error(lvq1_step, P0, L0, [1.0, 0.0, 2.0], 0, 0.1)


def test_label_length_mismatch_raises():
    assert _raises_value_error(lvq1_step, P0, [0], [1.0, 0.0], 0, 0.1)


def test_empty_prototype_set_raises():
    assert _raises_value_error(lvq1_step, np.zeros((0, 2)), np.array([], dtype=int), [1.0, 0.0], 0, 0.1)
