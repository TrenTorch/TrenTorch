---
name: potd-gradient-seatbelt-clipping
title: 'THE GRADIENT SEATBELT'
tags: [optimization]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Optimization

---

### Story

PayPal's fraud model occasionally sees gradient spikes from rare, extreme-value transactions.
Global-norm gradient clipping is the seatbelt that keeps one outlier batch from blowing up training.

---

### The Math

```
if ||g||_2 > tau:
    g <- g * (tau / ||g||_2)
else:
    g <- g
```

### Input Format

```
d tau
g_1 ... g_d
```

### Output Format

Clipped gradient, `d` values, 6 decimals.

### Constraints

- `1 <= d <= 10^4`, `tau > 0`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2 2.0
3.0 4.0
```

**Output**

```
1.200000 1.600000
```

**Explanation:** `||g||_2 = 5.0 > tau = 2.0`, so scale by `2.0/5.0 = 0.4`:
`(3.0, 4.0) * 0.4 = (1.2, 1.6)`.

## Theory

### The simple version

Occasionally a gradient is enormous, from one strange batch of data, and taking a step that large would wreck training. Clipping shrinks any gradient that is too large back down to a fixed maximum size, without changing its direction.

### The boundary is strict

Clipping triggers only when `||g||_2 > tau`, strictly. At exact equality (`||g||_2 == tau`), the
gradient passes through unchanged. A `>=` implementation would silently pass every other test and
fail only this specific boundary case, this mirrors the exact convention a real framework's
gradient-clipping function uses.

### Below the threshold, nothing changes

If `||g||_2` is well below `tau`, the gradient is returned exactly as given, not merely
approximately: no scaling is applied at all in that branch.

### A zero gradient has nothing to clip

An all-zero gradient has norm `0`, which is never greater than a positive `tau`, so it takes the
unchanged branch and stays all zero. There is no risk of dividing by a zero norm here, because
that division only happens inside the branch that is only reached when the norm exceeds `tau`,
and `tau > 0` by the constraints.

## Explanation

`clip_grad_norm` computes `norm = np.linalg.norm(g)` once. If `norm > tau` it returns
`g * (tau / norm)`, the rescaled gradient; otherwise it returns `g` unchanged. Because the division
`tau / norm` only ever executes inside the `norm > tau` branch, and `tau` is guaranteed positive,
there is no zero-norm division to guard against separately, the strict inequality that decides
whether to clip is the same check that keeps the division safe.
