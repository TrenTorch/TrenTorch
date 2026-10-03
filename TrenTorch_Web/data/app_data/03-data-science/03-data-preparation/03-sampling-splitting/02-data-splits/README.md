---
name: data-science-data-splits
title: 'Train, Validation & Test Splits'
tags: [data-science, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-stratified-sampling` keeps class proportions when sampling. Before any model is trained there is a more basic question: which rows may it learn from, and which are held back to judge it? A model scored on rows it was trained on looks better than it is, so the data is split into a **training** set to learn from, a **validation** set to tune choices on and a **test** set touched once at the end. Random shuffling is right for independent rows and wrong for anything with a time order, where shuffling lets the model train on the future to predict the past. This question builds the splits for both cases, and the cross-validation variants that reuse limited data.

### From theory to code

Implement `train_val_test_split(n, val_fraction, test_fraction, rng)` for shuffled splits, then `time_ordered_split(n, val_fraction, test_fraction)` for chronological splits, then `k_fold_indices(n, k, rng)` for cross-validation, then `expanding_window_splits(n, n_splits, min_train)` for cross-validation on time-ordered data. The signatures and docstrings are already in the editor.

### Constraints

- `n` is the number of rows, and splits are returned as integer index arrays into `0 .. n-1`. `rng` is a `numpy.random.Generator`.
- `train_val_test_split` shuffles with one `rng.permutation(n)`. The test set has `int(round(test_fraction * n))` indices, the validation set has `int(round(val_fraction * n))`, and the training set has the rest. In the permutation the order is train first, then validation, then test. It returns `(train, val, test)`.
- `time_ordered_split` uses the same sizes but no shuffling: the earliest rows are training, the next block is validation and the latest rows are test, each in increasing order. It returns `(train, val, test)`.
- `k_fold_indices` shuffles with one `rng.permutation(n)` and cuts it into `k` blocks with `np.array_split`. It returns a list of `k` pairs `(train_indices, val_indices)` where `val_indices` is block `i` and `train_indices` is every other block concatenated in block order.
- `expanding_window_splits` returns a list of `n_splits` pairs `(train_indices, val_indices)`. The rows after the first `min_train` rows are cut into `n_splits` contiguous blocks with `np.array_split`. Split `i` validates on block `i` and trains on every row before that block, in increasing order.

### Hints

<details>
<summary>Hint 1</summary>

All three random splits reuse the same trick: permute the row numbers once, then slice the permutation. That guarantees no row lands in two sets.

</details>

<details>
<summary>Hint 2</summary>

In time-ordered data, a row's neighbours in time are correlated. A split that leaves later rows in the training set and earlier rows in the test set lets the model peek at the future.

</details>

<details>
<summary>Hint 3</summary>

For the expanding window, the training set grows with every split because everything before the validation block is already in the past.

</details>

## Theory

### The simple version

A teacher who gives the exam questions out as homework cannot tell whether the students learned the subject or memorized the answers. Keeping the exam questions secret until the exam is the whole idea of a test set. A validation set is a practice exam the student can take repeatedly to decide how to study. For stock prices or weekly sales the exam must come _after_ the studying in time, since tomorrow cannot be used to learn about yesterday.

### The formula

With $n$ rows, validation fraction $f_v$ and test fraction $f_t$, the set sizes are

$$
n_{\text{test}} = \operatorname{round}(f_t\,n), \qquad n_{\text{val}} = \operatorname{round}(f_v\,n), \qquad n_{\text{train}} = n - n_{\text{val}} - n_{\text{test}}
$$

**$k$-fold cross-validation** cuts the shuffled rows into $k$ blocks. Each block takes a turn as the validation set while the other $k-1$ blocks train, and the $k$ scores are averaged:

$$
\text{CV score} = \frac{1}{k}\sum_{i=1}^{k} \text{score}\big(\text{model trained without block } i,\ \text{block } i\big)
$$

**Expanding-window** validation for time-ordered data trains on everything before each block and validates on the block itself, so the training set grows and no split ever trains on the future.

### Why three sets & not two

Every time a choice is made by looking at the validation score (which model, which learning rate, which features), the validation set stops being an honest judge, because the choice was tuned to it. The test set is kept apart so that one final, untouched measurement is still honest. Reusing the test set for tuning, even informally, quietly turns it into a second validation set.

### Splits that must not be shuffled

Time series, anything with repeated measurements of the same person or machine, and data with groups (several rows per customer) need splits that respect the structure. Shuffling puts a customer's rows on both sides of the split, so the model learns the customer rather than the pattern. Splitting by group, and by time for time-ordered data, is what keeps the test score honest.

### How NumPy/PyTorch actually implements this

`sklearn.model_selection.train_test_split` shuffles and splits (call it twice for three sets), `KFold` and `StratifiedKFold` are the cross-validation splitters, `TimeSeriesSplit` is the expanding-window splitter and `GroupKFold` splits by group. `torch.utils.data.random_split(dataset, [n_train, n_val, n_test], generator=g)` is the PyTorch equivalent of the shuffled three-way split.

## Explanation

`train_val_test_split` takes one `rng.permutation(n)` and slices it into train, validation and test by the rounded sizes, so the three index sets are disjoint and cover every row exactly once. `time_ordered_split` does the same slicing on `np.arange(n)` instead of a permutation, so each set is a contiguous time block in increasing order. `k_fold_indices` permutes once, splits into `k` blocks with `np.array_split`, and for each block concatenates the other blocks as the training indices. `expanding_window_splits` skips the first `min_train` rows as the minimum history, splits the remaining indices into `n_splits` blocks, and for block `i` trains on `np.arange(start_of_block_i)`, which is everything earlier.
