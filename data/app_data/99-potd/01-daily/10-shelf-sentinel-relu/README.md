---
name: potd-shelf-sentinel-relu
title: 'SHELF SENTINEL'
tags: [activation-functions, autograd]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Activation Functions, Autograd

---

### Story

Walmart's smart-shelf sensors report a raw weight-delta signal every time an item is picked up or
placed back, and that signal is noisy in both directions: small negative jitters from shelf
vibration, and clean positive spikes from genuine removals. Before this feeds the restock-trigger
model, every value below zero must be clamped away. You are implementing the exact ReLU layer used
in the sensor-ingestion pipeline, forward and backward.

---

### The Math

```
f(x) = max(0, x)         forward
f'(x) = 1 if x > 0 else 0   backward
```

Given a batch of raw readings `x` and, separately, an upstream gradient `g` from the next layer,
compute the forward activation and the backward gradient `g * f'(x)`.

---

### Input Format

```
n
x_1 x_2 ... x_n
g_1 g_2 ... g_n
```

### Output Format

Two lines: the activated values, then the backward gradient, each space-separated to 6 decimal
places.

### Constraints

- `1 <= n <= 10^5`
- Time limit: 1.0 second. Memory: 64 MB.

---

### Example

**Input**

```
5
-2.0 0.0 3.0 -0.5 1.5
1.0 1.0 1.0 1.0 1.0
```

**Output**

```
0.000000 0.000000 3.000000 0.000000 1.500000
0.000000 0.000000 1.000000 0.000000 1.000000
```

## Theory

### The simple version

ReLU is a light switch: a negative input keeps the light off, a positive input lets it shine exactly as bright as the input itself. The backward pass just remembers whether the switch was on.

### Exactly zero is not activated

The subgradient convention every major framework uses is strict: `x = 0` maps to a backward
gradient of `0`, not `1`. Test `x > 0`, never `x >= 0`.

### The backward pass never touches the values

The backward pass does not look at the activated output at all, only at whether the _input_ was
positive. A gradient multiplied by a mask, not by the forward result: `g * (x > 0)`.

### An all-negative batch is not a bug

If every value in the batch is negative, both output lines are entirely zero. That is the correct
answer, not a sign that something upstream broke.

## Explanation

`relu_forward` builds the mask `x > 0` once and reuses it for both halves of the answer:
`np.where(mask, x, 0.0)` for the activation, and `g * mask` for the backward gradient. Building the
mask once means the forward and backward pass agree on the boundary by construction: there is no
way for `x = 0` to activate `0.0` in the forward pass but leak a nonzero gradient in the backward
pass, because both read the same boolean array.
