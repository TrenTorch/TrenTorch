---
name: evaluation-nested-cross-validation
title: 'Nested cross-validation, and why plain CV leaks hyperparameter choices'
tags: [classical-ml, evaluation, cross-validation]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A very natural-looking but genuinely wrong pattern: run `04-grid-search`'s `grid_search` with k-fold CV as the scoring function, over the _whole_ dataset, then report that search's `best_score` as "how good this model is." This leaks information: the grid search tried many hyperparameter combinations and kept whichever one scored best on those _exact_ CV folds, so the reported number is optimistically biased — some hyperparameter combination will look good on any particular set of folds purely by chance, especially with a large grid or a small dataset, and reporting the max over many attempts is exactly what "selection bias" means.

### From theory to code

Implement `nested_cross_validation(input, labels, param_grid, k_outer, k_inner, train_and_predict_fn, score_fn, seed=None)`. Reuse `01-splitting-and-resampling`'s `k_fold_split` and `04-grid-search`'s `grid_search`. `train_and_predict_fn(params, train_input, train_labels, test_input) -> predictions`, `score_fn(labels, predictions) -> float`.

### Constraints

- Returns a list of `k_outer` scores, one per outer fold.
- Hyperparameter selection (the inner loop) must only ever see the outer fold's _training_ portion — never the outer test fold.
- Each outer fold: select hyperparameters via an inner k-fold search on the outer training data, retrain once on the _entire_ outer training fold with those hyperparameters, then evaluate exactly once on the outer test fold.
- `seed` controls both the outer and inner splits' reproducibility.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The inner `k_fold_split` must run on `outer_train_input`/`outer_train_labels` — the outer training fold only — never on the full dataset. That's the entire difference between this and the naive, leaky approach.

</details>

<details>
<summary>Hint 2</summary>

`grid_search(param_grid, fit_and_score)["best_params"]` where `fit_and_score` is a closure over that outer fold's training data, running its own inner CV loop and returning the mean inner score — this reuses `04-grid-search` unmodified, just fed a fold-scoped scoring function.

</details>

## Theory

### The simple version

The tell: with pure random-noise data (features genuinely unrelated to the labels), the naive whole-dataset-grid-search approach still reports an accuracy noticeably above chance, not because any hyperparameter is actually good, but because trying many options and keeping the best one _always_ finds something that got lucky on the specific folds used for both selecting and reporting.

### The formula

**Nested cross-validation** fixes this by keeping selection and evaluation on genuinely separate data:

```text
outer loop (k_outer folds): held out purely for HONEST evaluation, never touched by hyperparameter selection
    inner loop (k_inner folds, within the outer TRAINING data only): select the best hyperparameters here
    retrain on the full outer training fold with those hyperparameters
    evaluate ONCE on the outer test fold (data the inner loop never saw)
```

The inner loop is free to overfit its own folds while picking hyperparameters — that's the price of any hyperparameter search. But the outer loop's score is computed on data that had zero influence on which hyperparameters got chosen, so it can't inherit that same optimism. Averaging the `k_outer` outer scores gives an honest estimate of how the whole procedure (search + train) would perform on genuinely new data.

### How PyTorch actually implements this

Context only, untested by your submission: this is a general model-evaluation methodology, not a PyTorch operation — scikit-learn's documentation describes this exact pattern as `cross_val_score` wrapped around a `GridSearchCV`, and it applies identically to a PyTorch training loop swapped in as `train_and_predict_fn`.

## Explanation

`nested_cross_validation` splits `input`/`labels` into `k_outer` folds via `k_fold_split`. For each outer fold, `fit_and_score(params)` (a closure capturing that fold's own training data) runs a _second_, inner `k_fold_split` on only the outer training portion, evaluating `train_and_predict_fn` on each inner split and averaging the `k_inner` scores — this is what `grid_search` optimizes over, so hyperparameter selection only ever sees the outer training fold.

`grid_search(param_grid, fit_and_score)["best_params"]` picks the winning hyperparameters using only that inner information. Then `train_and_predict_fn` is called once more, trained on the _entire_ outer training fold (not just one inner split) with those chosen hyperparameters, and evaluated on the outer test fold — data that played no role in either the inner selection or this final retraining's hyperparameter choice. `score_fn` on that prediction is the one honest number for this outer fold, and the list of all `k_outer` such numbers is what the function returns; the caller averages them for a single overall estimate.
