import numpy as np


def gan_loss(d_real_logits, d_fake_logits, is_discriminator=True):
    """Compute GAN loss.

    Args:
        d_real_logits: Discriminator logits for real samples, shape (N,).
        d_fake_logits: Discriminator logits for fake samples, shape (N,).
        is_discriminator: If True, compute discriminator loss; else generator loss.

    Returns:
        Scalar loss.
    """
    pass
