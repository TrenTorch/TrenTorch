---
name: dl-core-binary-cross-entropy-loss
title: Binary Cross-Entropy
tags: [deep-learning, loss-functions, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def bce_loss_forward(probs, target, reduction="mean"): ...
def bce_loss_backward(probs, target, reduction="mean", grad_output=1.0) -> np.ndarray: ...
```

Mirrors `torch.nn.functional.binary_cross_entropy`: `probs` is already-sigmoided values in `(0, 1)`, `target` is `0`/`1` labels.

## Theory

Binary cross-entropy is `02-cross-entropy`'s two-class special case, made explicit rather than routed through a full softmax over two classes:

```text
elementwise_i = -(target_i * log(probs_i) + (1 - target_i) * log(1 - probs_i))
```

Only one of the two terms is ever "active" per example: when `target_i = 1`, the `(1 - target_i)` term vanishes and the loss is `-log(probs_i)` (penalize low confidence in the positive class); when `target_i = 0`, it's `-log(1 - probs_i)` (penalize high confidence in the positive class when the answer was negative).

This function's own name is the plain (non-logits) form: it takes `probs`, already-sigmoided values, as opposed to `*_with_logits` variants (like Classical ML's `classification-production-bce-with-logits`) that fuse the sigmoid and the loss into one numerically-fused operation. Taking raw probabilities means `log(0)` (when a probability collapses to exactly `0` or `1`, easy for a confident, well-trained sigmoid to produce) has to be guarded against directly, by clipping `probs` into `[eps, 1 - eps]` before ever taking a log.

Differentiating gives:

```text
dL/d_probs_i = (probs_i - target_i) / (probs_i * (1 - probs_i))
```

Note this is the gradient with respect to the **probability**, not the **logit**: `classification-bce-gradient` (Classical ML) derives the much simpler `prediction - target` form, that simplicity only appears because it differentiates through the sigmoid and the loss together; taken separately, as this question does, the probability-space gradient is the messier expression above.

## Explanation

`bce_loss_forward` clips `probs` into `[_EPS, 1 - _EPS]`, computes the elementwise formula from Theory, and reduces according to `reduction`, the same three-mode pattern `01-mse` and `02-cross-entropy` both use.

`bce_loss_backward` clips the same way, computes `(clipped - target) / (clipped * (1 - clipped))`, divides by the element count for `"mean"`, and multiplies by `grad_output`.
