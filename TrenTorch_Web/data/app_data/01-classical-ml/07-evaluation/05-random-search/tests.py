"""
pytest data/app_data/01-classical-ml/07-evaluation/05-random-search/tests.py
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from _load import load_solution  # noqa: E402

_module = load_solution(f"01-classical-ml/07-evaluation/{Path(__file__).resolve().parent.name}")
sample_params = _module.sample_params
random_search = _module.random_search


def test_sample_params_discrete_only_picks_from_the_list():
    rng = np.random.default_rng(0)
    spec = {"depth": [2, 3, 4]}
    for _ in range(20):
        params = sample_params(spec, rng)
        assert params["depth"] in [2, 3, 4]


def test_sample_params_continuous_stays_in_range():
    rng = np.random.default_rng(0)
    spec = {"lr": (0.001, 1.0)}
    for _ in range(20):
        params = sample_params(spec, rng)
        assert 0.001 <= params["lr"] <= 1.0


def test_sample_params_continuous_produces_varied_values_not_grid_points():
    rng = np.random.default_rng(0)
    spec = {"lr": (0.0, 1.0)}
    values = [sample_params(spec, rng)["lr"] for _ in range(20)]
    assert len(set(np.round(values, 6).tolist())) > 15  # genuinely varied, not a small fixed set


def test_random_search_returns_n_iter_scores():
    def fit_and_score(params):
        return -abs(params["x"])

    result = random_search({"x": (-1.0, 1.0)}, n_iter=15, fit_and_score_fn=fit_and_score, seed=0)
    assert len(result["all_scores"]) == 15


def test_random_search_is_reproducible_with_the_same_seed():
    def fit_and_score(params):
        return -abs(params["x"] - 0.3)

    result_a = random_search({"x": (-1.0, 1.0)}, n_iter=10, fit_and_score_fn=fit_and_score, seed=7)
    result_b = random_search({"x": (-1.0, 1.0)}, n_iter=10, fit_and_score_fn=fit_and_score, seed=7)
    assert result_a["best_params"] == result_b["best_params"]
    assert result_a["all_scores"] == result_b["all_scores"]


def test_random_search_finds_a_near_optimal_continuous_value():
    # The actual advantage over grid search, demonstrated: with enough
    # random draws over a continuous range, the best found should land
    # close to the true optimum, a value no small fixed grid would
    # necessarily include.
    def fit_and_score(params):
        return -((params["x"] - 0.4231) ** 2)

    result = random_search({"x": (0.0, 1.0)}, n_iter=200, fit_and_score_fn=fit_and_score, seed=1)
    assert abs(result["best_params"]["x"] - 0.4231) < 0.02


def test_rng_is_built_once_not_reseeded_every_iteration():
    # Directly targets a mutant that calls np.random.default_rng(seed)
    # inside the sampling loop instead of once outside it: with a fixed
    # seed, every "random" draw would then be identical, so every
    # sampled continuous value across n_iter would collapse to the
    # exact same number.
    def fit_and_score(_params):
        return 0.0

    result = random_search({"x": (0.0, 1.0)}, n_iter=10, fit_and_score_fn=fit_and_score, seed=3)
    sampled_values = [params["x"] for params, _ in result["all_scores"]]
    assert len(set(sampled_values)) > 1
