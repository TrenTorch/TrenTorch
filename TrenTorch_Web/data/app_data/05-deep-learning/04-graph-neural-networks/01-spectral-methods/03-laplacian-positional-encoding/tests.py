import numpy as np
from _load import load_solution


_module = load_solution(__file__)
laplacian_positional_encoding = _module.laplacian_positional_encoding


def test_basic_shape():
    adj = np.eye(5)
    pe = laplacian_positional_encoding(adj, k=3)
    assert pe.shape == (5, 3)


def test_default_k():
    adj = np.eye(8)
    pe = laplacian_positional_encoding(adj)
    assert pe.shape == (8, 10)


def test_k_larger_than_nodes():
    adj = np.eye(3)
    pe = laplacian_positional_encoding(adj, k=10)
    assert pe.shape == (3, 10)


def test_fully_connected():
    n = 5
    adj = np.ones((n, n)) - np.eye(n)
    pe = laplacian_positional_encoding(adj, k=3)
    assert pe.shape == (n, 3)


def test_finite_output():
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    pe = laplacian_positional_encoding(adj, k=5)
    assert np.all(np.isfinite(pe))


def test_different_k_values():
    adj = np.eye(10)
    for k_val in [1, 3, 5, 10, 20]:
        pe = laplacian_positional_encoding(adj, k=k_val)
        assert pe.shape == (10, k_val)


def test_sparse_graph():
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    pe = laplacian_positional_encoding(adj, k=4)
    assert pe.shape == (6, 4)


def test_cycle_graph():
    n = 7
    adj = np.zeros((n, n))
    for i in range(n):
        adj[i, (i + 1) % n] = 1
        adj[(i + 1) % n, i] = 1
    pe = laplacian_positional_encoding(adj, k=3)
    assert pe.shape == (n, 3)


def test_star_graph():
    n = 8
    adj = np.zeros((n, n))
    adj[0, 1:] = 1
    adj[1:, 0] = 1
    pe = laplacian_positional_encoding(adj, k=5)
    assert pe.shape == (n, 5)


def test_symmetry():
    adj = np.random.randint(0, 2, (5, 5)).astype(float)
    adj = (adj + adj.T) / 2
    pe = laplacian_positional_encoding(adj, k=3)
    assert pe.shape == (5, 3)
    assert np.all(np.isfinite(pe))
