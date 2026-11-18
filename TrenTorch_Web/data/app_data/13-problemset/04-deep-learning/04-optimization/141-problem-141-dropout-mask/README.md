---
name: problem-141-dropout-mask
title: 'Dropout Mask'
tags: [problemset, dl-training-theory, regularization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'regularization'
hint: 'mask = rng.random(shape) < keep_prob; return x * mask / keep_prob'
tools: [NumPy]
---

## Statement

Apply **inverted dropout** to activations `x` during training. Draw a keep-mask with `np.random.default_rng(seed).random(x.shape) < keep_prob`, zero out the dropped entries, and divide the survivors by `keep_prob` so the expected value of each activation is unchanged.

Implement `solve(x, keep_prob, seed=0)`.

**Returns.** Return a NumPy array with the shape of `x`. `keep_prob` must lie in $(0,1]$, otherwise `ValueError` is raised; `keep_prob=1` returns `x` unchanged.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0, 4.0], 0.5, 0)
```

Output:

```text
[0.0, 4.0, 6.0, 8.0]
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0], 1.0, 0)
```

Output:

```text
[1.0, 2.0, 3.0]
```

**Example 3**

Input:

```python
solve([1.0, 2.0], 0.0, 0)
```

Output: Raises `ValueError`.

## Theory

### The simple version

Dropout randomly switches off a fraction of the neurons on every training step. The network cannot rely on any single neuron, so it learns more robust, redundant features, which reduces overfitting.

### Why divide by `keep_prob`

If each activation survives with probability $p$, its expected value shrinks to $p\,x$. Dividing the survivors by $p$ makes $\mathbb E[\tilde x]=x$ again, so nothing needs to change at test time, when dropout is simply switched off.

$$\tilde x_i=\frac{m_i\,x_i}{p},\qquad m_i\sim\text{Bernoulli}(p)$$

### Why it matters

- Dropout stops neurons from relying on each other, which reduces overfitting.
- Dividing the survivors by `keep_prob` keeps the expected activation the same, so nothing changes at inference.

### How it works

1. Draw a uniform number for every entry with the seeded generator.
2. Keep the entries whose draw is below `keep_prob`.
3. Zero the others and divide the survivors by `keep_prob`.

### Worked example

With `keep_prob=0.5` and seed $0$ the first entry's draw ($0.64$) is above $0.5$, so $1$ is dropped; the other three draws are below $0.5$, so $2,3,4$ are kept and doubled: [0.0, 4.0, 6.0, 8.0].

## Explanation

With $p=0.5$ the kept entries are doubled and the others are zero (first example). The mask depends on the seed, so the same seed gives the same mask. `keep_prob=0` would divide by zero (everything is dropped), so it is rejected.
