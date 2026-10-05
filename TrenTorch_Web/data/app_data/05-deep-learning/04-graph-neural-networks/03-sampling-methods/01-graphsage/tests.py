import numpy as np
from _load import load_solution


_module = load_solution(__file__)
graphsage_layer = _module.graphsage_layer


def test_basic_shape():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=2)
    assert output.shape == (5, 4)


def test_identity_case():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.eye(3)
    np.random.seed(42)
    output = graphsage_layer(features, adj, weight, num_samples=2)
    assert output.shape == (5, 3)


def test_fully_connected():
    features = np.random.randn(4, 2).astype(np.float32)
    adj = np.ones((4, 4))
    weight = np.ones((2, 3)).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=2)
    assert output.shape == (4, 3)


def test_sparse_graph():
    features = np.random.randn(6, 4).astype(np.float32)
    adj = np.eye(6)
    adj[0, 1] = 1
    adj[1, 0] = 1
    weight = np.random.randn(4, 5).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=1)
    assert output.shape == (6, 5)


def test_different_sample_sizes():
    features = np.random.randn(8, 3).astype(np.float32)
    adj = np.ones((8, 8))
    weight = np.random.randn(3, 4).astype(np.float32)
    for num_samples in [1, 2, 4, 8]:
        output = graphsage_layer(features, adj, weight, num_samples)
        assert output.shape == (8, 4)


def test_finite_output():
    features = np.random.randn(10, 5).astype(np.float32)
    adj = np.random.randint(0, 2, (10, 10)).astype(float)
    weight = np.random.randn(5, 8).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=3)
    assert np.all(np.isfinite(output))


def test_isolated_nodes():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    weight = np.random.randn(3, 4).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=2)
    assert output.shape == (5, 4)


def test_all_samples_available():
    features = np.random.randn(4, 3).astype(np.float32)
    adj = np.ones((4, 4))
    weight = np.ones((3, 2)).astype(np.float32)
    output = graphsage_layer(features, adj, weight, num_samples=10)
    assert output.shape == (4, 2)


def test_reproducibility_with_seed():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.ones((5, 5))
    weight = np.ones((3, 4)).astype(np.float32)
    np.random.seed(0)
    out1 = graphsage_layer(features, adj, weight, num_samples=2)
    np.random.seed(0)
    out2 = graphsage_layer(features, adj, weight, num_samples=2)
    assert np.allclose(out1, out2)


def test_different_output_dims():
    features = np.random.randn(5, 3).astype(np.float32)
    adj = np.eye(5)
    for out_dim in [1, 2, 5, 10]:
        weight = np.random.randn(3, out_dim).astype(np.float32)
        output = graphsage_layer(features, adj, weight, num_samples=2)
        assert output.shape == (5, out_dim)
