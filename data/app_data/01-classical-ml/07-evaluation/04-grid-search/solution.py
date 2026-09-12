import itertools
from typing import Callable


def generate_param_combinations(param_grid: dict[str, list]) -> list[dict]:
    keys = list(param_grid.keys())
    value_lists = [param_grid[key] for key in keys]
    return [dict(zip(keys, values)) for values in itertools.product(*value_lists)]


def grid_search(param_grid: dict[str, list], fit_and_score_fn: Callable[[dict], float]) -> dict:
    combinations = generate_param_combinations(param_grid)

    all_scores = []
    best_params, best_score = None, float("-inf")
    for params in combinations:
        score = fit_and_score_fn(params)
        all_scores.append((params, score))
        if score > best_score:
            best_score = score
            best_params = params

    return {"best_params": best_params, "best_score": best_score, "all_scores": all_scores}
