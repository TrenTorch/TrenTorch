---
name: ensembles-stacking-oof
title: 'Stacking with out-of-fold predictions'
tags: [classical-ml, supervised, ensembles, stacking, cross-validation]
difficulty: Advanced
---

## Statement

### Learn how much to trust each model

Stacking trains several base models, then learns how to combine their predictions. The meta-learner must see predictions on data the base models did not train on, otherwise it learns to trust whichever model overfit the most.

Implement two functions.

**`oof_predictions(model_fn, X, y, n_splits=3)`** returns an array of length `n` with out-of-fold predictions. Split the rows into `n_splits` contiguous blocks with no shuffling. For each block, call `model_fn(X_train, y_train, X_block)` on the other blocks, and store the result at the block's positions.

**`stacking_weights(P, y)`** takes `P` of shape `(n, m)`, where each column is one base model's out-of-fold predictions, and returns the least-squares weights `w` of length `m` with no intercept, so that `P @ w` best matches `y`.

### Constraints

- `2 ≤ n_splits ≤ n`, otherwise raise `ValueError`.
- `P` must have as many rows as `y`, otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.array_split(np.arange(n), n_splits)` to get the contiguous blocks.

</details>

<details>
<summary>Hint 2</summary>

`np.linalg.lstsq(P, y, rcond=None)[0]` gives the weights.

</details>

## Theory

If the base models' out-of-fold predictions are honest, the least-squares weights measure how useful each model is on new data. A model that is just noise gets a weight near zero, and a model that matches the target gets weight near one.

## Explanation

`oof_predictions` assigns each block predictions from a model fit on everything else. `stacking_weights` solves the linear meta problem in one `lstsq` call, which keeps the meta-learner as simple as possible.
