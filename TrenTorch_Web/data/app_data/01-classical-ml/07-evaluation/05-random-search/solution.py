from typing import Callable

import numpy as np


def sample_params(param_distributions: dict, rng: np.random.Generator) -> dict:
    params = {}
    for key, spec in param_distributions.items():
        if isinstance(spec, tuple):
            low, high = spec
            params[key] = rng.uniform(low, high)
        else:
            params[key] = spec[rng.integers(0, len(spec))]
    return params


def random_search(
    param_distributions: dict,
    n_iter: int,
    fit_and_score_fn: Callable[[dict], float],
    seed: int | None = None,
) -> dict:
    rng = np.random.default_rng(seed)

    all_scores = []
    best_params, best_score = None, float("-inf")
    for _ in range(n_iter):
        params = sample_params(param_distributions, rng)
        score = fit_and_score_fn(params)
        all_scores.append((params, score))
        if score > best_score:
            best_score = score
            best_params = params

    return {"best_params": best_params, "best_score": best_score, "all_scores": all_scores}
