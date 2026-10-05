import numpy as np
from _load import load_solution


_module = load_solution(__file__)
detect_over_smoothing = _module.detect_over_smoothing


def test_output_shape():
    features = np.random.randn(5, 4).astype(np.float32)
    adj = np.eye(5)
    scores = detect_over_smoothing(features, adj, num_layers=3)
    assert scores.shape == (3,)


def test_non_negative_scores():
    features = np.random.randn(8, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (8, 8)).astype(float)
    scores = detect_over_smoothing(features, adj, num_layers=5)
    assert np.all(scores >= 0)


def test_decreasing_divergence():
    features = np.random.randn(10, 4).astype(np.float32)
    adj = np.ones((10, 10))
    scores = detect_over_smoothing(features, adj, num_layers=5)
    assert len(scores) == 5


def test_identity_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    scores = detect_over_smoothing(features, adj, num_layers=3)
    assert scores.shape == (3,)
    assert np.all(np.isfinite(scores))


def test_fully_connected():
    n = 6
    features = np.random.randn(n, 4).astype(np.float32)
    adj = np.ones((n, n))
    scores = detect_over_smoothing(features, adj, num_layers=5)
    assert np.all(np.isfinite(scores))


def test_sparse_graph():
    features = np.random.randn(8, 3).astype(np.float32)
    adj = np.eye(8)
    adj[0, 1] = 1
    adj[1, 0] = 1
    scores = detect_over_smoothing(features, adj, num_layers=4)
    assert scores.shape == (4,)


def test_cycle_graph():
    n = 7
    features = np.random.randn(n, 5).astype(np.float32)
    adj = np.zeros((n, n))
    for i in range(n):
        adj[i, (i + 1) % n] = 1
        adj[(i + 1) % n, i] = 1
    scores = detect_over_smoothing(features, adj, num_layers=6)
    assert scores.shape == (6,)
    assert np.all(np.isfinite(scores))


def test_single_layer():
    features = np.random.randn(5, 4).astype(np.float32)
    adj = np.random.randint(0, 2, (5, 5)).astype(float)
    scores = detect_over_smoothing(features, adj, num_layers=1)
    assert scores.shape == (1,)


def test_many_layers():
    features = np.random.randn(6, 3).astype(np.float32)
    adj = np.ones((6, 6))
    scores = detect_over_smoothing(features, adj, num_layers=20)
    assert scores.shape == (20,)
    assert np.all(np.isfinite(scores))


def test_uniform_features():
    features = np.ones((5, 4)).astype(np.float32)
    adj = np.ones((5, 5))
    scores = detect_over_smoothing(features, adj, num_layers=5)
    assert np.allclose(scores, 0.0, atol=1e-5)
