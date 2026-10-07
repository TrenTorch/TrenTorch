---
name: cosine-learning-rate-company-240
title: 'cosine-learning-rate — Adobe case'
tags: [problemset, dl-training-theory, learning-rate-schedules, adobe]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Adobe'
hint: 'lr_min + 0.5*(lr_max-lr_min)*(1+cos(pi*t/T))'
---

## Statement

Adobe-inspired model-training pipeline changes its learning rate over the course of a training schedule. You need to calculate the cosine-decayed learning rate at a requested training step so the scheduler matches the experiment configuration.

Compute the cosine-annealed learning rate at step `t` of `T`: $\eta_{\min}+\tfrac12(\eta_{\max}-\eta_{\min})\big(1+\cos(\pi t/T)\big)$. Note the argument order `(t, T, lr_max, lr_min)`. `t` is not clamped, so for $t>T$ the cosine starts rising again.

Implement `solve(t,T,lr_max,lr_min)`.

**Returns.** Return the learning rate as a Python float. `T` must be positive.

### Examples

**Example 1**

Input:

```python
solve(5, 10, 0.1, 0.0)
```

Output:

```text
0.05
```

**Example 2**

Input:

```python
solve(0, 10, 0.1, 0.01)
```

Output:

```text
0.1
```

**Example 3**

Input:

```python
solve(10, 10, 0.1, 0.01)
```

Output:

```text
0.01
```

## Theory

### The simple version

Cosine annealing lowers the learning rate along half a cosine wave: slowly at first, fastest in the middle and slowly again at the end, which settles training gently into a minimum.

### The formula

$$\eta_t=\eta_{\min}+\frac12(\eta_{\max}-\eta_{\min})\Big(1+\cos\frac{\pi t}{T}\Big)$$

## Explanation

At $t=0$ the cosine is $1$ and the rate is $\eta_{\max}$; at $t=T$ it is $-1$ and the rate is $\eta_{\min}$; halfway ($t=T/2$) $\cos(\pi/2)=0$ and the rate is the average of the two (first example, $0.05$).
