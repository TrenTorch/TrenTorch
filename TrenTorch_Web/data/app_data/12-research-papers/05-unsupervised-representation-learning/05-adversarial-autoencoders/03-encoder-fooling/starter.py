import numpy as np


def encoder_fooling_loss(d_codes):
    """
    d_codes: discriminator outputs on encoder codes, in (0, 1)

    Returns:
        -mean(log D(z_encoder)), the encoder's adversarial loss, as a float.
    """
    # TODO: Negate the mean log discriminator output on the encoder's codes (see Theory).
    pass
