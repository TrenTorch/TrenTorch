"""
pytest tests.py
"""

import itertools

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
forward_likelihood = _module.forward_likelihood

PI = np.array([0.6, 0.4])
A = np.array([[0.7, 0.3], [0.4, 0.6]])
B = np.array([[0.9, 0.1], [0.2, 0.8]])


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _brute_force(pi, A, B, obs):
    K = len(pi)
    total = 0.0
    for path in itertools.product(range(K), repeat=len(obs)):
        p = pi[path[0]] * B[path[0], obs[0]]
        for t in range(1, len(obs)):
            p *= A[path[t - 1], path[t]] * B[path[t], obs[t]]
        total += p
    return total


def test_single_state_single_symbol_is_emission_probability():
    one = np.array([1.0])
    assert np.isclose(forward_likelihood(one, np.array([[1.0]]), np.array([[0.2, 0.8]]), [1]), 0.8)


def test_single_state_sequence_is_product_of_emissions():
    one = np.array([1.0])
    assert np.isclose(forward_likelihood(one, np.array([[1.0]]), np.array([[0.2, 0.8]]), [0, 1]), 0.16)


def test_matches_brute_force_on_length_three_sequence():
    obs = [0, 1, 1]
    assert np.isclose(forward_likelihood(PI, A, B, obs), _brute_force(PI, A, B, obs))


def test_matches_brute_force_on_length_four_sequence():
    obs = [1, 0, 0, 1]
    assert np.isclose(forward_likelihood(PI, A, B, obs), _brute_force(PI, A, B, obs))


def test_likelihood_over_all_length_one_sequences_sums_to_one():
    total = sum(forward_likelihood(PI, A, B, [m]) for m in range(2))
    assert np.isclose(total, 1.0)


def test_likelihood_over_all_length_two_sequences_sums_to_one():
    total = sum(forward_likelihood(PI, A, B, [a, b]) for a, b in itertools.product(range(2), repeat=2))
    assert np.isclose(total, 1.0)


def test_likelihood_is_between_zero_and_one():
    p = forward_likelihood(PI, A, B, [0, 0, 1, 0])
    assert 0.0 < p < 1.0


def test_identity_transitions_keep_state_fixed():
    I = np.eye(2)
    # With state fixed at 0 (pi = [1, 0]), p([0, 0]) = B[0, 0]^2.
    p = forward_likelihood(np.array([1.0, 0.0]), I, B, [0, 0])
    assert np.isclose(p, 0.81)


def test_accepts_python_lists_as_inputs():
    p1 = forward_likelihood(PI.tolist(), A.tolist(), B.tolist(), [0, 1])
    p2 = forward_likelihood(PI, A, B, np.array([0, 1]))
    assert np.isclose(p1, p2)


def test_out_of_range_observation_raises():
    assert _raises_value_error(forward_likelihood, PI, A, B, [0, 2])


def test_empty_sequence_raises():
    assert _raises_value_error(forward_likelihood, PI, A, B, [])


def test_non_stochastic_transition_row_raises():
    bad = np.array([[0.7, 0.7], [0.4, 0.6]])
    assert _raises_value_error(forward_likelihood, PI, bad, B, [0, 1])


def test_negative_probability_raises():
    bad = np.array([[1.2, -0.2], [0.4, 0.6]])
    assert _raises_value_error(forward_likelihood, PI, bad, B, [0, 1])


def test_inputs_are_not_modified():
    obs = np.array([0, 1, 1])
    before = A.copy()
    forward_likelihood(PI, A, B, obs)
    assert np.array_equal(A, before) and obs.tolist() == [0, 1, 1]
