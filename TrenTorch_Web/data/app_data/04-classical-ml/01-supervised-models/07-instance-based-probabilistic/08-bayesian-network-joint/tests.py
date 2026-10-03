"""
pytest tests.py
"""

import itertools

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
joint_probability = _module.joint_probability


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


# Chain A -> B with binary variables.
CHAIN_PARENTS = [(), (0,)]
CHAIN_CPTS = [np.array([0.6, 0.4]), np.array([[0.9, 0.1], [0.2, 0.8]])]

# Collider A -> C <- B with binary variables.
COLLIDER_PARENTS = [(), (), (0, 1)]
COLLIDER_CPTS = [
    np.array([0.6, 0.4]),
    np.array([0.5, 0.5]),
    np.array([[[0.9, 0.1], [0.3, 0.7]], [[0.5, 0.5], [0.2, 0.8]]]),
]


def test_root_only_network_returns_the_table_entry():
    assert np.isclose(joint_probability((1,), [()], [np.array([0.3, 0.7])]), 0.7)


def test_chain_joint_is_product_of_local_tables():
    assert np.isclose(joint_probability((1, 0), CHAIN_PARENTS, CHAIN_CPTS), 0.08)


def test_chain_joint_sums_to_one_over_all_assignments():
    total = sum(joint_probability(x, CHAIN_PARENTS, CHAIN_CPTS) for x in itertools.product([0, 1], repeat=2))
    assert np.isclose(total, 1.0)


def test_marginal_of_root_is_recovered_by_summing_out_the_child():
    p_a1 = sum(joint_probability((1, b), CHAIN_PARENTS, CHAIN_CPTS) for b in [0, 1])
    assert np.isclose(p_a1, 0.4)


def test_collider_joint_matches_hand_computation():
    # P(A=1) * P(B=0) * P(C=1 | A=1, B=0) = 0.4 * 0.5 * 0.5
    assert np.isclose(joint_probability((1, 0, 1), COLLIDER_PARENTS, COLLIDER_CPTS), 0.1)


def test_collider_joint_sums_to_one_over_all_assignments():
    total = sum(joint_probability(x, COLLIDER_PARENTS, COLLIDER_CPTS) for x in itertools.product([0, 1], repeat=3))
    assert np.isclose(total, 1.0)


def test_independent_roots_multiply_their_marginals():
    parents = [(), ()]
    cpts = [np.array([0.3, 0.7]), np.array([0.25, 0.75])]
    assert np.isclose(joint_probability((1, 0), parents, cpts), 0.7 * 0.25)


def test_all_joint_values_are_nonnegative():
    values = [joint_probability(x, CHAIN_PARENTS, CHAIN_CPTS) for x in itertools.product([0, 1], repeat=2)]
    assert min(values) >= 0.0


def test_value_out_of_range_raises():
    assert _raises_value_error(joint_probability, (2, 0), CHAIN_PARENTS, CHAIN_CPTS)


def test_unnormalized_row_raises():
    bad_cpts = [np.array([0.6, 0.4]), np.array([[0.9, 0.2], [0.2, 0.8]])]
    assert _raises_value_error(joint_probability, (1, 0), CHAIN_PARENTS, bad_cpts)


def test_wrong_table_rank_raises():
    bad_cpts = [np.array([0.6, 0.4]), np.array([0.9, 0.1])]
    assert _raises_value_error(joint_probability, (1, 0), CHAIN_PARENTS, bad_cpts)


def test_length_mismatch_raises():
    assert _raises_value_error(joint_probability, (1,), CHAIN_PARENTS, CHAIN_CPTS)


def test_inputs_are_not_modified():
    x = [1, 0]
    cpts = [c.copy() for c in CHAIN_CPTS]
    joint_probability(x, CHAIN_PARENTS, cpts)
    assert x == [1, 0] and all(np.array_equal(a, b) for a, b in zip(cpts, CHAIN_CPTS))
