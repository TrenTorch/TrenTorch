import pytest
import numpy as np
from _load import load_solution


_module = load_solution(__file__)
vae_loss = _module.vae_loss


def test_basic_shapes():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = np.random.randn(4, 10).astype(np.float32)
    mu = np.random.randn(4, 5).astype(np.float32)
    logvar = np.random.randn(4, 5).astype(np.float32)
    loss = vae_loss(x_recon, x_true, mu, logvar)
    assert isinstance(loss, (float, np.floating))


def test_perfect_reconstruction():
    x = np.random.randn(4, 10).astype(np.float32)
    mu = np.zeros((4, 5)).astype(np.float32)
    logvar = np.zeros((4, 5)).astype(np.float32)
    loss = vae_loss(x, x, mu, logvar)
    assert loss == pytest.approx(0.0, abs=1e-6)


def test_zero_mu_logvar():
    x_recon = np.ones((2, 8)).astype(np.float32)
    x_true = np.ones((2, 8)).astype(np.float32)
    mu = np.zeros((2, 4)).astype(np.float32)
    logvar = np.zeros((2, 4)).astype(np.float32)
    loss = vae_loss(x_recon, x_true, mu, logvar)
    assert np.isfinite(loss)


def test_different_latent_dims():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = np.random.randn(4, 10).astype(np.float32)
    for latent_dim in [2, 5, 10, 20]:
        mu = np.random.randn(4, latent_dim).astype(np.float32)
        logvar = np.random.randn(4, latent_dim).astype(np.float32)
        loss = vae_loss(x_recon, x_true, mu, logvar)
        assert np.isfinite(loss)


def test_large_reconstruction_error():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = x_recon + 10.0
    mu = np.zeros((4, 5)).astype(np.float32)
    logvar = np.zeros((4, 5)).astype(np.float32)
    loss = vae_loss(x_recon, x_true, mu, logvar)
    assert loss > 50


def test_large_mu_values():
    x_recon = np.ones((2, 8)).astype(np.float32)
    x_true = np.ones((2, 8)).astype(np.float32)
    mu = np.full((2, 4), 5.0).astype(np.float32)
    logvar = np.zeros((2, 4)).astype(np.float32)
    loss = vae_loss(x_recon, x_true, mu, logvar)
    assert loss > 10


def test_large_negative_logvar():
    x_recon = np.ones((2, 8)).astype(np.float32)
    x_true = np.ones((2, 8)).astype(np.float32)
    mu = np.zeros((2, 4)).astype(np.float32)
    logvar = np.full((2, 4), -10.0).astype(np.float32)
    loss = vae_loss(x_recon, x_true, mu, logvar)
    assert np.isfinite(loss)


def test_batch_size_independence():
    x_recon1 = np.random.randn(2, 10).astype(np.float32)
    x_true1 = np.random.randn(2, 10).astype(np.float32)
    mu1 = np.random.randn(2, 5).astype(np.float32)
    logvar1 = np.random.randn(2, 5).astype(np.float32)
    loss1 = vae_loss(x_recon1, x_true1, mu1, logvar1)
    x_recon2 = np.random.randn(8, 10).astype(np.float32)
    x_true2 = np.random.randn(8, 10).astype(np.float32)
    mu2 = np.random.randn(8, 5).astype(np.float32)
    logvar2 = np.random.randn(8, 5).astype(np.float32)
    loss2 = vae_loss(x_recon2, x_true2, mu2, logvar2)
    assert np.isfinite(loss1) and np.isfinite(loss2)


def test_finite_outputs():
    for _ in range(10):
        x_recon = np.random.randn(4, 10).astype(np.float32)
        x_true = np.random.randn(4, 10).astype(np.float32)
        mu = np.random.randn(4, 5).astype(np.float32)
        logvar = np.random.randn(4, 5).astype(np.float32)
        loss = vae_loss(x_recon, x_true, mu, logvar)
        assert np.isfinite(loss)


def test_kl_term_effect():
    x_recon = np.ones((2, 8)).astype(np.float32)
    x_true = np.ones((2, 8)).astype(np.float32)
    mu1 = np.zeros((2, 4)).astype(np.float32)
    logvar1 = np.zeros((2, 4)).astype(np.float32)
    loss1 = vae_loss(x_recon, x_true, mu1, logvar1)
    mu2 = np.full((2, 4), 3.0).astype(np.float32)
    logvar2 = np.zeros((2, 4)).astype(np.float32)
    loss2 = vae_loss(x_recon, x_true, mu2, logvar2)
    assert loss2 > loss1
