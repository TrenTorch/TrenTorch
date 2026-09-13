---
name: dl-core-binary-cross-entropy-loss
title: Binary Cross-Entropy
tags: [deep-learning, loss-functions, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`02-cross-entropy` handles the general multi-class case via a full softmax over every class. Binary classification is the two-class special case of that same idea, common enough (and simple enough) that it gets its own dedicated, explicit loss rather than routing through a full softmax over two classes.

### From theory to code

Implement `bce_loss_forward(probs, target, reduction="mean")` and `bce_loss_backward(probs, target, reduction="mean", grad_output=1.0)`, mirroring `torch.nn.functional.binary_cross_entropy`: `probs` is already-sigmoided values in `(0, 1)`, `target` is `0`/`1` labels.

### Constraints

- `probs`: any NumPy array shape, values in `(0, 1)` (already passed through a sigmoid). `target`: matching shape, `0`/`1` labels.
- `reduction="mean"`/`"sum"`/`"none"`: same three modes as `01-mse` and `02-cross-entropy`.
- Must stay finite even when `probs` is exactly `0` or `1` (guard `log` with clipping).
- `bce_loss_backward` returns the gradient with respect to `probs` (not logits) — a different, messier expression than the fused sigmoid+BCE gradient.
- No Python loops; no mutating `probs` or `target`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Only one of the two log terms is ever "active" per example, depending on whether `target_i` is `0` or `1` — but you don't need an `if`, the `(1 - target_i)` and `target_i` factors already zero out whichever term doesn't apply.

</details>

<details>
<summary>Hint 2</summary>

Clip `probs` into `[eps, 1 - eps]` before any `log`, in both the forward AND backward pass — a confident, well-trained sigmoid can genuinely output exactly `0.0` or `1.0` in floating point.

</details>

## Theory

### The simple version

Binary cross-entropy is `02-cross-entropy`'s two-class special case, made explicit rather than routed through a full softmax over two classes:

```text
elementwise_i = -(target_i * log(probs_i) + (1 - target_i) * log(1 - probs_i))
```

Only one of the two terms is ever "active" per example: when `target_i = 1`, the `(1 - target_i)` term vanishes and the loss is `-log(probs_i)` (penalize low confidence in the positive class); when `target_i = 0`, it's `-log(1 - probs_i)` (penalize high confidence in the positive class when the answer was negative).

### The formula

This function's own name is the plain (non-logits) form: it takes `probs`, already-sigmoided values, as opposed to `*_with_logits` variants (like Classical ML's `classification-production-bce-with-logits`) that fuse the sigmoid and the loss into one numerically-fused operation. Taking raw probabilities means `log(0)` (when a probability collapses to exactly `0` or `1`, easy for a confident, well-trained sigmoid to produce) has to be guarded against directly, by clipping `probs` into `[eps, 1 - eps]` before ever taking a log.

Differentiating gives:

```text
dL/d_probs_i = (probs_i - target_i) / (probs_i * (1 - probs_i))
```

Note this is the gradient with respect to the **probability**, not the **logit**: `classification-bce-gradient` (Classical ML) derives the much simpler `prediction - target` form, that simplicity only appears because it differentiates through the sigmoid and the loss together; taken separately, as this question does, the probability-space gradient is the messier expression above.

### How PyTorch actually implements this

`torch.nn.functional.binary_cross_entropy(probs, target, reduction=...)` implements exactly this plain (non-fused) formula, taking already-sigmoided probabilities — verified in this exercise's own `tests.py`, whose `test_forward_matches_known_oracle_values` and `test_backward_matches_known_oracle_values` bake in values generated once, offline, from `torch.nn.functional.binary_cross_entropy` plus autograd. PyTorch also offers `binary_cross_entropy_with_logits`, which fuses the sigmoid in and produces the much simpler `prediction - target` gradient this exercise's Theory contrasts against.

## Explanation

`bce_loss_forward` clips `probs` into `[_EPS, 1 - _EPS]`, computes the elementwise formula from Theory, and reduces according to `reduction`, the same three-mode pattern `01-mse` and `02-cross-entropy` both use.

`bce_loss_backward` clips the same way, computes `(clipped - target) / (clipped * (1 - clipped))`, divides by the element count for `"mean"`, and multiplies by `grad_output`.
