---
name: dl-core-cross-entropy-loss
title: Cross-Entropy
tags: [deep-learning, loss-functions, autograd]
difficulty: Intermediate
---

## Statement

Implement:

```python
def cross_entropy_forward(logits, target, reduction="mean"): ...
def cross_entropy_backward(logits, target, reduction="mean", grad_output=1.0) -> np.ndarray: ...
```

Mirrors `torch.nn.functional.cross_entropy`: `logits` is `(n, num_classes)` raw scores, `target` is `(n,)` integer class indices (not one-hot).

## Theory

Cross-entropy loss is the standard loss for multi-class classification. PyTorch's `cross_entropy` fuses two conceptually separate steps into one numerically stable operation:

```text
log_probs = log_softmax(logits)           # 04-softmax, but in log-space
loss_i    = -log_probs[i, target[i]]      # negative log-likelihood of the true class
```

`-log(p)` is small when the model assigns high probability `p` to the correct class (little "surprise") and grows large as `p -> 0` (the model was confidently wrong). Working in log-space directly, rather than computing `softmax` then `log`, avoids computing `exp` of large numbers and then immediately undoing it with `log`, the same numerical-stability concern `04-softmax`'s row-max shift addresses.

The gradient of this combined operation has a famously clean closed form:

```text
dL/d_logits = softmax(logits) - one_hot(target)
```

This is the mathematical reason frameworks fuse softmax and cross-entropy into a single operation instead of composing separate softmax and NLL backward passes: differentiating through `04-softmax`'s backward and a separate NLL backward would eventually simplify to exactly this, but computing it directly is both faster and avoids extra numerical error along the way. Intuitively: the gradient pushes probability mass away from every class (subtracting `1` from wherever the true class's probability sits) proportional to how much probability the model currently assigns there, the model gets penalized for probability it placed on the wrong answer, and rewarded (pushed to increase) at the true answer.

## Explanation

`cross_entropy_forward` computes `log_probs` via the provided `_log_softmax`, indexes out `-log_probs[i, target[i]]` for every row using `np.arange(n)` fancy indexing, and reduces according to `reduction`, matching `01-mse`'s own three-reduction-mode pattern.

`cross_entropy_backward` recomputes `log_probs`, exponentiates to get `softmax(logits)` back, subtracts `1` at each row's true-class column (`grad[np.arange(n), target] -= 1.0`, the `one_hot(target)` subtraction from Theory), divides by `n` for `"mean"`, and multiplies by `grad_output`.
