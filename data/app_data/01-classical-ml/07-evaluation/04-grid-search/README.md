---
name: evaluation-grid-search
title: 'Grid search over a hyperparameter grid'
tags: [classical-ml, evaluation, hyperparameter-tuning]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`03-bias-variance-tradeoff` shows that a model's complexity — its hyperparameters — controls where it lands on the bias/variance tradeoff, and that neither extreme wins. But nothing so far in this curriculum has picked those hyperparameters systematically; `learning_rate`, `max_depth`, `n_trees`, `lam` have all been chosen by hand, by the person writing the training call, not discovered from the data.

The most literal fix: define a small set of candidate values for each hyperparameter, actually try *every combination* of them by training and validating a real model for each one, and keep whichever combination scored best. No cleverness, no assumptions about which hyperparameters matter more — just brute-force coverage of a defined search space.

### From theory to code

Implement `generate_param_combinations(param_grid)` to enumerate every combination, then `grid_search(param_grid, fit_and_score_fn)` to score each one and track the winner. `fit_and_score_fn` is a black box supplied by the caller — it trains a model with one specific set of hyperparameters and returns a validation score, higher is better; this question doesn't care what model it is, just how to search over its hyperparameters.

### Constraints

- `param_grid`: a dict mapping each hyperparameter name to a list of candidate values.
- `generate_param_combinations` returns a list of dicts, one per combination — the Cartesian product of every hyperparameter's candidate values, e.g. `{"lr": [0.01, 0.1], "depth": [2, 3]}` produces 4 combinations.
- The number of combinations returned must equal the product of each hyperparameter's candidate-list length.
- `grid_search` returns a dict with `"best_params"` (the params dict that scored highest), `"best_score"` (that score), and `"all_scores"` (a list of `(params, score)` for every combination tried, in the order tried).
- Ties aside, the combination with the strictly highest score wins — never the lowest.
- `fit_and_score_fn` is called exactly once per combination.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The standard library already has a Cartesian product: `itertools.product(*value_lists)` over `param_grid`'s values, one list per hyperparameter.

</details>

<details>
<summary>Hint 2</summary>

Each tuple `itertools.product` yields needs to become a dict again — `dict(zip(keys, values))` pairs it back up with `param_grid`'s original keys, in the same order they were passed to `product`.

</details>

## Theory

### The simple version

Picture choosing a recipe by trying every combination of oven temperature and bake time from a short list of each — 3 temperatures times 2 times is 6 actual bakes, no guessing. Grid search does exactly this for hyperparameters: lay out a short list of candidates per knob, bake (train + validate) once per combination, and keep the best result.

### The formula

```text
param_grid = {"lr": [0.01, 0.1, 1.0], "depth": [2, 3]}
   |  every combination (Cartesian product)
(lr=0.01, depth=2), (lr=0.01, depth=3), (lr=0.1, depth=2), (lr=0.1, depth=3), (lr=1.0, depth=2), (lr=1.0, depth=3)
   |  fit_and_score_fn on each
6 scores
   |  keep the best
```

The combination count multiplies across hyperparameters: 3 learning rates times 2 depths is 6 combinations here; 3 hyperparameters with 5 values each is 125. This exhaustiveness is grid search's whole appeal — it genuinely checks everything in the grid — and its whole cost, since that number grows fast, exactly the tradeoff `05-random-search`, the next question in this track, addresses differently.

### How PyTorch actually implements this

Context only, untested by your submission: hyperparameter search sits outside a model's forward pass entirely, so there's no `torch.nn` equivalent. `itertools.product` is the same combinatorial tool `sklearn.model_selection.GridSearchCV` uses internally to enumerate a `param_grid`.

## Explanation

`generate_param_combinations` pulls `keys = list(param_grid.keys())` and the matching `value_lists`, then `itertools.product(*value_lists)` — the standard library's Cartesian product — walks every combination. `dict(zip(keys, values))` pairs each resulting tuple back up with the original hyperparameter names, turning a tuple like `(0.01, 2)` into `{"lr": 0.01, "depth": 2}`.

`grid_search` calls `generate_param_combinations(param_grid)` once, then loops over the result, calling `fit_and_score_fn` once per combination. It tracks the running best with a plain comparison (`if score > best_score: best_score, best_params = score, params`) — strictly greater, so the first combination to reach a given score wins ties, and a mutant that flipped this to `<` would keep the *worst* combination instead, which is exactly what `test_grid_search_picks_the_maximum_not_the_minimum` checks against. Every `(params, score)` pair is also appended to `all_scores` along the way, so the caller can inspect the full grid's results, not just the winner — useful for plotting or sanity-checking that the search actually explored a reasonable range.
