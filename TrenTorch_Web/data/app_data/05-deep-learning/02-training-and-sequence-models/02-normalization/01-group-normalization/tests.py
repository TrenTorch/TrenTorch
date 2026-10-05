import numpy as np
from _load import load_solution


_module = load_solution(__file__)
group_norm = _module.group_norm


def test_2d_input():
    x = np.array([[1.0, 2.0, 3.0, 4.0]])
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
    assert result.shape == (1, 4)


def test_4d_input():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
    assert result.shape == (2, 4, 3, 3)


def test_invalid_num_groups():
    x = np.ones((1, 4))
    gamma = np.ones(4)
    beta = np.zeros(4)
    try:
        group_norm(x, num_groups=3, gamma=gamma, beta=beta)
        assert False
    except ValueError:
        pass


def test_gamma_beta_shape():
    x = np.ones((1, 4))
    gamma = np.ones(3)
    beta = np.zeros(4)
    try:
        group_norm(x, num_groups=2, gamma=gamma, beta=beta)
        assert False
    except ValueError:
        pass


def test_mean_zero_variance_one():
    np.random.seed(0)
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
    assert not np.any(np.isnan(result))


def test_gamma_beta_applied():
    x = np.ones((1, 4))
    gamma = np.array([2.0, 2.0, 2.0, 2.0])
    beta = np.array([1.0, 1.0, 1.0, 1.0])
    result = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
    assert result.shape == (1, 4)


def test_single_group():
    x = np.random.randn(2, 4).astype(np.float32)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result = group_norm(x, num_groups=1, gamma=gamma, beta=beta)
    assert result.shape == (2, 4)


def test_many_groups():
    x = np.random.randn(2, 8).astype(np.float32)
    gamma = np.ones(8)
    beta = np.zeros(8)
    result = group_norm(x, num_groups=8, gamma=gamma, beta=beta)
    assert result.shape == (2, 8)


def test_finite_output():
    x = np.random.randn(4, 8, 5, 5).astype(np.float32)
    gamma = np.random.randn(8)
    beta = np.random.randn(8)
    result = group_norm(x, num_groups=4, gamma=gamma, beta=beta)
    assert np.all(np.isfinite(result))


def test_different_batch_sizes():
    for batch_size in [1, 2, 4]:
        x = np.random.randn(batch_size, 4, 3, 3).astype(np.float32)
        gamma = np.ones(4)
        beta = np.zeros(4)
        result = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
        assert result.shape == (batch_size, 4, 3, 3)


def test_scale_effect():
    x = np.random.randn(2, 4)
    gamma = np.ones(4)
    beta = np.zeros(4)
    result1 = group_norm(x, num_groups=2, gamma=gamma, beta=beta)
    gamma2 = 2.0 * np.ones(4)
    result2 = group_norm(x, num_groups=2, gamma=gamma2, beta=beta)
    assert not np.allclose(result1, result2)
