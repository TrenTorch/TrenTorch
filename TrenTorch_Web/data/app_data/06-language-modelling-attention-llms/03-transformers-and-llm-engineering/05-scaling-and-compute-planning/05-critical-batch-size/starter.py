import numpy as np


def gradient_noise_scale(per_example_grads: np.ndarray) -> float:
    """tr(covariance) / ||mean gradient||^2 from per-example gradients."""
    # TODO
    pass


def steps_to_target(batch_size: float, s_min: float, b_crit: float) -> float:
    """S = s_min * (1 + b_crit / batch_size)."""
    # TODO
    pass
