---
name: problem-149-random-search-sampler
title: 'Random Search Sampler'
tags: [problemset, dl-training-theory, hyperparameter-tuning]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'hyperparameter tuning'
hint: 'per config: lr = 10**rng.uniform(-5,-1), then depth = rng.integers(2,10)'
tools: [NumPy]
---

## Statement

Generate `n` reproducible random-search configurations with `np.random.default_rng(seed)`. For each configuration, in order, draw the learning rate as `10 ** rng.uniform(-5, -1)` and then the tree depth as `rng.integers(2, 10)`.

Implement `solve(n, seed=0)`.

**Returns.** Return a list of `n` dicts `{'lr': float, 'depth': int}` with `lr` between $10^{-5}$ and $10^{-1}$ and `depth` between 2 and 9.

### Examples

**Example 1**

Input:

```python
solve(2, seed=0)
```

Output:

```text
[{'lr': 0.003531, 'depth': 6}, {'lr': 1.5e-05, 'depth': 4}]
```

**Example 2**

Input:

```python
solve(1, seed=7)
```

Output:

```text
[{'lr': 0.003165, 'depth': 7}]
```

## Theory

### The simple version

Random search tries random hyper-parameter settings instead of a full grid. It often finds good settings faster than grid search because usually only a few hyper-parameters really matter, and random sampling tests many more distinct values of those few.

### Log-uniform sampling

Learning rates span orders of magnitude, so the exponent is sampled uniformly: $\eta=10^{u}$ with $u\sim U(-5,-1)$. That makes $10^{-4}$ as likely as $10^{-2}$.

## Explanation

The learning rate and depth are drawn one after another from the same generator, so the sequence of configurations is fully determined by the seed. Sampling `lr` directly from $U(10^{-5},10^{-1})$ instead would almost never try values below $10^{-3}$.
