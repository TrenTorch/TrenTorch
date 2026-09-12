---
name: dl-core-cross-entropy-loss
title: Cross-Entropy
tags: [deep-learning, loss-functions, autograd]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`04-softmax` turns raw class scores into a probability distribution. For multi-class classification, the standard loss then asks a single question of that distribution: how much probability did the model assign to the *actual* correct class? Cross-entropy is exactly that question turned into a differentiable loss — and computing it well means never actually materializing the softmax probabilities and then taking their log separately, since that route reintroduces the same overflow risk `04-softmax`'s row-max shift was built to avoid.

### From theory to code

Implement `cross_entropy_forward(logits, target, reduction="mean")` and `cross_entropy_backward(logits, target, reduction="mean", grad_output=1.0)`, mirroring `torch.nn.functional.cross_entropy`: `logits` is `(n, num_classes)` raw scores, `target` is `(n,)` integer class indices (not one-hot).

### Constraints

- `logits`: shape `(n, num_classes)`. `target`: shape `(n,)`, integer class indices in `[0, num_classes)`.
- `reduction="mean"`: returns a scalar, the average per-sample loss.
- `reduction="sum"`: returns a scalar, the total loss.
- `reduction="none"`: returns shape `(n,)`, the per-sample loss.
- `cross_entropy_backward` takes the same `logits`/`target`/`reduction`, plus `grad_output`, and returns a `(n, num_classes)` gradient regardless of `reduction`.
- Compute in log-space directly (log-softmax), never `log(softmax(logits))` as two separate steps.
- No Python loops over samples; no mutating `logits` or `target`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`log_softmax(logits)` computed directly (shift by the row max, subtract `log(sum(exp(shifted)))`) avoids ever calling `exp` on a large raw logit and then immediately undoing it with `log` — compute it in one pass, not as `softmax` followed by `log`.

</details>

<details>
<summary>Hint 2</summary>

`log_probs[np.arange(n), target]` picks out, per row, the log-probability the model assigned to that row's true class — negate and reduce.

</details>

## Theory

### The simple version

`-log(p)` is small when the model assigns high probability `p` to the correct class (little "surprise") and grows large as `p -> 0` (the model was confidently wrong). Cross-entropy loss is exactly this "surprise" measured at whichever class the label says is actually correct, averaged (or summed) across the batch.

### The formula

PyTorch's `cross_entropy` fuses two conceptually separate steps into one numerically stable operation:

```text
log_probs = log_softmax(logits)           # 04-softmax, but in log-space
loss_i    = -log_probs[i, target[i]]      # negative log-likelihood of the true class
```

Working in log-space directly, rather than computing `softmax` then `log`, avoids computing `exp` of large numbers and then immediately undoing it with `log`, the same numerical-stability concern `04-softmax`'s row-max shift addresses.

The gradient of this combined operation has a famously clean closed form:

```text
dL/d_logits = softmax(logits) - one_hot(target)
```

This is the mathematical reason frameworks fuse softmax and cross-entropy into a single operation instead of composing separate softmax and NLL backward passes: differentiating through `04-softmax`'s backward and a separate NLL backward would eventually simplify to exactly this, but computing it directly is both faster and avoids extra numerical error along the way. Intuitively: the gradient pushes probability mass away from every class (subtracting `1` from wherever the true class's probability sits) proportional to how much probability the model currently assigns there — the model gets penalized for probability it placed on the wrong answer, and rewarded (pushed to increase) at the true answer.

### How PyTorch actually implements this

`torch.nn.functional.cross_entropy(logits, target, reduction=...)` implements exactly this fused log-softmax-plus-NLL computation, with the same clean `softmax(logits) - one_hot(target)` backward pass — verified in this exercise's own `tests.py`, whose `test_forward_matches_known_oracle_values` and `test_backward_matches_known_oracle_values` bake in values generated once, offline, from `torch.nn.functional.cross_entropy` plus autograd.

## Explanation

`cross_entropy_forward` computes `log_probs` via the provided `_log_softmax`, indexes out `-log_probs[i, target[i]]` for every row using `np.arange(n)` fancy indexing, and reduces according to `reduction`, matching `01-mse`'s own three-reduction-mode pattern.

`cross_entropy_backward` recomputes `log_probs`, exponentiates to get `softmax(logits)` back, subtracts `1` at each row's true-class column (`grad[np.arange(n), target] -= 1.0`, the `one_hot(target)` subtraction from Theory), divides by `n` for `"mean"`, and multiplies by `grad_output`.
