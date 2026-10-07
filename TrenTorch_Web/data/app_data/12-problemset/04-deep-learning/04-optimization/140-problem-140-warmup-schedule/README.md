---
name: problem-140-warmup-schedule
title: 'Warmup Schedule'
tags: [problemset, dl-training-theory, learning-rate-schedules]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'learning-rate schedules'
hint: 'linear (t+1)/warmup before warmup; then cosine over the remaining T - warmup steps'
tools: [NumPy]
---

## Statement

Compute a learning rate with linear warm-up followed by cosine decay. For steps `t < warmup` the rate is `lr0 * (t + 1) / warmup`. From `t = warmup` on, with $q=\min(t-\text{warmup},\,\max(1,T-\text{warmup}))$, the rate is $\eta_{\min}+\tfrac12(\eta_0-\eta_{\min})\big(1+\cos(\pi q/\max(1,T-\text{warmup}))\big)$.

Implement `solve(lr0, min_lr, t, warmup, T)`.

**Returns.** Return the learning rate as a float. It reaches `lr0` at `t = warmup - 1` and again at `t = warmup`, then decays to `min_lr` at `t = T`.

### Examples

**Example 1**

Input:

```python
solve(1.0, 0.1, 0, 2, 6)
```

Output:

```text
0.5
```

**Example 2**

Input:

```python
solve(1.0, 0.1, 2, 2, 6)
```

Output:

```text
1.0
```

**Example 3**

Input:

```python
solve(1.0, 0.1, 6, 2, 6)
```

Output:

```text
0.1
```

## Theory

### The simple version

At the start of training the weights are random and gradients are erratic, so jumping in with the full learning rate can destabilise the run. Warm-up begins with a small rate and raises it linearly, and afterwards a cosine curve brings it smoothly down. Transformers are almost always trained this way.

### The schedule

$$\eta_t=\begin{cases}\eta_0\,\dfrac{t+1}{w}&t<w\\[2mm]\eta_{\min}+\tfrac12(\eta_0-\eta_{\min})\big(1+\cos\frac{\pi q}{T-w}\big)&t\ge w\end{cases}$$

## Explanation

In the first example, step 0 of a 2-step warm-up is $1\cdot1/2=0.5$. The cosine phase starts at its peak ($q=0$, the second example gives $1.0$) and ends at the minimum when $t=T$ (third example gives $0.1$). Steps beyond $T$ stay at the minimum because $q$ is capped.
