import numpy as np
from _load import load_solution


_module = load_solution(__file__)
vq_vae_loss = _module.vq_vae_loss


def test_basic_shape():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = np.random.randn(4, 10).astype(np.float32)
    z_e = np.random.randn(4, 5).astype(np.float32)
    z_q = np.random.randn(4, 5).astype(np.float32)
    loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
    assert isinstance(loss, (float, np.floating))


def test_perfect_reconstruction():
    x = np.random.randn(4, 10).astype(np.float32)
    z = np.random.randn(4, 5).astype(np.float32)
    loss = vq_vae_loss(x, x, z, z)
    assert loss >= 0


def test_default_beta():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = np.random.randn(4, 10).astype(np.float32)
    z_e = np.random.randn(4, 5).astype(np.float32)
    z_q = np.random.randn(4, 5).astype(np.float32)
    loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
    assert np.isfinite(loss)


def test_different_beta_values():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = np.random.randn(4, 10).astype(np.float32)
    z_e = np.random.randn(4, 5).astype(np.float32)
    z_q = np.random.randn(4, 5).astype(np.float32)
    loss1 = vq_vae_loss(x_recon, x_true, z_e, z_q, beta=0.1)
    loss2 = vq_vae_loss(x_recon, x_true, z_e, z_q, beta=1.0)
    assert loss1 != loss2


def test_zero_beta():
    x_recon = np.ones((4, 10)).astype(np.float32)
    x_true = np.ones((4, 10)).astype(np.float32)
    z_e = np.random.randn(4, 5).astype(np.float32)
    z_q = np.random.randn(4, 5).astype(np.float32)
    loss = vq_vae_loss(x_recon, x_true, z_e, z_q, beta=0.0)
    assert loss >= 0


def test_large_reconstruction_error():
    x_recon = np.random.randn(4, 10).astype(np.float32)
    x_true = x_recon + 10.0
    z_e = np.random.randn(4, 5).astype(np.float32)
    z_q = np.random.randn(4, 5).astype(np.float32)
    loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
    assert loss > 50


def test_large_quantization_error():
    x_recon = np.ones((4, 10)).astype(np.float32)
    x_true = np.ones((4, 10)).astype(np.float32)
    z_e = np.full((4, 5), 10.0).astype(np.float32)
    z_q = np.full((4, 5), -10.0).astype(np.float32)
    loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
    assert loss > 100


def test_batch_size_independence():
    for batch_size in [1, 2, 4, 8]:
        x_recon = np.random.randn(batch_size, 10).astype(np.float32)
        x_true = np.random.randn(batch_size, 10).astype(np.float32)
        z_e = np.random.randn(batch_size, 5).astype(np.float32)
        z_q = np.random.randn(batch_size, 5).astype(np.float32)
        loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
        assert np.isfinite(loss)


def test_finite_outputs():
    for _ in range(10):
        x_recon = np.random.randn(4, 10).astype(np.float32)
        x_true = np.random.randn(4, 10).astype(np.float32)
        z_e = np.random.randn(4, 5).astype(np.float32)
        z_q = np.random.randn(4, 5).astype(np.float32)
        loss = vq_vae_loss(x_recon, x_true, z_e, z_q)
        assert np.isfinite(loss)
