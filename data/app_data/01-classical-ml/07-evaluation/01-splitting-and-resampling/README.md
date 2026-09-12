---
name: evaluation-splitting-and-resampling
title: 'Train/test split, k-fold cross-validation, bootstrapping'
tags: [classical-ml, evaluation, resampling]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every model trained so far in this curriculum has been trained and then, implicitly, trusted. But a model that memorizes its training set can report a perfect training score while being useless on anything new. Before a score means anything, the data used to compute it has to be data the model never touched during training.

The simplest way to guarantee that: cut the dataset into two disjoint pieces before training ever starts, one for fitting the model, one held back purely for judging it. That's a train/test split, and it's the foundation every fancier evaluation scheme in this track builds on.

### From theory to code

Implement `train_test_split(input, labels, test_size, seed=None)` and `k_fold_split(n_samples, k, seed=None)`. Both rely on the same primitive: shuffle sample indices once, then partition the shuffled order into the pieces each function needs.

### Constraints

- `train_test_split` returns `(train_input, test_input, train_labels, test_labels)`.
- `test_size` is a fraction of samples (`0` to `1`) to hold out as the test set; the test set size is `round(n_samples * test_size)`.
- Train and test sets must be disjoint and together cover every original index exactly once.
- `input[i]` and `labels[i]` must stay paired after the split.
- Same `seed` must reproduce the exact same split.
- `k_fold_split` returns a list of `k` `(train_idx, val_idx)` pairs, one per fold acting as validation.
- Every index `0..n_samples-1` appears in exactly one fold's `val_idx` across the `k` pairs.
- Within a pair, `train_idx` and `val_idx` are disjoint and together cover every index.
- Folds must be as close to equal size as `n_samples` and `k` allow, even when `k` doesn't evenly divide `n_samples`.
- No fabricated bootstrapping here — `02-bagging`'s `bootstrap_sample` already implements it; this question doesn't reimplement it.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Both functions start the same way: shuffle indices once with `rng.permutation(n_samples)`. Everything after that is just slicing or grouping that one shuffled array — never re-shuffling per fold.

</details>

<details>
<summary>Hint 2</summary>

For `k_fold_split`, `np.array_split(shuffled_idx, k)` handles an uneven `n_samples / k` for you. For fold `i`, the validation set is `folds[i]`; the training set is every *other* fold concatenated together.

</details>

## Theory

### The simple version

Imagine grading yourself on the exact homework problems you studied from — you'd always look brilliant, and learn nothing about how you'd do on the real exam. Held-out data plays the role of the real exam: problems the model never got to study.

Three ways to arrange "studied" vs "exam" data, in increasing order of how much they squeeze out of a fixed dataset:

- **Train/test split**: one held-out chunk, evaluated once. Simple, but that chunk never helps training, and the result depends on which points happened to land there.
- **K-fold cross-validation**: rotate which chunk is the "exam" `k` times, so every sample eventually gets both studied and examined, and average the `k` exam scores for a steadier estimate.
- **Bootstrapping** (`02-bagging`'s `bootstrap_sample`): resample with replacement, the same trick that gives each Random Forest tree its own training set. Applied to evaluation instead of training, it turns one accuracy number into a whole distribution of them.

### The formula

```text
train_test_split:
    shuffled_idx = rng.permutation(n_samples)
    n_test = round(n_samples * test_size)
    test_idx, train_idx = shuffled_idx[:n_test], shuffled_idx[n_test:]

k_fold_split:
    shuffled_idx = rng.permutation(n_samples)
    folds = array_split(shuffled_idx, k)
    for i in range(k):
        val_idx   = folds[i]
        train_idx = concatenate(folds[j] for j != i)
```

### How PyTorch actually implements this

Context only, untested by your submission: this is a data-splitting utility, not a `torch.nn` layer. `torch.utils.data.random_split` performs the same shuffle-then-partition idea for a `Dataset`, and `sklearn.model_selection.train_test_split` / `KFold` are the direct analogues implemented here.

## Explanation

`train_test_split` shuffles every sample index once (`rng.permutation(n_samples)`), then simply slices the shuffled order: the first `round(n_samples * test_size)` indices become `test_idx`, the rest become `train_idx`. Slicing a permutation can't duplicate or drop an index, so disjointness and full coverage fall out for free. Indexing `input[train_idx]`/`labels[train_idx]` (and the `test_idx` counterparts) keeps rows and labels paired because both are indexed with the same array.

`k_fold_split` shuffles indices the same way, then `np.array_split(shuffled_idx, k)` divides them into `k` folds — `array_split` handles a remainder gracefully instead of requiring exact divisibility, which is why the folds test uses `n_samples=23, k=4` on purpose. For each fold `i`, `val_idx = folds[i]`, and `train_idx = np.concatenate([folds[j] for j in range(k) if j != i])` — every other fold's indices, concatenated. Looping `i` over every fold produces exactly the `k` pairs Theory describes, one pair per fold acting as the held-out validation set in turn.
