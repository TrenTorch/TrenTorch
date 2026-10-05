import numpy as np
from _load import load_solution


_module = load_solution(__file__)
gcn_layer = _module.gcn_layer


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert output.shape == (5, 4)


def test_identity_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.eye(3)
    output = gcn_layer(features, adj, weight)
    assert np.allclose(output[:, :3], features)


def test_fully_connected():
    features = np.random.randn(4, 2).astype(np.float32)
    adj = np.ones((4, 4))
    weight = np.ones((2, 3)).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert output.shape == (4, 3)


def test_finite_output():
    features = np.random.randn(10, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    weight = np.random.randn(5, 8).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert np.all(np.isfinite(output))


def test_sparse_graph():
    features = np.random.randn(8, 4).astype(np.float32)
    adj = np.eye(8)
    adj[0, 1] = 1
    adj[1, 0] = 1
    weight = np.random.randn(4, 6).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert output.shape == (8, 6)


def test_different_output_dims():
    features = np.random.randn(6, 3).astype(np.float32)
    adj = np.eye(6)
    for out_dim in [1, 2, 5, 10]:
        weight = np.random.randn(3, out_dim).astype(np.float32)
        output = gcn_layer(features, adj, weight)
        assert output.shape == (6, out_dim)


def test_degree_normalization():
    features = np.ones((4, 2)).astype(np.float32)
    adj = np.array([[1, 1, 0, 0],
                     [1, 1, 1, 0],
                     [0, 1, 1, 1],
                     [0, 0, 1, 1]], dtype=float)
    weight = np.ones((2, 3)).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert np.all(np.isfinite(output))


def test_batch_independence():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.random.randint(0, 2, (5, 5)).astype(float)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert output.shape == (5, 4)


def test_zero_features():
    features = np.zeros((5, 3)).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert np.allclose(output, 0.0)


def test_zero_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.zeros((5, 5))
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gcn_layer(features, adj, weight)
    assert np.allclose(output, 0.0)
