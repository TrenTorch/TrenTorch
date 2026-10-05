import numpy as np
from _load import load_solution


_module = load_solution(__file__)
chebyshev_conv = _module.chebyshev_conv


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(4, 3, 4).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=3)
    assert output.shape == (5, 4)


def test_different_k_values():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    for k_val in [1, 2, 3, 5]:
        weight = np.random.randn(k_val + 1, 3, 4).astype(np.float32)
        output = chebyshev_conv(features, adj, weight, k=k_val)
        assert output.shape == (5, 4)


def test_finite_output():
    features = np.random.randn(8, 4).astype(np.float32)
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    weight = np.random.randn(4, 4, 6).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=3)
    assert np.all(np.isfinite(output))


def test_fully_connected():
    features = np.random.randn(4, 2).astype(np.float32)
    adj = np.ones((4, 4))
    weight = np.random.randn(4, 2, 3).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=3)
    assert output.shape == (4, 3)


def test_sparse_graph():
    features = np.random.randn(6, 3).astype(np.float32)
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    weight = np.random.randn(4, 3, 5).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=3)
    assert output.shape == (6, 5)


def test_different_output_dims():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    for out_dim in [1, 2, 5, 10]:
        weight = np.random.randn(4, 3, out_dim).astype(np.float32)
        output = chebyshev_conv(features, adj, weight, k=3)
        assert output.shape == (5, out_dim)


def test_zero_features():
    features = np.zeros((5, 3)).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(4, 3, 4).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=3)
    assert np.allclose(output, 0.0)


def test_k_one():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    weight = np.random.randn(2, 3, 4).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=1)
    assert output.shape == (5, 4)


def test_random_graphs():
    for _ in range(5):
        features = np.random.randn(8, 4).astype(np.float32)
        adj = np.random.randint(0, 2, (8, 8)).astype(float)
        weight = np.random.randn(4, 4, 5).astype(np.float32)
        output = chebyshev_conv(features, adj, weight, k=3)
        assert np.all(np.isfinite(output))


def test_large_k():
    features = np.random.randn(6, 2).astype(np.float32)
    adj = np.ones((6, 6))
    weight = np.random.randn(11, 2, 3).astype(np.float32)
    output = chebyshev_conv(features, adj, weight, k=10)
    assert output.shape == (6, 3)
