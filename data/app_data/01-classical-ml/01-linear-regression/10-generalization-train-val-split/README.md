---
name: linear-regression-generalization-train-val-split
title: 'Generalization: train/val split and the generalization gap'
tags: [classical-ml, linear-regression, evaluation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Full Linear Regression Training Loop` trains a model and reports its loss, but a subtle trap lurks in that number: a loss computed on the EXACT data the model trained on tells you how well the model memorized that data, not how well it will perform on new data it's never seen. A model with enough flexibility (enough parameters relative to how much data it has) can drive training loss arbitrarily close to zero by essentially memorizing quirks and noise specific to the training set, while performing badly on anything new, the textbook definition of overfitting.

The fix is procedural, not algorithmic: hold out a chunk of data the model NEVER trains on, and evaluate on that held-out set instead. The gap between training performance and held-out performance is itself a measurement, the generalization gap, and it's the single most important diagnostic for "is this model actually learning something general, or just memorizing."

### From theory to code

Theory splits data into a training portion and a validation portion (shuffled first, so the split isn't accidentally biased by whatever order the data happened to arrive in), then defines the generalization gap as simply validation loss minus training loss.

Implement `train_val_split(input, target, val_fraction=0.2, seed=None)` first, then `generalization_gap(train_loss, val_loss)` on top of it.

### Constraints

- Shuffle `input` and `target` TOGETHER using the same permutation, a row's features must stay paired with its own target.
- `val_fraction` controls the split size; `round(n * val_fraction)` rows go to validation.
- Same `seed` must produce the same split (reproducibility, matching `01-sampling-estimating-distribution`'s convention).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`rng.permutation(n)` gives one shuffled order; index BOTH `input` and `target` with that same order to keep pairs aligned.

</details>

<details>
<summary>Hint 2</summary>

`generalization_gap` is a one-line subtraction, `val_loss - train_loss`.

</details>

## Theory

### The simple version

A student who memorizes the exact answers to last year's practice exam will ace that specific practice exam, but that says nothing about whether they actually understood the material, the real test is a DIFFERENT set of questions they've never seen before. A model's training loss is like the practice-exam score; validation loss (measured on data the model never trained on) is the real test. A model that aces the practice exam but bombs the real test has memorized, not learned, exactly what a large generalization gap reveals numerically.

### The formula

```text
train_val_split(input, target, val_fraction):
    shuffle input and target together, using the SAME random order
    val_size = round(len(input) * val_fraction)
    first val_size (of the shuffled order) -> validation set
    the rest -> training set

generalization_gap = val_loss - train_loss
```

A generalization gap near zero means the model performs about as well on unseen data as on data it trained on, a healthy sign. A LARGE positive gap (val loss much worse than train loss) is the numerical signature of overfitting: the model has fit patterns specific to the training set that don't hold up on new data. This is exactly why every serious ML workflow reports validation performance, not training performance, as the honest measure of how a model will actually perform once deployed, `07-evaluation`'s entire track (Classical ML) builds directly on this same train/val split idea, extending it to k-fold cross-validation, nested cross-validation, and beyond.

### How PyTorch actually implements this

`torch.utils.data.random_split` performs exactly this shuffle-then-split operation on a `Dataset`, the standard tool every PyTorch training script reaches for before training even starts. Every training loop this curriculum has built so far (`05-training-loop`'s `train_linear_regression`) trains on ONE dataset only; a real training script trains on the split's training portion and evaluates on the validation portion every few epochs specifically to WATCH the generalization gap as training proceeds, a gap that starts small and grows over training epochs is the classic early sign of overfitting, and is exactly what `07-early-stopping` (Evaluation & Model Selection, Classical ML) monitors to decide when to stop training before it gets worse.

## Explanation

`train_val_split` generates one shuffled permutation of row indices via `rng.permutation(n)`, splits it into a validation-sized prefix and a training-sized remainder, and indexes both `input` and `target` with each portion, keeping every row's features paired with its own target throughout.

`generalization_gap` returns `val_loss - train_loss` directly, the definition from Theory.
