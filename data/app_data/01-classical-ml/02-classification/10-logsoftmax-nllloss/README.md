---
name: classification-logsoftmax-nllloss
title: 'LogSoftmax + NLLLoss: the two pieces CrossEntropyLoss actually fuses'
tags: [classical-ml, classification, loss-functions]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`Stretch: Softmax + Categorical Cross-Entropy` computed `softmax`, then took `log` of the true class's probability, two separate operations chained together. That two-step version has a real, silent failure mode: when a logit dominates strongly enough, `softmax` correctly produces a probability extremely close to (but not exactly) `0` for the losing classes, and `log` of a number that close to zero either underflows to `-inf` or, worse, rounds to EXACTLY `0.0` in floating point, at which point `log(0.0)` is `-inf`, propagating `nan` through the rest of the computation.

`torch.nn.functional.cross_entropy` never actually computes `log(softmax(Z))` as two separate steps for exactly this reason. It's built from two pieces, `log_softmax` (which never actually forms the raw probabilities, staying in log-space the entire time) and `nll_loss` (which just indexes and averages), and this question builds both pieces to see precisely how the fused version sidesteps the naive version's numerical trap.

### From theory to code

Theory derives `log_softmax` algebraically (expanding `log(exp(z_i) / sum(exp(z_j)))` and simplifying) into a form that never divides two floating-point numbers close to zero, and defines `nll_loss` as a simple indexing-and-averaging operation on whatever log-space values it's handed.

Implement `log_softmax(Z)` first, then `nll_loss(log_probs, y_indices)` on top of it.

### Constraints

- `log_softmax` must not call `np.log(softmax(Z))` as two separate steps, it must derive the log-space result directly, algebraically.
- `Z` is `(n, num_classes)`, `y_indices` is `(n,)`, integer class indices.
- `nll_loss` averages over rows (the `n` axis), consistent with `06-softmax-cce`'s own `cce_loss` reduction convention.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Start from `06-softmax-cce`'s own max-shift trick (`Z - max(Z, axis=1, keepdims=True)`), then subtract `log(sum(exp(shifted Z)))` instead of dividing and taking a separate log.

</details>

<details>
<summary>Hint 2</summary>

`nll_loss` is one line: `-np.mean(log_probs[np.arange(n), y_indices])`, indexing out each row's true-class log-probability.

</details>

## Theory

### The simple version

Imagine measuring a whisper's loudness by first converting it to a fraction of the loudest sound in the room (a number extremely close to zero), then taking the log of that tiny fraction, two steps, with a lot of precision lost in that first division before the log ever runs. A more careful approach measures loudness directly in a logarithmic scale from the start, decibels, never forming the tiny intermediate fraction at all. `log_softmax` is exactly this: work entirely in log-space from the beginning, instead of forming (possibly tiny) raw probabilities and THEN taking their log.

### The formula

Starting from softmax's definition and taking a log:

```text
log(softmax(Z)_i) = log(exp(Z_i) / sum_j(exp(Z_j)))
                   = Z_i - log(sum_j(exp(Z_j)))
```

Applying the same max-shift stability trick `06-softmax-cce`'s `softmax` already uses (subtracting `max(Z)` doesn't change the mathematical result, since it cancels, but keeps every `exp()` call bounded):

```text
log_softmax(Z)_i = (Z_i - max(Z)) - log(sum_j(exp(Z_j - max(Z))))
```

Crucially, this expression NEVER divides two numbers, it's built entirely from subtraction and one `log` of a SUM (which stays comfortably away from zero, since it always includes the term where `Z_j - max(Z) = 0`, contributing at least `exp(0) = 1` to the sum). This is precisely why `log_softmax(Z)` stays finite and accurate even when `np.log(softmax(Z))` (the naive two-step version) would produce `-inf` or `nan`.

`nll_loss` (negative log-likelihood) is then trivial once the log-probabilities are already computed: index out the true class's log-probability for every row, negate, and average, exactly `06-softmax-cce`'s `cce_loss`, just now taking already-log-space input instead of raw probabilities.

### How PyTorch actually implements this

`torch.nn.functional.cross_entropy` is, internally, precisely `nll_loss(log_softmax(logits), target)`, fused into one call and one optimized kernel rather than two separate Python-visible steps, exactly the composition this question builds by hand. `02-deep-learning-core/03-losses/02-cross-entropy`'s own `_log_softmax` helper is the identical function implemented here, reused directly rather than rederived, this question is the Classical ML section's own first-principles encounter with the exact same numerical-stability lesson that question's Theory section names explicitly. `torch.nn.LogSoftmax` and `torch.nn.NLLLoss` also exist as separate, standalone modules (occasionally useful when you need the log-probabilities themselves, not just the final loss, for something like `07-early-stopping`-style per-example loss inspection), but `cross_entropy`'s fused version is preferred in almost all real training code specifically for the numerical stability this question demonstrates.

## Explanation

`log_softmax` shifts `Z` by its row max (for the same overflow-avoidance reason `06-softmax-cce`'s `softmax` shifts), then subtracts `log(sum(exp(shifted Z)))`, the direct algebraic simplification from Theory, never forming or dividing by a raw probability.

`nll_loss` indexes out each row's true-class log-probability via `log_probs[np.arange(n), y_indices]`, negates, and averages.
