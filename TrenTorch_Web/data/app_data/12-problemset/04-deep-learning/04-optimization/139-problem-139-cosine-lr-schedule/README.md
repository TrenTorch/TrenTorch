---
name: problem-139-cosine-lr-schedule
title: 'Cosine LR Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'min_lr + 0.5*(lr0-min_lr)*(1+cos(pi*t/T)), with t clamped to [0, T]'
tools: [NumPy]
---

## Statement

Compute the cosine-annealed learning rate at step `t` of `T`: $\eta_{\min}+\tfrac12(\eta_0-\eta_{\min})\big(1+\cos(\pi t/T)\big)$. `t` is clamped to $[0,T]$; if `T <= 0` the rate is `min_lr`.

Implement `solve(lr0, min_lr, t, T)`.

**Returns.** Return the learning rate as a float, starting at `lr0` for $t=0$ and ending at `min_lr` for $t=T$.

### Examples

**Example 1**

Input:

```python
solve(5.0, 1.0, 0, 10)
```

Output:

```text
5.0
```

**Example 2**

Input:

```python
solve(5.0, 1.0, 5, 10)
```

Output:

```text
3.0
```

**Example 3**

Input:

```python
solve(5.0, 1.0, 10, 10)
```

Output:

```text
1.0
```

## Theory

### The simple version

Cosine annealing lowers the learning rate along half a cosine wave: slowly at first, fastest in the middle, and slowly again as it approaches the minimum. It is a popular schedule because it needs few hyper-parameters and ends gently.

### The formula

$$\eta_t=\eta_{\min}+\frac12(\eta_0-\eta_{\min})\Big(1+\cos\frac{\pi t}{T}\Big)$$

### Why it matters

- Cosine annealing decays smoothly with few hyper-parameters.
- It ends gently at the minimum.

### How it works

1. Clamp $t$ to $[0,T]$.
2. $\eta_{\min}+\tfrac12(\eta_0-\eta_{\min})(1+\cos(\pi t/T))$.

### Worked example

At $t=0$: $\cos0=1$, so $1+\tfrac12\cdot4\cdot2=5$ i.e. 5.0. At $t=5$ of $10$ the cosine is $0$ and the rate is $3$.

## Explanation

At $t=0$ the cosine is $1$ and the rate is $\eta_0$; at $t=T$ it is $-1$ and the rate is $\eta_{\min}$; halfway it is the average of the two ($3.0$ in the second example). Clamping $t$ keeps the rate at the minimum if training runs past $T$ steps.
