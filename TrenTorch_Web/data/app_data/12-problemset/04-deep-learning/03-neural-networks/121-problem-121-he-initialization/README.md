---
name: problem-121-he-initialization
title: 'He Initialization'
tags: [problemset, dl-core, weight-initialization]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'weight initialization'
hint: 'rng.normal(0, sqrt(2/fan_in), (fan_in, fan_out))'
tools: [NumPy]
---

## Statement

Create a weight matrix with He (Kaiming) **normal** initialisation: draw each entry from $\mathcal N(0,\,2/\text{fan\_in})$ using `np.random.default_rng(seed).normal(0, sqrt(2/fan_in), (fan_in, fan_out))`.

Implement `solve(fan_in,fan_out,seed=0)`.

**Returns.** Return a float NumPy array of shape `(fan_in, fan_out)`.

### Examples

**Example 1**

Input:

```python
solve(2, 3, 0)
```

Output:

```text
[[0.12573, -0.132105, 0.640423], [0.1049, -0.535669, 0.361595]]
```

**Example 2**

Input:

```python
solve(4, 1, 3)
```

Output:

```text
[[1.443148], [-1.807128], [0.295641], [-0.401474]]
```

## Theory

### The simple version

ReLU zeroes out half of its inputs, which halves the variance of the signal at every layer. He initialisation compensates by starting the weights with twice the variance that would otherwise keep the signal steady, which lets very deep ReLU networks train.

### The formula

$$W_{ij}\sim\mathcal N\!\Big(0,\;\frac{2}{\text{fan}_{in}}\Big)$$

## Explanation

The factor $2$ accounts for ReLU keeping only about half of the signal. The standard deviation passed to `rng.normal` is $\sqrt{2/\text{fan}_{in}}$, not the variance. Using `fan_in` (rather than the average with `fan_out`) preserves the variance of the forward pass.
