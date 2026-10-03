"""
pytest tests.py
"""

import itertools

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
state_posteriors = _module.state_posteriors

PI = np.array([0.6, 0.4])
A = np.array([[0.7, 0.3], [0.4, 0.6]])
B = np.array([[0.9, 0.1], [0.2, 0.8]])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _brute_force_posteriors(pi, A, B, obs):
    K, T = len(pi), len(obs)
    gamma = np.zeros((T, K))
    total = 0.0
    for path in itertools.product(range(K), repeat=T):
        p = pi[path[0]] * B[path[0], obs[0]]
        for t in range(1, T):
            p *= A[path[t - 1], path[t]] * B[path[t], obs[t]]
        total += p
        for t, s in enumerate(path):
            gamma[t, s] += p
    return gamma / total


def test_matches_brute_force_on_length_three():
    obs = [0, 1, 1]
    assert np.allclose(state_posteriors(PI, A, B, obs), _brute_force_posteriors(PI, A, B, obs))


def test_matches_brute_force_on_length_four():
    obs = [1, 0, 0, 1]
    assert np.allclose(state_posteriors(PI, A, B, obs), _brute_force_posteriors(PI, A, B, obs))


def test_rows_sum_to_one():
    gamma = state_posteriors(PI, A, B, [0, 1, 0, 0, 1])
    assert np.allclose(gamma.sum(axis=1), 1.0)


def test_output_shape_is_time_by_state():
    assert state_posteriors(PI, A, B, [0, 1, 1]).shape == (3, 2)


def test_single_state_gives_all_ones():
    gamma = state_posteriors(np.array([1.0]), np.array([[1.0]]), np.array([[0.3, 0.7]]), [0, 1, 1])
    assert np.allclose(gamma, 1.0)


def test_single_observation_is_proportional_to_pi_times_emission():
    gamma = state_posteriors(PI, A, B, [0])
    expected = PI * B[:, 0]
    assert np.allclose(gamma[0], expected / expected.sum())


def test_strong_emissions_make_posteriors_confident():
    emit = np.array([[0.99, 0.01], [0.01, 0.99]])
    gamma = state_posteriors(np.array([0.5, 0.5]), A, emit, [0, 0, 0])
    assert np.all(gamma[:, 0] > 0.9)


def test_future_observations_change_earlier_posterior():
    # Seeing symbol 1 later should shift belief about the earlier state.
    gamma_alone = state_posteriors(PI, A, B, [0])
    gamma_with_future = state_posteriors(PI, A, B, [0, 1, 1])
    assert not np.allclose(gamma_alone[0], gamma_with_future[0])


def test_all_entries_are_between_zero_and_one():
    gamma = state_posteriors(PI, A, B, [1, 0, 1, 1])
    assert np.all((gamma >= 0) & (gamma <= 1))


def test_out_of_range_observation_raises():
    assert _raises_value_error(state_posteriors, PI, A, B, [0, 3])


def test_empty_sequence_raises():
    assert _raises_value_error(state_posteriors, PI, A, B, [])


def test_non_stochastic_emission_row_raises():
    bad = np.array([[0.9, 0.9], [0.2, 0.8]])
    assert _raises_value_error(state_posteriors, PI, A, bad, [0, 1])


def test_inputs_are_not_modified():
    obs = np.array([0, 1, 1])
    before = A.copy()
    state_posteriors(PI, A, B, obs)
    assert np.array_equal(A, before) and obs.tolist() == [0, 1, 1]
