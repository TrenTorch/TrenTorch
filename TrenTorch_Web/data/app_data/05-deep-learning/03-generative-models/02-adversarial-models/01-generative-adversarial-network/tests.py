import numpy as np
from _load import load_solution


_module = load_solution(__file__)
gan_loss = _module.gan_loss


def test_discriminator_loss():
    d_real_logits = np.array([5.0, 5.0, 5.0])
    d_fake_logits = np.array([-5.0, -5.0, -5.0])
    loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
    assert np.isfinite(loss) and loss < 1.0


def test_generator_loss():
    d_fake_logits = np.array([5.0, 5.0, 5.0])
    d_real_logits = np.array([0.0, 0.0, 0.0])
    loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert np.isfinite(loss) and loss < 1.0


def test_bad_discriminator():
    d_real_logits = np.array([-5.0, -5.0, -5.0])
    d_fake_logits = np.array([5.0, 5.0, 5.0])
    loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
    assert loss > 2.0


def test_good_generator():
    d_real_logits = np.array([0.0, 0.0, 0.0])
    d_fake_logits = np.array([5.0, 5.0, 5.0])
    loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert loss < 0.1


def test_bad_generator():
    d_real_logits = np.array([0.0, 0.0, 0.0])
    d_fake_logits = np.array([-5.0, -5.0, -5.0])
    loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert loss > 5.0


def test_different_batch_sizes():
    for batch_size in [1, 4, 8, 16]:
        d_real_logits = np.random.randn(batch_size)
        d_fake_logits = np.random.randn(batch_size)
        disc_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
        gen_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
        assert np.isfinite(disc_loss) and np.isfinite(gen_loss)


def test_finite_outputs():
    for _ in range(10):
        d_real_logits = np.random.randn(8) * 10
        d_fake_logits = np.random.randn(8) * 10
        disc_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
        gen_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
        assert np.isfinite(disc_loss) and np.isfinite(gen_loss)


def test_loss_bounds():
    d_real_logits = np.random.randn(8)
    d_fake_logits = np.random.randn(8)
    disc_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
    gen_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert 0 <= disc_loss <= 10
    assert 0 <= gen_loss <= 10


def test_equilibrium_state():
    d_real_logits = np.zeros(8)
    d_fake_logits = np.zeros(8)
    disc_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
    gen_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert np.isfinite(disc_loss) and np.isfinite(gen_loss)


def test_discriminator_vs_generator():
    d_real_logits = np.array([2.0, 2.0, 2.0])
    d_fake_logits = np.array([-2.0, -2.0, -2.0])
    disc_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=True)
    gen_loss = gan_loss(d_real_logits, d_fake_logits, is_discriminator=False)
    assert gen_loss > disc_loss
