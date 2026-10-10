import pytest
import numpy as np
from _load import load_solution


_module = load_solution(__file__)
mdn_loss = _module.mdn_loss


def test_shape_mismatch_y():
    y = np.array([1.0, 2.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 1.0]])
    sigma = np.array([[1.0, 1.0]])
    try:
        mdn_loss(y, pi, mu, sigma)
        assert False
    except ValueError:
        pass


def test_shape_mismatch_components():
    y = np.array([1.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0]])
    sigma = np.array([[1.0, 1.0]])
    try:
        mdn_loss(y, pi, mu, sigma)
        assert False
    except ValueError:
        pass


def test_negative_sigma():
    y = np.array([1.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 1.0]])
    sigma = np.array([[-1.0, 1.0]])
    try:
        mdn_loss(y, pi, mu, sigma)
        assert False
    except ValueError:
        pass


def test_single_gaussian():
    y = np.array([0.0])
    pi = np.array([[1.0]])
    mu = np.array([[0.0]])
    sigma = np.array([[1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    expected = -np.log(1.0 / np.sqrt(2.0 * np.pi))
    np.testing.assert_allclose(loss, expected, atol=1e-6)


def test_mixture_two_gaussians():
    y = np.array([0.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 0.0]])
    sigma = np.array([[1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss > 0.0


def test_perfect_prediction():
    y = np.array([0.0])
    pi = np.array([[1.0, 0.0]])
    mu = np.array([[0.0, 10.0]])
    sigma = np.array([[0.1, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss == pytest.approx(-np.log(1.0 / (0.1 * np.sqrt(2 * np.pi))))


def test_batch():
    y = np.array([0.0, 1.0, 2.0])
    pi = np.array([[0.5, 0.5], [0.3, 0.7], [0.6, 0.4]])
    mu = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
    sigma = np.array([[1.0, 1.0], [1.0, 1.0], [1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss > 0.0


def test_many_components():
    y = np.array([0.5])
    pi = np.array([[0.2, 0.2, 0.2, 0.2, 0.2]])
    mu = np.array([[0.0, 1.0, 2.0, 3.0, 4.0]])
    sigma = np.array([[1.0, 1.0, 1.0, 1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss > 0.0


def test_off_distribution():
    y = np.array([100.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 1.0]])
    sigma = np.array([[1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert loss > 10.0


def test_on_distribution():
    y = np.array([0.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 1.0]])
    sigma = np.array([[1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert loss < 5.0


def test_scalar_input_broadcast():
    y = 0.0
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 1.0]])
    sigma = np.array([[1.0, 1.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)


def test_large_variance():
    y = np.array([0.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 0.0]])
    sigma = np.array([[10.0, 10.0]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss > 0.0


def test_small_variance():
    y = np.array([0.0])
    pi = np.array([[0.5, 0.5]])
    mu = np.array([[0.0, 0.0]])
    sigma = np.array([[0.01, 0.01]])
    loss = mdn_loss(y, pi, mu, sigma)
    assert np.isfinite(loss)
    assert loss == pytest.approx(-np.log(1.0 / (0.01 * np.sqrt(2 * np.pi))))
