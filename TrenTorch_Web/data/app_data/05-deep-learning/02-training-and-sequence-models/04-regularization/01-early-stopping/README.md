---
name: dl-training-early-stopping
title: 'Early stopping: monitor validation loss, restore the best checkpoint'
tags: [neural-networks, regularization, training]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Overparameterization and double descent: more parameters than data can still generalize`, later in this Part, complicates a simpler, older intuition worth understanding first: train a model long enough on a fixed training set, and TRAINING loss will keep decreasing (the model can always keep fitting its training examples a little better), but VALIDATION loss, measured on data the model never trains on, often stops improving and starts getting WORSE partway through training, the model has begun memorizing training-set-specific noise rather than learning anything that generalizes. The training run itself doesn't know this is happening; left running for its full planned number of epochs, it'll happily keep optimizing training loss long past the point where validation performance peaked.

Early stopping is the direct fix: watch validation loss every epoch, and if it hasn't improved for a while (a "patience" window of consecutive epochs), stop training and go back to whichever checkpoint actually had the BEST validation loss, not the checkpoint from whenever training happened to end.

### From theory to code

Implement `EarlyStopping.step(val_loss, state)`, called once per epoch. If `val_loss` is better (lower) than the best ever seen by more than `min_delta`, record it as the new best (along with `state`, typically a snapshot of the model's weights at that point) and reset the patience counter to zero. Otherwise, increment the patience counter, and if it reaches `self.patience`, set `self.should_stop = True`. Return `self.should_stop` either way, so a training loop can check the return value directly.

### Constraints

- The very FIRST call to `step` always counts as an improvement (there's no previous best to compare against yet), regardless of how large `val_loss` is.
- An improvement must beat the previous best by MORE than `min_delta`, not just be strictly smaller: `val_loss < best_loss - min_delta`, not `val_loss < best_loss`. With `min_delta=0`, this reduces to any strict improvement counting.
- `self.counter` resets to `0` on every improvement, and only accumulates on CONSECUTIVE non-improving epochs; a single improvement in the middle of a losing streak resets the streak entirely.
- `self.best_state` must be updated to whatever `state` was passed on the epoch that produced the new best `val_loss`, so it always reflects the actual best-performing checkpoint.

### Hints

<details>
<summary>Hint 1: The first call</summary>

`self.best_loss is None` is only true before the first call, use `if self.best_loss is None or val_loss < self.best_loss - self.min_delta:` as the single condition covering both "this is the first epoch" and "this epoch genuinely improved."

</details>

<details>
<summary>Hint 2: Improvement vs. no improvement</summary>

Inside that `if`, update `self.best_loss = val_loss`, `self.best_state = state`, and reset `self.counter = 0`. In the `else` branch, increment `self.counter += 1`, and if `self.counter >= self.patience`, set `self.should_stop = True`.

</details>

<details>
<summary>Hint 3</summary>

Return `self.should_stop` as the last line, this lets a training loop write `if early_stopping.step(val_loss): break` directly, without needing to check a separate attribute afterward.

</details>

## Theory

### The simple version

Trail running with a turnaround rule: "if I haven't gained any new elevation in the last 20 minutes, I've probably crested the peak and I'm now on flat or descending ground, turn back." You don't need to see the whole mountain from the summit to know you've likely passed it, a sustained lack of further progress is itself the signal. Early stopping applies the exact same logic to validation loss: a sustained lack of improvement (`patience` consecutive non-improving epochs) is treated as strong evidence that the "peak" (best generalization) has already been passed, even without knowing in advance exactly where it was.

### The formula

There's no numerical formula here beyond the comparison rule itself:

```
is_improvement = (best_loss is None) or (val_loss < best_loss - min_delta)

if is_improvement:
    best_loss = val_loss
    best_state = state
    counter = 0
else:
    counter += 1
    if counter >= patience:
        should_stop = True
```

### How PyTorch actually implements this

PyTorch itself has no built-in `EarlyStopping` class (it's considered training-loop logic, outside PyTorch's own scope, exactly like `[03-training-loop]`'s `DataLoader` and `MetricTracker`), but this exact pattern is what PyTorch Lightning's `EarlyStopping` callback and Keras's `EarlyStopping` callback both implement, parameter names (`patience`, `min_delta`) included, since this specific formulation has become close to a de facto standard. `min_delta` exists because validation loss is itself somewhat noisy from epoch to epoch (computed on a finite validation set, subject to some of the same batch-to-batch variance training loss has); without it, a training run could get "stuck" resetting its patience counter on genuinely meaningless, noise-sized improvements of `0.0000001`, defeating the entire point of the patience window. In real code, `state` is typically `copy.deepcopy(model.state_dict())`, a full snapshot of every parameter's current values, specifically deep-copied because `model.state_dict()` on its own returns references to the model's LIVE tensors, which would keep changing underneath you as training continues past the epoch where you saved it.

## Explanation

`step` checks `self.best_loss is None or val_loss < self.best_loss - self.min_delta`: the first clause makes the very first call always count as an improvement (nothing to compare against yet), and the second clause is the actual improvement threshold, requiring `val_loss` to beat the previous best by MORE than `min_delta`, not merely tie or barely beat it. On an improvement, `self.best_loss`, `self.best_state`, and `self.counter` (reset to `0`) are all updated. On a non-improvement, `self.counter` increments, and once it reaches `self.patience`, `self.should_stop` flips to `True` (and stays `True`, since nothing in `step` ever resets it back to `False`). The function returns `self.should_stop` either way, letting a training loop check it directly from the call site.
