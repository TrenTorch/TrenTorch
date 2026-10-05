import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))


def binary_cross_entropy(predictions, targets):
    eps = 1e-7
    predictions = np.clip(predictions, eps, 1 - eps)
    return -np.mean(targets * np.log(predictions) + (1 - targets) * np.log(1 - predictions))


def gan_loss(d_real_logits, d_fake_logits, is_discriminator=True):
    """Compute GAN loss.

    Args:
        d_real_logits: Discriminator logits for real samples, shape (N,).
        d_fake_logits: Discriminator logits for fake samples, shape (N,).
        is_discriminator: If True, compute discriminator loss; else generator loss.

    Returns:
        Scalar loss.
    """
    d_real_probs = sigmoid(d_real_logits)
    d_fake_probs = sigmoid(d_fake_logits)

    if is_discriminator:
        real_loss = binary_cross_entropy(d_real_probs, np.ones_like(d_real_probs))
        fake_loss = binary_cross_entropy(d_fake_probs, np.zeros_like(d_fake_probs))
        return real_loss + fake_loss
    else:
        return binary_cross_entropy(d_fake_probs, np.ones_like(d_fake_probs))
