from typing import Callable


def generate_param_combinations(param_grid: dict[str, list]) -> list[dict]:
    """
    param_grid: e.g. {"lr": [0.01, 0.1], "depth": [2, 3]}

    Returns:
        every combination as a dict, e.g.
        [{"lr": 0.01, "depth": 2}, {"lr": 0.01, "depth": 3},
         {"lr": 0.1, "depth": 2}, {"lr": 0.1, "depth": 3}]
        (the Cartesian product of every hyperparameter's candidate values)
    """
    # TODO: itertools.product over param_grid's values, zipped back up
    # with param_grid's keys into a dict per combination.
    pass


def grid_search(param_grid: dict[str, list], fit_and_score_fn: Callable[[dict], float]) -> dict:
    """
    fit_and_score_fn(params: dict) -> float: trains a model with these
    hyperparameters and returns a validation score (higher is better).

    Returns a dict:
      "best_params": the params dict that scored highest
      "best_score": that score
      "all_scores": list of (params, score) for every combination tried
    """
    # TODO: generate_param_combinations(), call fit_and_score_fn on
    # every combination, track the best score and its params, collect
    # every (params, score) pair along the way.
    pass
