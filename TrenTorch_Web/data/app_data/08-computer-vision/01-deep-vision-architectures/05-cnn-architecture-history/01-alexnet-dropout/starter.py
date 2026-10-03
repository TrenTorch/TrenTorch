import numpy as np


def dropout_forward(x: np.ndarray, p: float, rng: np.random.Generator) -> np.ndarray:
    """
    x: any-shape array of activations
    p: probability of dropping (zeroing) any given unit, in [0, 1)
    rng: a numpy random Generator, used so tests can control randomness

    "Inverted" dropout: randomly zero each unit independently with
    probability p, and scale every SURVIVING unit by 1 / (1 - p) so the
    expected value of the output equals the input, both during training
    (with dropout active) and at inference (where dropout is simply
    turned off).
    """
    # TODO: draw a random (0, 1) value per element of x with rng.random,
    # keep the element (mask = 1) where that value is >= p, zero it
    # otherwise, then divide the whole result by (1 - p).
    pass
