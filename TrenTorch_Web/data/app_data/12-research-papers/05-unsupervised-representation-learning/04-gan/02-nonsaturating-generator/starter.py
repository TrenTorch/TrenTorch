import numpy as np


def gan_generator_loss(d_fake):
    """
    d_fake: discriminator outputs on generated samples, in (0, 1)

    Returns:
        The non-saturating generator loss -mean(log D(G(z))), as a float.
    """
    # TODO: Negate the mean log discriminator output on generated samples (see Theory).
    pass
