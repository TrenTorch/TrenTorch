import numpy as np
from _load import load_solution


_module = load_solution(__file__)
gin_layer = _module.gin_layer


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gin_layer(features, adj, weight)
    assert output.shape == (5, 4)


def test_zero_epsilon():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gin_layer(features, adj, weight, epsilon=0.0)
    assert output.shape == (5, 4)


def test_positive_epsilon():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    out1 = gin_layer(features, adj, weight, epsilon=0.0)
    out2 = gin_layer(features, adj, weight, epsilon=0.5)
    assert not np.allclose(out1, out2)


def test_fully_connected():
    features = np.random.randn(4, 2).astype(np.float32)
    adj = np.ones((4, 4))
    weight = np.ones((2, 3)).astype(np.float32)
    output = gin_layer(features, adj, weight)
    assert output.shape == (4, 3)


def test_sparse_graph():
    features = np.random.randn(6, 4).astype(np.float32)
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    weight = np.random.randn(4, 5).astype(np.float32)
    output = gin_layer(features, adj, weight)
    assert output.shape == (6, 5)


def test_finite_output():
    features = np.random.randn(10, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    weight = np.random.randn(5, 8).astype(np.float32)
    output = gin_layer(features, adj, weight, epsilon=0.1)
    assert np.all(np.isfinite(output))


def test_identity_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.eye(3)
    output = gin_layer(features, adj, weight, epsilon=0.0)
    assert np.allclose(output[:, :3], features)


def test_zero_features():
    features = np.zeros((5, 3)).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = gin_layer(features, adj, weight)
    assert np.allclose(output, 0.0)


def test_different_epsilon_values():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    weight = np.ones((3, 2)).astype(np.float32)
    for epsilon in [0.0, 0.5, 1.0, 2.0]:
        output = gin_layer(features, adj, weight, epsilon)
        assert np.all(np.isfinite(output))


def test_large_epsilon():
    features = np.ones((4, 2)).astype(np.float32)
    adj = np.zeros((4, 4))
    weight = np.ones((2, 3)).astype(np.float32)
    output = gin_layer(features, adj, weight, epsilon=10.0)
    assert np.all(np.isfinite(output))
