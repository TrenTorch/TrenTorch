---
name: evaluation-early-stopping
title: 'Early stopping: halting training at the best validation checkpoint'
tags: [classical-ml, evaluation, regularization, training-loop]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-full-boosting-loop`'s `n_trees` and every other training loop in this curriculum runs for a fixed, predetermined number of iterations. In practice, training longer doesn't always help: past some point, a model starts fitting the training set's specific noise rather than the real pattern, and validation loss (measured on data the model hasn't fit to) starts getting *worse* even as training loss keeps improving — the same overfitting `03-bias-variance-tradeoff`'s high-variance regime describes.

### From theory to code

Implement `best_epoch_with_min_delta`, `early_stopping_should_stop`, and `train_with_early_stopping(step_fn, max_epochs, patience, min_delta=0.0)`. `step_fn(epoch) -> (state, val_loss)` is a black box: one epoch of training plus a validation-loss check, for whatever model. This question doesn't care what model it is, just when to stop training it.

### Constraints

- `best_epoch_with_min_delta(history, min_delta=0.0)` returns the index of the best (lowest) loss, where "best" requires beating the previous best by more than `min_delta`.
- `early_stopping_should_stop(history, patience, min_delta=0.0)` returns `True` once `patience` epochs have passed with no qualifying improvement; `False` for an empty history.
- `train_with_early_stopping` returns a dict with `best_state`, `best_loss`, `history`, and `stopped_epoch`.
- The returned model is whichever epoch's `state` had the best validation loss, never necessarily the *last* epoch's.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`best_epoch_with_min_delta` and `train_with_early_stopping`'s own best-tracking must use the exact same comparison (`value < best_value - min_delta`) — if they disagree about what counts as an improvement, the two could pick different "best" epochs.

</details>

<details>
<summary>Hint 2</summary>

"Epochs since best" is just `(len(history) - 1) - best_epoch_with_min_delta(...)` — no separate counter variable needed, recompute it from the history each time.

</details>

## Theory

### The simple version

**Early stopping** is the practical fix: keep training, but keep a running record of the best validation loss seen so far and *which* epoch produced it, and stop once validation loss hasn't meaningfully improved for `patience` epochs in a row. Critically, the model actually returned is the one from the *best* epoch, not the one training happened to be on when it stopped — the last few epochs before stopping were already getting worse, by definition.

### The formula

```text
epoch: 0    1    2    3    4    5    6    7    8
loss:  10   8    6    5    4    3    3.5  4    4.5
                              ^best              ^stop (3 epochs since best, patience=3)
```

`min_delta` guards against stopping on statistically meaningless noise: a validation loss that wiggles down by `0.0001` isn't a real improvement worth resetting the patience counter for — `min_delta` sets the bar an improvement has to clear to count at all.

### How PyTorch actually implements this

Context only, untested by your submission: PyTorch has no built-in early-stopping utility — it's typically implemented as a small callback in the training loop itself (or via a library like PyTorch Lightning's `EarlyStopping` callback), following exactly this pattern: track the best validation metric and its epoch, compare the current epoch's gap against it to `patience`, and checkpoint (`torch.save`) the best-so-far model state rather than only the final one.

## Explanation

`best_epoch_with_min_delta` walks `history` once, tracking the smallest value seen and updating only when a later value beats it by more than `min_delta` (`value < best_value - min_delta`, not just `value < best_value`), so a tiny fluctuation doesn't reset which epoch counts as "best."

`early_stopping_should_stop` compares `(len(history) - 1) - best_epoch_with_min_delta(...)` (how many epochs have passed since the best one) against `patience` — an empty history can't have stopped yet, so it returns `False` immediately.

`train_with_early_stopping` calls `step_fn` once per epoch, appending each `val_loss` to `history`. It updates `best_state`/`best_loss` only when the new loss actually beats the previous best by more than `min_delta` (the same rule `best_epoch_with_min_delta` uses, kept consistent so the two never disagree about which epoch is "best"), and checks `early_stopping_should_stop` after every epoch, breaking out of the loop the moment it returns `True`. `stopped_epoch` records where training actually halted; `best_state`/`best_loss` record what actually gets returned to the caller — an earlier, better checkpoint than the epoch training stopped on.
