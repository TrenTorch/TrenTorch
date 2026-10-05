import numpy as np
from _load import load_solution


_module = load_solution(__file__)
graph_readout = _module.graph_readout


def test_sum_readout():
    features = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
    result = graph_readout(features, 'sum')
    expected = np.array([9, 12], dtype=np.float32)
    assert np.allclose(result, expected)


def test_mean_readout():
    features = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
    result = graph_readout(features, 'mean')
    expected = np.array([3, 4], dtype=np.float32)
    assert np.allclose(result, expected)


def test_max_readout():
    features = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
    result = graph_readout(features, 'max')
    expected = np.array([5, 6], dtype=np.float32)
    assert np.allclose(result, expected)


def test_single_node():
    features = np.array([[1, 2, 3]], dtype=np.float32)
    result_sum = graph_readout(features, 'sum')
    result_mean = graph_readout(features, 'mean')
    result_max = graph_readout(features, 'max')
    assert np.allclose(result_sum, [1, 2, 3])
    assert np.allclose(result_mean, [1, 2, 3])
    assert np.allclose(result_max, [1, 2, 3])


def test_uniform_features():
    features = np.ones((10, 5), dtype=np.float32)
    result_sum = graph_readout(features, 'sum')
    result_mean = graph_readout(features, 'mean')
    assert np.allclose(result_sum, 10.0)
    assert np.allclose(result_mean, 1.0)


def test_different_readout_types():
    features = np.random.randn(8, 4).astype(np.float32)
    sum_result = graph_readout(features, 'sum')
    mean_result = graph_readout(features, 'mean')
    max_result = graph_readout(features, 'max')
    assert sum_result.shape == (4,)
    assert mean_result.shape == (4,)
    assert max_result.shape == (4,)


def test_output_shape():
    for num_nodes in [1, 5, 10, 100]:
        for feature_dim in [1, 2, 5, 10]:
            features = np.random.randn(num_nodes, feature_dim).astype(np.float32)
            for readout_type in ['sum', 'mean', 'max']:
                result = graph_readout(features, readout_type)
                assert result.shape == (feature_dim,)


def test_permutation_invariance():
    features = np.array([[1, 2], [3, 4], [5, 6]], dtype=np.float32)
    perm_features = features[[2, 0, 1]]
    for readout_type in ['sum', 'mean', 'max']:
        result1 = graph_readout(features, readout_type)
        result2 = graph_readout(perm_features, readout_type)
        assert np.allclose(result1, result2)


def test_negative_features():
    features = np.array([[-1, -2], [-3, -4], [-5, -6]], dtype=np.float32)
    result = graph_readout(features, 'sum')
    expected = np.array([-9, -12], dtype=np.float32)
    assert np.allclose(result, expected)


def test_invalid_readout_type():
    features = np.random.randn(5, 3).astype(np.float32)
    try:
        graph_readout(features, 'invalid')
        assert False
    except ValueError:
        pass
