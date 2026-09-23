---
name: potd-utilization-nudge-sgd-step
title: 'THE UTILIZATION NUDGE'
tags: [optimization]
difficulty: Beginner
---

## Statement

**Difficulty:** Easy
**Tags:** Optimization

---

### Story

NVIDIA's internal GPU-scheduler team tunes a lightweight utilization-prediction model with plain
SGD before ever touching anything fancier. Every optimizer in the more advanced tracks builds on
getting this single update exactly right.

---

### The Math

```
theta <- theta - eta * grad
```

### Input Format

```
d eta
theta_1 ... theta_d
grad_1 ... grad_d
```

### Output Format

Updated `theta`, `d` values, 6 decimals.

### Constraints

- `1 <= d <= 10^4`
- Time limit: 1.0 second.

---

### Example

**Input**

```
2 0.1
1.0 2.0
0.2 -0.1
```

**Output**

```
0.980000 2.010000
```

## Theory

### The simple version

Gradient descent nudges every parameter a little bit in the direction that reduces the loss, by an amount the learning rate controls. Do that once, and you have taken one training step.

### This is the whole optimizer

There is no momentum term, no second moment, no decay: one elementwise multiply and one elementwise
subtract, applied to the whole parameter vector at once.

### `eta = 1`

At `eta = 1` the step equals the full negative gradient exactly. This is a good check that the
scale of the step is right: a solution that accidentally applies `eta` twice, or not at all, is
caught immediately at this value.

### A zero gradient changes nothing

If every entry of `grad` is `0`, the update leaves `theta` exactly as it was, bit for bit, since
subtracting `eta * 0` is subtracting `0`.

## Explanation

`sgd_step` returns `theta - eta * grad` as one vectorized NumPy expression over the whole parameter
vector. At `d = 10^4` this is still a single array operation, not a per-element Python loop, which
is the difference this problem is checking for since every later, more complex optimizer in this
track builds on this same elementwise update running at vector scale.
