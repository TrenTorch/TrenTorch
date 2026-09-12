from typing import Callable

import numpy as np


def sample_params(param_distributions: dict, rng: np.random.Generator) -> dict:
    """
    param_distributions: for each hyperparameter, either a (low, high)
    tuple (sample a continuous value uniformly from that range) or a
    list (sample one value uniformly from the list, for discrete
    choices).

    Returns:
        one randomly-sampled dict of hyperparameter values.
    """
    # TODO: For each key, check if its spec is a tuple (continuous) or
    # a list (discrete), and sample accordingly with rng.
    pass


def random_search(
    param_distributions: dict,
    n_iter: int,
    fit_and_score_fn: Callable[[dict], float],
    seed: int | None = None,
) -> dict:
    """
    Same return shape as 04-grid-search's grid_search:
      {"best_params", "best_score", "all_scores"}
    but samples n_iter random configurations instead of trying every
    combination in a fixed grid.
    """
    # TODO: One rng, built once. Repeat n_iter times: sample_params(),
    # score it, track the best, collect every (params, score) pair.
    pass
