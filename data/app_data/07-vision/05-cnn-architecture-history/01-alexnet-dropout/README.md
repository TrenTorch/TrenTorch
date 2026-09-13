---
name: vision-history-alexnet-dropout
title: 'Note: AlexNet — Dropout, and What Actually Changed from LeNet'
tags: [computer-vision, cnn, history, regularization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

AlexNet (2012) is usually credited with "starting" deep learning's modern era, but its architecture wasn't a radical departure from LeNet (1998) — it's a deeper stack of the same convolution/pool/fully-connected pattern. What actually mattered was a handful of practical changes that made a deep network trainable and generalizable at all: ReLU instead of sigmoid/tanh (avoiding vanishing gradients — see `02-deep-learning-core`'s activation questions), and dropout, a regularization technique that fights overfitting in the large fully-connected layers that dominate AlexNet's parameter count. This question implements dropout, since it's the one AlexNet-era idea concrete and self-contained enough to code and test directly.

### From theory to code

Theory says: during training, randomly and independently zero out each unit with some probability `p`, forcing the network to not rely on any single unit too heavily (since it might vanish on any given forward pass). To keep the _expected_ value of the output unchanged (so nothing downstream needs to know or care whether dropout is active), scale every unit that survives by `1 / (1 - p)`.

Implement `dropout_forward(x, p, rng)` against that reasoning.

### Constraints

- `x`: any-shape array of activations.
- `p`: drop probability, in `[0, 1)`.
- `rng`: a `numpy.random.Generator`, passed in explicitly so tests (and callers) can control and reproduce randomness.
- Returns an array the same shape as `x`, where each element is either exactly `0.0` (dropped) or `x[i] / (1 - p)` (kept and rescaled).
- `x` is never modified in place.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`rng.random(x.shape)` draws one uniform `[0, 1)` value per element of `x` — compare it against `p` to decide, per element, whether to keep or drop.

</details>

<details>
<summary>Hint 2</summary>

`mask = (rng.random(x.shape) >= p).astype(x.dtype)` is 1.0 wherever a unit survives and 0.0 wherever it's dropped — `x * mask / (1 - p)` applies the mask and the inverted-dropout rescaling in one expression.

</details>

## Theory

### The simple version

Imagine training a team where, on any given day, a random subset of members simply doesn't show up — nobody can afford to become the single point of failure the whole team quietly depends on, so everyone has to learn to contribute somewhat independently and redundantly. Dropout does this to a neural network's units: every forward pass during training, a random subset is temporarily zeroed out, which discourages any small group of units from co-adapting into a fragile, over-specialized shortcut. Rescaling the survivors keeps the "total signal" flowing through the layer roughly constant whether or not any given unit happened to survive.

### The formula

```text
mask = 1 where random_uniform(0,1) >= p, else 0    # drawn fresh, per element, per forward pass
out  = x * mask / (1 - p)
```

### How PyTorch actually implements this

`torch.nn.Dropout(p)` and `torch.nn.functional.dropout(x, p, training=True)` implement exactly this "inverted dropout" scheme — the scaling by `1/(1-p)` happens at _training_ time specifically so that calling `model.eval()` can simply skip dropout entirely (`training=False` returns `x` unchanged) with no separate rescaling step needed at inference. AlexNet applied dropout only to its final two large fully-connected layers, since those layers held the overwhelming majority of its ~60 million parameters and were where overfitting was the biggest risk; its convolutional layers, with far fewer parameters and heavy weight-sharing across spatial positions, didn't need it.

## Explanation

`rng.random(x.shape)` draws one independent uniform value in `[0, 1)` for every element of `x`, and comparing against `p` produces a boolean array that's `True` (kept) with probability `1 - p` per element and `False` (dropped) with probability `p` — exactly the independent-per-unit dropping the theory calls for. Casting that boolean mask to `x.dtype` turns it into `1.0`/`0.0`, so `x * mask` zeroes every dropped element while leaving surviving elements untouched; dividing the whole result by `(1 - p)` is the "inversion" that gives dropout its name — it rescales the kept units up so that, averaged over many random masks, `E[mask] * (1/(1-p)) = (1-p) * (1/(1-p)) = 1`, meaning the expected output equals the original input regardless of `p`.
