---
name: problem-120-xavier-initialization
title: 'Xavier Initialization'
tags: [problemset, dl-core, weight-initialization]
difficulty: Advanced
kind: problemset
relatedModule: 'part-deep-learning|Neural Networks'
topic: 'weight initialization'
hint: 'a = sqrt(6/(fan_in+fan_out)); rng.uniform(-a, a, (fan_in, fan_out))'
tools: [NumPy]
---

## Statement

Create a weight matrix with Xavier (Glorot) **uniform** initialisation: draw each entry from $U(-a,a)$ with $a=\sqrt{6/(\text{fan\_in}+\text{fan\_out})}$, using `np.random.default_rng(seed).uniform(-a, a, (fan_in, fan_out))`.

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
[[0.300068, -0.504372, -1.005677], [-1.059235, 0.686341, 0.904302]]
```

**Example 2**

Input:

```python
solve(1, 1, 5)
```

Output:

```text
[[1.056561]]
```

## Theory

### The simple version

If the initial weights are too large, signals blow up as they pass through the layers; if too small, they fade to nothing. Xavier initialisation picks the scale so that the variance of the activations (and of the gradients) stays roughly the same from layer to layer.

### The formula

$$W_{ij}\sim U(-a,a),\qquad a=\sqrt{\frac{6}{\text{fan}_{in}+\text{fan}_{out}}}\;\Longrightarrow\;\operatorname{Var}(W_{ij})=\frac{2}{\text{fan}_{in}+\text{fan}_{out}}$$

## Explanation

A uniform distribution on $(-a,a)$ has variance $a^2/3$, so this choice of $a$ gives the Glorot variance $2/(\text{fan}_{in}+\text{fan}_{out})$. It suits tanh and sigmoid layers; for ReLU the He initialisation (next problem) is preferred. The seed makes the result reproducible.
