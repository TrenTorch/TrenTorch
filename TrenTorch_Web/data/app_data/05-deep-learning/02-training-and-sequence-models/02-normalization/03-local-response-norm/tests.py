import numpy as np
from _load import load_solution


_module = load_solution(__file__)
local_response_norm = _module.local_response_norm


def test_basic_shape():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    result = local_response_norm(x)
    assert result.shape == x.shape


def test_invalid_k():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    try:
        local_response_norm(x, k=-1.0)
        assert False
    except ValueError:
        pass


def test_invalid_alpha():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    try:
        local_response_norm(x, alpha=-1e-4)
        assert False
    except ValueError:
        pass


def test_invalid_beta():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    try:
        local_response_norm(x, beta=-0.75)
        assert False
    except ValueError:
        pass


def test_invalid_n():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    try:
        local_response_norm(x, n=-5)
        assert False
    except ValueError:
        pass


def test_finite_output():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    result = local_response_norm(x)
    assert np.all(np.isfinite(result))


def test_different_neighborhood_sizes():
    x = np.random.randn(2, 8, 3, 3).astype(np.float32)
    for n in [1, 3, 5, 7]:
        result = local_response_norm(x, n=n)
        assert result.shape == x.shape


def test_different_alpha_values():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    r1 = local_response_norm(x, alpha=1e-4)
    r2 = local_response_norm(x, alpha=1e-3)
    assert not np.allclose(r1, r2)


def test_different_beta_values():
    x = np.random.randn(2, 4, 3, 3).astype(np.float32)
    r1 = local_response_norm(x, beta=0.5)
    r2 = local_response_norm(x, beta=0.75)
    assert not np.allclose(r1, r2)


def test_large_batch():
    x = np.random.randn(8, 16, 5, 5).astype(np.float32)
    result = local_response_norm(x)
    assert result.shape == x.shape
    assert np.all(np.isfinite(result))


def test_single_channel():
    x = np.random.randn(2, 1, 3, 3).astype(np.float32)
    result = local_response_norm(x)
    assert result.shape == (2, 1, 3, 3)


def test_zero_input():
    x = np.zeros((2, 4, 3, 3)).astype(np.float32)
    result = local_response_norm(x)
    assert np.allclose(result, 0.0)


def test_ones_normalization():
    x = np.ones((2, 4, 3, 3)).astype(np.float32)
    result = local_response_norm(x, k=1.0, alpha=0.1, beta=0.5, n=3)
    assert result.shape == (2, 4, 3, 3)
    assert np.all(np.isfinite(result))
