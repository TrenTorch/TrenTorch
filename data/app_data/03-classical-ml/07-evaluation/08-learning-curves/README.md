---
name: evaluation-learning-curves
title: 'Learning curves: training/validation error vs. dataset size'
tags: [classical-ml, evaluation, model-complexity]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Say a model isn't doing as well as you'd like. There's an obvious, expensive fix: go collect more training data. But is it actually going to help? `03-bias-variance-tradeoff` diagnosed underfitting versus overfitting by comparing several _differently-trained_ models against the truth. That's useful, but it doesn't directly answer the question a manager or a budget actually cares about: "if I spend the next month labeling 10x more examples, will this specific model get meaningfully better?"

A learning curve answers exactly that, and cheaply: train the _same_ model (same hyperparameters, same complexity) on progressively larger slices of the data you already have, and watch how its training error and validation error move as the slice grows. The shape of those two curves, not their absolute values, tells you whether more data is worth collecting at all.

### From theory to code

Theory describes two curve shapes: both errors plateauing together at a high, similar value (more data won't help, the model itself is too simple), or validation error visibly dropping and closing in on training error as the training set grows (more data is helping, and might keep helping).

Producing either curve needs the same mechanical step repeated at every size: train on that many points, measure both errors, record them. Implement `learning_curve(fit_and_evaluate_fn, train_sizes)`, which owns exactly that sweep, the caller-supplied `fit_and_evaluate_fn` does the actual training and measuring.

### Constraints

- `fit_and_evaluate_fn(n_samples) -> (train_error, val_error)`: trains a model on the first `n_samples` training points and returns both its training error and its (fixed, held-out) validation error.
- `train_sizes`: a list of integers, not necessarily sorted.
- Call `fit_and_evaluate_fn` exactly once per entry in `train_sizes`, in the order given, never sorted or deduplicated.
- Returns `(train_errors, val_errors)`, each shape `(len(train_sizes),)`, one entry per size, in the same order as `train_sizes`.
- Do not swap which returned value goes into which output array.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

This is a sweep, not a model. You aren't training anything yourself, `fit_and_evaluate_fn` already does that; your job is only to call it once per size and keep two running lists.

</details>

<details>
<summary>Hint 2</summary>

`fit_and_evaluate_fn` returns a `(train_error, val_error)` tuple. Unpack it into two separate lists as you go, then convert both to `np.ndarray` at the end, don't try to build the arrays up front before you know all the values.

</details>

## Theory

### The simple version

Imagine grading a student on the same test after they've studied 10 flashcards, then 50, then 200. If their score barely moves no matter how many flashcards they study, the flashcards aren't the bottleneck, something about how they study is. If their score keeps climbing and starts matching how well they do on flashcards they've actually seen, more flashcards would keep helping. A learning curve runs exactly this experiment on a model instead of a student.

### The formula

```text
for n_samples in train_sizes:
    train_error, val_error = fit_and_evaluate_fn(n_samples)
    record train_error into train_errors
    record val_error into val_errors
return train_errors, val_errors
```

The diagnosis reads off the two resulting arrays:

- **High bias (underfitting)**: `train_errors` and `val_errors` both stay high and close together across all sizes; `val_errors[-1] - val_errors[0]` is small, more data barely moved anything.
- **High variance, closing gap (overfitting, improving with data)**: `train_errors` stays low throughout; `val_errors` starts well above it but decreases substantially, `val_errors[-1]` ends up close to `train_errors[-1]`.

### How PyTorch actually implements this

PyTorch has no built-in `learning_curve` utility, this is a training-and-evaluation protocol, not a tensor operation. In practice it's built the same way `solution.py` does it: a loop that slices a `Dataset`/`DataLoader` down to `n_samples`, runs an ordinary PyTorch training loop (`03-decision-trees`-style tree fitting or `01-linear-regression/05-training-loop`-style gradient descent), and records `loss.item()` on the training slice and on a fixed validation set at each size.

## Explanation

`learning_curve` in `solution.py` is a thin loop over `train_sizes`: it initializes `train_errors = []` and `val_errors = []`, and for each `n_samples` calls `train_error, val_error = fit_and_evaluate_fn(n_samples)`, appending each piece to its own list. After the loop, `return np.array(train_errors), np.array(val_errors)` converts both to the arrays the caller expects. The actual work, training on a specific subset of the data and computing both errors, is left entirely to the caller-supplied `fit_and_evaluate_fn`, the same "black box function, don't assume what model it trains" pattern `04-grid-search`'s `fit_and_score_fn` uses; `tests.py`'s `test_calls_fit_and_evaluate_exactly_once_per_size` and `test_preserves_the_given_order_not_sorted` both check that this loop does nothing more than iterate `train_sizes` in order, exactly once each, no sorting or extra calls.
