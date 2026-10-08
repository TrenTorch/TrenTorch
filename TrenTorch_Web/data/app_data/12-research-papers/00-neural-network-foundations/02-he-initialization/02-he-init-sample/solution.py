import numpy as np


def he_init_weights(fan_in, fan_out, rng):
    return rng.normal(0.0, np.sqrt(2.0 / fan_in), size=(fan_out, fan_in))
