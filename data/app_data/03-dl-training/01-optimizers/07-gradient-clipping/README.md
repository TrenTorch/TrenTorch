---
name: dl-training-gradient-clipping
title: Gradient clipping (global norm)
tags: [optimization]
difficulty: Beginner
---

## Statement

### The problem, from first principles

`01-outlier-detection` (Math & Statistics) already warned that a single extreme value can badly distort a mean or a standard deviation. The same failure mode threatens gradient descent directly: one badly-scaled batch, or one region of an especially steep loss surface, can produce a gradient whose magnitude is enormous, and taking a full-size step in that direction can throw a model's weights somewhere far worse than where they started, sometimes badly enough that training never fully recovers, a real, common cause of a loss curve that suddenly spikes to `nan` partway through training.

Gradient clipping is the direct fix: measure how large the gradient is overall, and if it's larger than some chosen threshold, shrink it back down before it's ever used to update anything, while carefully preserving its DIRECTION, only the magnitude gets capped.

### From theory to code

Theory computes one GLOBAL norm across every gradient array at once (treating them as if concatenated into a single vector), and, if that norm exceeds a threshold, rescales every gradient by the same factor so the new global norm is exactly the threshold.

Implement `compute_global_norm(grads)` first, then `clip_grad_norm(grads, max_norm)` on top of it.

### Constraints

- `compute_global_norm` computes ONE number across ALL gradient arrays combined, not a separate norm per array.
- `clip_grad_norm` returns fresh arrays (copies), whether or not clipping was actually needed.
- Rescaling must use the SAME factor for every gradient array, preserving their relative proportions.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`sum(np.sum(g**2) for g in grads)` sums every gradient array's own squared values into one running total; take a single `sqrt` at the end.

</details>

<details>
<summary>Hint 2</summary>

`clip_coef = max_norm / (total_norm + eps)`; only rescale if `clip_coef < 1.0` (meaning the actual norm exceeds `max_norm`).

</details>

## Theory

### The simple version

A driver going downhill hits the brakes hard enough to avoid a sudden hazard, but SLAMMING the brakes too hard can send the car into a skid, worse than the original hazard. A measured, capped braking force avoids both problems: strong enough to actually respond to the hazard, but never so extreme it causes its own crash. Gradient clipping caps how large a single training step's "force" can be, in exactly this spirit: strong enough to respond to a real, large gradient signal, but never so large it sends the model's weights somewhere catastrophic.

### The formula

```text
global_norm = sqrt(sum over ALL gradient arrays of sum(g^2))

clip_coef = max_norm / (global_norm + eps)
if clip_coef < 1:
    every gradient *= clip_coef      -- shrink, preserving relative direction
else:
    leave every gradient unchanged   -- already within budget
```

Computing ONE global norm, rather than clipping each parameter's gradient independently, matters: it preserves the RELATIVE proportions between different parameters' gradients (a parameter whose gradient happened to be twice as large as another's stays twice as large after clipping, just both scaled down together), rather than distorting the gradient's overall direction the way clipping each piece independently would.

### How PyTorch actually implements this

`torch.nn.utils.clip_grad_norm_` implements exactly this formula (this question's implementation matches it precisely, verified directly), called in a training loop AFTER `loss.backward()` populates every parameter's `.grad`, and BEFORE `optimizer.step()` applies them. It's a standard, nearly-universal safeguard in training large models, especially transformers and RNNs (`Backprop through time (BPTT): vanishing and exploding gradient intuition`, later in this curriculum's Sequence Modeling content, names the exact exploding-gradient failure mode this guards against directly), where a rare but genuinely large gradient spike, left unclipped, can permanently destabilize an otherwise-healthy training run.

## Explanation

`compute_global_norm` sums every gradient array's own sum-of-squares into one running total, then takes a single square root, exactly the "as if concatenated" formula from Theory.

`clip_grad_norm` computes that global norm, derives `clip_coef = max_norm / (total_norm + eps)`, and either rescales every gradient array by that factor (if it's below `1.0`, meaning the real norm exceeded `max_norm`) or returns unmodified copies (if the gradient was already within budget).
