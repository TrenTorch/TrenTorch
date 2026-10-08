import numpy as np


def gan_discriminator_loss(d_real, d_fake):
    d_real = np.asarray(d_real, dtype=float)
    d_fake = np.asarray(d_fake, dtype=float)
    return float(-np.mean(np.log(d_real)) - np.mean(np.log(1 - d_fake)))
