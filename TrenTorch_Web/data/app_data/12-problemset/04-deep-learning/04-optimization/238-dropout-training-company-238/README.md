---
name: dropout-training-company-238
title: 'dropout-training — Oracle case'
tags: [problemset, dl-training-theory, regularization-dl, oracle]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Oracle'
hint: 'mask = rng.random(shape) >= p; return x * mask / (1 - p)'
tools: [NumPy]
---

## Statement

Oracle-inspired neural-network training experiment uses dropout to reduce reliance on individual activations. You need to apply inverted dropout during training so the expected activation scale remains consistent with inference.

Apply inverted dropout with **drop probability** `p`: draw `np.random.default_rng(seed).random(x.shape)`, keep the entries where the draw is `>= p`, zero the others and divide the survivors by $1-p$. `p` must satisfy $0\le p<1$, otherwise `ValueError` is raised.

Implement `solve(x, p, seed=0)`.

**Returns.** Return a float NumPy array with the shape of `x`.

Apply inverted dropout with **drop probability** `p`: draw `np.random.default_rng(seed).random(x.shape)`, keep the entries where the draw is `>= p`, zero the others and divide the survivors by $1-p$. `p` must satisfy $0\le p<1$, otherwise `ValueError` is raised.

Implement `solve(x, p, seed=0)`.

**Returns.** Return a float NumPy array with the shape of `x`.

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3, 4], 0.5)
```

Output:

```text
[2.0, 0.0, 0.0, 0.0]
```

**Example 2**

Input:

```python
solve([1.0, 2.0], 0.0)
```

Output:

```text
[1.0, 2.0]
```

**Example 3**

Input:

```python
solve([1.0], 1.0)
```

Output: Raises `ValueError`.

## Theory

### The simple version

Dropout switches off a random fraction $p$ of the activations on each training step so the network cannot rely on any one of them. The survivors are multiplied by $1/(1-p)$ ("inverted" dropout) so the expected value of every activation stays the same, which means inference needs no change at all.

### The formula

$$\tilde x_i=\frac{m_i\,x_i}{1-p},\qquad m_i=\mathbb 1[u_i\ge p],\;u_i\sim U(0,1)$$

### Why it matters

- Dropout stops units from relying on each other, which reduces overfitting.
- Dividing the survivors by $1-p$ keeps the expected activation unchanged, so inference needs no change.

### How it works

1. Draw a uniform number for every entry with the seeded generator.
2. Keep entries whose draw is at least $p$.
3. Zero the rest and divide the survivors by $1-p$.

### Worked example

With $p=0.5$ and seed $0$ the draws are about $(0.64,0.27,0.04,0.02)$. Only the first is at least $0.5$, so only $1$ survives and is doubled: [2.0, 0.0, 0.0, 0.0].

## Explanation

Here `p` is the probability of _dropping_ a unit, the opposite of the `keep_prob` used in the earlier dropout problem. `p=0` keeps everything (second example) and `p=1` would drop everything and divide by zero, so it is rejected. The mask is determined by the seed.
