---
name: evaluation-splitting-and-resampling
title: 'Train/test split, k-fold cross-validation, bootstrapping'
tags: [classical-ml, evaluation, resampling]
difficulty: Beginner
---

## Statement

Implement:

```python
def train_test_split(input, labels, test_size, seed=None) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: ...
def k_fold_split(n_samples, k, seed=None) -> list[tuple[np.ndarray, np.ndarray]]: ...
```

- Bootstrapping itself is already implemented, `02-bagging`'s `bootstrap_sample`, reuse it, this question doesn't reimplement it.

## Theory

Every model in this curriculum has been trained and then, implicitly, trusted. Real evaluation needs a principled way to check "does this actually generalize," and there are three standard tools, in increasing order of how much they squeeze out of a fixed amount of data:

**Train/test split**: hold out a fraction of the data, train on the rest, evaluate once on the held-out part. Simple, but wasteful, whatever fraction you hold out never contributes to training, and a single split's result depends on which specific points happened to land in the test set.

**K-fold cross-validation**: split the data into `k` roughly-equal folds, train `k` separate times, each time holding out a different fold as validation and training on the other `k-1`. Every sample gets used for both training (in `k-1` of the folds) and validation (in exactly one fold), and averaging the `k` validation scores gives a much less noisy estimate than one single split would, at the cost of training `k` times instead of once.

**Bootstrapping** (`02-bagging`'s `bootstrap_sample`): resample the data with replacement, the same idea already used to give each tree in a Random Forest a different training set. Applied to evaluation rather than training, running a metric across many bootstrap resamples of the test set gives a distribution of that metric, not just a single number, which is how a confidence interval on a reported accuracy or F1 score gets built.

```text
train/test split:  one split, one train, one evaluation
k-fold CV:          k splits, k trains, k evaluations, averaged
bootstrapping:      many resamples, one thing (evaluate, or, in 02-bagging, train) each time
```

## Explanation

`train_test_split` shuffles every sample index once (`rng.permutation(n_samples)`), then simply slices the shuffled order, the first `round(n_samples * test_size)` indices become the test set, the rest become train, this guarantees no overlap and full coverage by construction (slicing a permutation can't duplicate or drop an index).

`k_fold_split` shuffles indices the same way, then `np.array_split(shuffled_idx, k)` divides them into `k` folds (as close to equal size as `n_samples` and `k` allow, `array_split` handles a remainder gracefully instead of requiring exact divisibility). For each fold `i`, `val_idx` is that fold, and `train_idx` is every _other_ fold concatenated, `np.concatenate([folds[j] for j in range(k) if j != i])`, giving exactly the `k` train/validation pairs Theory describes, one pair per fold acting as the held-out validation set in turn.
