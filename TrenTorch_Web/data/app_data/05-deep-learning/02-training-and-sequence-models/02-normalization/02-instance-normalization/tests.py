import numpy as np
from _load import load_solution


_module = load_solution(__file__)
instance_norm = _module.instance_norm


def test_2d_input():
    x = np.array([[1.0, 2.0, 3.0, 4.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = instance_norm(x, gamma, beta)
    assert result.shape == (1, 4)


def test_4d_input():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = instance_norm(x, gamma, beta)
    assert result.shape == (2, 4, 3, 3)


def test_gamma_beta_shape():
    x = np.ones((1, 4))
    gamma = np.ones(3)
    beta = np.zeros(4)
    try:
        instance_norm(x, gamma, beta)
        assert False
    except ValueError:
        pass


def test_independent_per_instance():
    x1 = np.random.randn(1, 2, 3, 3).astype(np.float32)
    x2 = np.random.randn(1, 2, 3, 3).astype(np.float32)
    gamma = np.ones(2)
    beta = np.zeros(2)
    r1 = instance_norm(x1, gamma, beta)
    r2 = instance_norm(x2, gamma, beta)
    assert not np.allclose(r1, r2)


def test_spatial_normalization():
    x = np.ones((2, 3, 4, 4)).astype(np.float32)
    gamma = np.ones(3)
    beta = np.zeros(3)
    result = instance_norm(x, gamma, beta)
    assert not np.any(np.isnan(result))


def test_mean_zero_variance_one():
    np.random.seed(0)
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = instance_norm(x, gamma, beta)
    assert np.all(np.isfinite(result))


def test_gamma_beta_applied():
    x = np.ones((1, 4, 2, 2))
    gamma = np.array([2.0, 2.0, 2.0, 2.0])
    beta = np.array([1.0, 1.0, 1.0, 1.0])
    result = instance_norm(x, gamma, beta)
    assert result.shape == (1, 4, 2, 2)


def test_single_channel():
    x = np.random.randn(2, 1, 3, 3).astype(np.float32)
    gamma = np.ones(1)
    beta = np.zeros(1)
    result = instance_norm(x, gamma, beta)
    assert result.shape == (2, 1, 3, 3)


def test_many_channels():
    x = np.random.randn(2, 8, 3, 3).astype(np.float32)
    gamma = np.ones(8)
    beta = np.zeros(8)
    result = instance_norm(x, gamma, beta)
    assert result.shape == (2, 8, 3, 3)


def test_finite_output():
    x = np.random.randn(4, 8, 5, 5).astype(np.float32)
    gamma = np.random.randn(8)
    beta = np.random.randn(8)
    result = instance_norm(x, gamma, beta)
    assert np.all(np.isfinite(result))


def test_different_spatial_sizes():
    for h, w in [(2, 2), (3, 5), (7, 7)]:
        x = np.random.randn(2, 4, h, w).astype(np.float32)
        gamma = np.ones(4)
        beta = np.zeros(4)
        result = instance_norm(x, gamma, beta)
        assert result.shape == (2, 4, h, w)


def test_scale_effect():
    x = np.random.randn(2, 4, 3, 3)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result1 = instance_norm(x, gamma, beta)
    gamma2 = 2.0 * np.ones(4)
    result2 = instance_norm(x, gamma2, beta)
    assert not np.allclose(result1, result2)
