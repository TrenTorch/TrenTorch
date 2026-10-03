"""
pytest tests.py
"""

import itertools

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
viterbi = _module.viterbi

PI = np.array([0.6, 0.4])
A = np.array([[0.7, 0.3], [0.4, 0.6]])
B = np.array([[0.9, 0.1], [0.2, 0.8]])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _joint(path, pi, A, B, obs):
    p = pi[path[0]] * B[path[0], obs[0]]
    for t in range(1, len(obs)):
        p *= A[path[t - 1], path[t]] * B[path[t], obs[t]]
    return p


def _brute_force_best(pi, A, B, obs):
    K = len(pi)
    best_path, best_p = None, -1.0
    for path in itertools.product(range(K), repeat=len(obs)):
        p = _joint(path, pi, A, B, obs)
        if p > best_p:
            best_path, best_p = list(path), p
    return best_path, best_p


def test_returned_probability_equals_brute_force_maximum():
    obs = [0, 1, 1]
    _, prob = viterbi(PI, A, B, obs)
    _, best = _brute_force_best(PI, A, B, obs)
    assert np.isclose(prob, best)


def test_returned_path_achieves_brute_force_maximum():
    obs = [0, 1, 1, 0]
    path, prob = viterbi(PI, A, B, obs)
    assert np.isclose(_joint(path, PI, A, B, obs), prob)
    _, best = _brute_force_best(PI, A, B, obs)
    assert np.isclose(prob, best)


def test_path_length_matches_sequence_length():
    path, _ = viterbi(PI, A, B, [0, 0, 1, 1, 0])
    assert len(path) == 5


def test_path_states_are_valid_indices():
    path, _ = viterbi(PI, A, B, [1, 0, 1])
    assert set(path) <= {0, 1}


def test_single_observation_picks_state_with_largest_pi_times_emission():
    # pi_0 * B[0, 0] = 0.54, pi_1 * B[1, 0] = 0.08.
    path, prob = viterbi(PI, A, B, [0])
    assert path == [0] and np.isclose(prob, 0.54)


def test_sticky_transitions_keep_one_state_when_emissions_are_mild():
    sticky = np.array([[0.99, 0.01], [0.01, 0.99]])
    emit = np.array([[0.6, 0.4], [0.4, 0.6]])
    path, _ = viterbi(np.array([0.5, 0.5]), sticky, emit, [0, 0, 0, 0])
    assert path == [0, 0, 0, 0]


def test_strong_emissions_drive_the_path_despite_transitions():
    emit = np.array([[0.99, 0.01], [0.01, 0.99]])
    path, _ = viterbi(np.array([0.5, 0.5]), A, emit, [0, 1, 0])
    assert path == [0, 1, 0]


def test_brute_force_agreement_on_several_random_sequences():
    rng = np.random.default_rng(0)
    for _ in range(10):
        obs = rng.integers(0, 2, size=4).tolist()
        _, prob = viterbi(PI, A, B, obs)
        _, best = _brute_force_best(PI, A, B, obs)
        assert np.isclose(prob, best)


def test_probability_is_at_most_one():
    _, prob = viterbi(PI, A, B, [0, 1, 0, 1, 0])
    assert 0.0 < prob <= 1.0


def test_out_of_range_observation_raises():
    assert _raises_value_error(viterbi, PI, A, B, [0, 5])


def test_empty_sequence_raises():
    assert _raises_value_error(viterbi, PI, A, B, [])


def test_non_stochastic_initial_distribution_raises():
    assert _raises_value_error(viterbi, np.array([0.5, 0.6]), A, B, [0, 1])


def test_inputs_are_not_modified():
    obs = np.array([0, 1, 1])
    before = B.copy()
    viterbi(PI, A, B, obs)
    assert np.array_equal(B, before)
