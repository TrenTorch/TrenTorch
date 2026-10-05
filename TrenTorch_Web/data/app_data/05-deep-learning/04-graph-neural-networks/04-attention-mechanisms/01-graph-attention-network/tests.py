import numpy as np
from _load import load_solution


_module = load_solution(__file__)
gat_attention_weights = _module.gat_attention_weights


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weights = gat_attention_weights(features, adj)
    assert weights.shape == (5, 5)


def test_attention_sums_to_one():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    weights = gat_attention_weights(features, adj)
    sums = np.sum(weights, axis=1)
    assert np.allclose(sums, 1.0, atol=1e-6)


def test_zero_for_non_edges():
    features = np.random.randn(4, 3).astype(np.float32)
    adj = np.eye(4)
    weights = gat_attention_weights(features, adj)
    expected_zeros = (1 - adj).astype(bool)
    assert np.allclose(weights[expected_zeros], 0.0, atol=1e-6)


def test_fully_connected():
    features = np.random.randn(3, 4).astype(np.float32)
    adj = np.ones((3, 3))
    weights = gat_attention_weights(features, adj)
    assert np.all(np.isfinite(weights))
    assert np.allclose(np.sum(weights, axis=1), 1.0)


def test_sparse_graph():
    features = np.random.randn(6, 2).astype(np.float32)
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    weights = gat_attention_weights(features, adj)
    assert weights.shape == (6, 6)
    assert np.allclose(np.sum(weights, axis=1), 1.0)


def test_identical_features():
    features = np.ones((4, 3)).astype(np.float32)
    adj = np.ones((4, 4))
    weights = gat_attention_weights(features, adj)
    assert np.allclose(weights, 0.25, atol=1e-6)


def test_different_feature_dims():
    for feat_dim in [1, 5, 10]:
        features = np.random.randn(5, feat_dim).astype(np.float32)
        adj = np.eye(5)
        weights = gat_attention_weights(features, adj)
        assert weights.shape == (5, 5)


def test_finite_outputs():
    for _ in range(10):
        features = np.random.randn(5, 4).astype(np.float32)
        adj = np.random.randint(0, 2, (5, 5)).astype(float)
        weights = gat_attention_weights(features, adj)
        assert np.all(np.isfinite(weights))


def test_batch_graphs():
    features = np.random.randn(8, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    weights = gat_attention_weights(features, adj)
    assert weights.shape == (8, 8)


def test_no_self_loops():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    adj = adj - np.diag(np.diag(adj))
    weights = gat_attention_weights(features, adj)
    assert np.allclose(np.diag(weights), 0.0, atol=1e-6)
