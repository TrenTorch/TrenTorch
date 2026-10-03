"""
pytest tests.py
"""

import numpy as np

from _load import load_solution

_module = load_solution(__file__)
mutual_information = _module.mutual_information
chow_liu_tree = _module.chow_liu_tree


def _raises_value_error(function, *args, **kwargs):
    try:
        function(*args, **kwargs)
    except ValueError:
        return True
    return False


def _is_connected(n, edges):
    adj = {i: set() for i in range(n)}
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def test_balanced_identical_bits_have_one_bit_of_information():
    a = np.array([0, 0, 1, 1])
    assert np.isclose(mutual_information(a, a), 1.0)


def test_independent_variables_have_zero_information():
    a = np.array([0, 0, 1, 1])
    b = np.array([0, 1, 0, 1])
    assert np.isclose(mutual_information(a, b), 0.0)


def test_mutual_information_is_symmetric():
    rng = np.random.default_rng(0)
    a = rng.integers(0, 3, size=50)
    b = rng.integers(0, 2, size=50)
    assert np.isclose(mutual_information(a, b), mutual_information(b, a))


def test_information_does_not_depend_on_value_names():
    a = np.array([0, 0, 1, 1, 1])
    b = np.array([0, 1, 1, 1, 0])
    assert np.isclose(mutual_information(a, b), mutual_information(a + 5, b * 7))


def test_constant_variable_has_zero_information():
    assert np.isclose(mutual_information(np.zeros(6, dtype=int), [0, 1, 0, 1, 1, 0]), 0.0)


def test_information_is_never_negative():
    rng = np.random.default_rng(1)
    for _ in range(10):
        a = rng.integers(0, 4, size=40)
        b = rng.integers(0, 4, size=40)
        assert mutual_information(a, b) >= -1e-12


def test_mutual_information_length_mismatch_raises():
    assert _raises_value_error(mutual_information, [0, 1], [0, 1, 1])


def test_two_variables_give_one_edge():
    X = np.array([[0, 0], [1, 1], [0, 0], [1, 1]])
    assert chow_liu_tree(X) == [(0, 1)]


def test_one_variable_gives_no_edges():
    assert chow_liu_tree(np.array([[0], [1], [1]])) == []


def test_tree_has_d_minus_one_edges_and_spans_all_nodes():
    rng = np.random.default_rng(2)
    X = rng.integers(0, 2, size=(120, 5))
    edges = chow_liu_tree(X)
    assert len(edges) == 4
    assert _is_connected(5, edges)


def test_edges_are_sorted_pairs_with_i_less_than_j():
    rng = np.random.default_rng(3)
    X = rng.integers(0, 3, size=(80, 4))
    edges = chow_liu_tree(X)
    assert all(i < j for i, j in edges)
    assert edges == sorted(edges)


def test_strongly_dependent_pair_is_kept():
    rng = np.random.default_rng(4)
    a = rng.integers(0, 2, size=300)
    flip = rng.random(300) < 0.1
    c = np.where(flip, 1 - a, a)
    X = np.column_stack([a, a.copy(), c])
    assert (0, 1) in chow_liu_tree(X)


def test_tree_has_maximum_total_information_against_a_chain():
    rng = np.random.default_rng(5)
    X = rng.integers(0, 2, size=(200, 4))
    X[:, 1] = np.where(rng.random(200) < 0.2, 1 - X[:, 0], X[:, 0])
    X[:, 3] = np.where(rng.random(200) < 0.3, 1 - X[:, 2], X[:, 2])
    tree = chow_liu_tree(X)
    chain = [(0, 1), (1, 2), (2, 3)]
    tree_total = sum(mutual_information(X[:, i], X[:, j]) for i, j in tree)
    chain_total = sum(mutual_information(X[:, i], X[:, j]) for i, j in chain)
    assert tree_total >= chain_total - 1e-12


def test_non_matrix_input_raises():
    assert _raises_value_error(chow_liu_tree, np.array([0, 1, 1]))


def test_inputs_are_not_modified():
    X = np.array([[0, 1], [1, 1], [0, 0], [1, 0]])
    X0 = X.copy()
    chow_liu_tree(X)
    assert np.array_equal(X, X0)
