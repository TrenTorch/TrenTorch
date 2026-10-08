import numpy as np


def gan_generator_loss(d_fake):
    d_fake = np.asarray(d_fake, dtype=float)
    return float(-np.mean(np.log(d_fake)))
