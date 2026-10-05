import numpy as np


def gan_discriminator_loss(d_real, d_fake):
    """
    d_real: discriminator outputs on real samples, in (0, 1)
    d_fake: discriminator outputs on generated samples, in (0, 1)

    Returns:
        -mean(log D(x)) - mean(log(1 - D(G(z)))), as a float.
    """
    # TODO: Apply the two binary cross-entropy terms from Theory.
    pass
