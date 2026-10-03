import numpy as np


def cfg_combine(eps_uncond: np.ndarray, eps_cond: np.ndarray, w: float) -> np.ndarray:
    """eps_uncond + w * (eps_cond - eps_uncond)."""
    # TODO
    pass


def drop_condition(cond_ids: np.ndarray, p: float, null_id: int, rng: np.random.RandomState) -> np.ndarray:
    """Replace each condition by null_id with probability p using one rng.random_sample call."""
    # TODO
    pass
