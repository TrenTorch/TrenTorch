import numpy as np
from _load import load_solution


_module = load_solution(__file__)
message_passing = _module.message_passing


def message_fn_simple(sender, receiver):
    return sender


def message_fn_add(sender, receiver):
    return sender + receiver


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    output = message_passing(features, adj, message_fn_simple)
    assert output.shape == (5, 3)


def test_identity_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    output = message_passing(features, adj, message_fn_simple)
    assert np.allclose(output, features)


def test_zero_adjacency():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.zeros((5, 5))
    output = message_passing(features, adj, message_fn_simple)
    assert np.allclose(output, 0.0)


def test_fully_connected():
    features = np.ones((4, 2)).astype(np.float32)
    adj = np.ones((4, 4))
    output = message_passing(features, adj, message_fn_simple)
    assert np.allclose(output, features)


def test_different_message_functions():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    out1 = message_passing(features, adj, message_fn_simple)
    out2 = message_passing(features, adj, message_fn_add)
    assert not np.allclose(out1, out2)


def test_sparse_graph():
    features = np.random.randn(6, 4).astype(np.float32)
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    output = message_passing(features, adj, message_fn_simple)
    assert output.shape == (6, 4)


def test_finite_output():
    features = np.random.randn(10, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    output = message_passing(features, adj, message_fn_simple)
    assert np.all(np.isfinite(output))


def test_message_aggregation():
    features = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]], dtype=np.float32)
    adj = np.array([[0, 1, 0], [1, 0, 1], [0, 1, 0]], dtype=float)
    output = message_passing(features, adj, message_fn_simple)
    assert output.shape == (3, 2)


def test_custom_message_function():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    def custom_msg(sender, receiver):
        return sender * 2
    output = message_passing(features, adj, custom_msg)
    assert output.shape == (5, 3)


def test_large_graphs():
    features = np.random.randn(100, 10).astype(np.float32)
    adj = np.random.randint(0, 2, (100, 100)).astype(float)
    output = message_passing(features, adj, message_fn_simple)
    assert output.shape == (100, 10)
    assert np.all(np.isfinite(output))
