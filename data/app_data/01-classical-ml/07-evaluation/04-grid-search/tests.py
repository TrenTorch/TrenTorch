"""
pytest data/app_data/01-classical-ml/07-evaluation/04-grid-search/tests.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
generate_param_combinations = _module.generate_param_combinations
grid_search = _module.grid_search


def test_generate_param_combinations_matches_hand_computation():
    grid = {"a": [1, 2], "b": [10, 20]}
    result = generate_param_combinations(grid)
    expected = [
        {"a": 1, "b": 10},
        {"a": 1, "b": 20},
        {"a": 2, "b": 10},
        {"a": 2, "b": 20},
    ]
    assert result == expected


def test_generate_param_combinations_single_hyperparameter():
    grid = {"x": [1, 2, 3]}
    result = generate_param_combinations(grid)
    assert result == [{"x": 1}, {"x": 2}, {"x": 3}]


def test_generate_param_combinations_count_multiplies_across_hyperparameters():
    grid = {"a": [1, 2, 3], "b": [10, 20], "c": [100]}
    result = generate_param_combinations(grid)
    assert len(result) == 3 * 2 * 1


def test_grid_search_finds_the_actual_best_combination():
    grid = {"x": [1, 5, 9, 20]}

    def fit_and_score(params):
        return -((params["x"] - 5) ** 2)  # best score (0) at x=5

    result = grid_search(grid, fit_and_score)
    assert result["best_params"] == {"x": 5}
    assert result["best_score"] == 0


def test_grid_search_all_scores_covers_every_combination_exactly_once():
    grid = {"a": [1, 2], "b": [10, 20]}
    call_log = []

    def fit_and_score(params):
        call_log.append(params)
        return params["a"] + params["b"]

    result = grid_search(grid, fit_and_score)
    assert len(result["all_scores"]) == 4
    assert len(call_log) == 4
    scored_params = [params for params, _ in result["all_scores"]]
    for combo in generate_param_combinations(grid):
        assert combo in scored_params


def test_grid_search_picks_the_maximum_not_the_minimum():
    # Directly targets a mutant that keeps the WORST score instead of
    # the best (e.g. a flipped comparison): a grid with a clear single
    # maximum must have that one selected, not one of the lower ones.
    grid = {"x": [1, 2, 3]}

    def fit_and_score(params):
        return {1: 0.1, 2: 0.9, 3: 0.5}[params["x"]]

    result = grid_search(grid, fit_and_score)
    assert result["best_params"] == {"x": 2}
    assert result["best_score"] == 0.9
