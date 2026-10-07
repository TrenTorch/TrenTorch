---
name: problem-133-softmax-temperature
title: 'Softmax Temperature'
tags: [problemset, dl-core, attention---activations]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'attention / activations'
hint: 'softmax(logits / temperature) with the max subtracted'
tools: [NumPy]
---

## Statement

Apply softmax with a temperature to a vector of logits: divide the logits by `temperature`, then take a numerically stable softmax. The temperature must be positive.

Implement `solve(logits,temperature)`.

**Returns.** Return a NumPy vector of probabilities that sums to 1.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0, 3.0], 1.0)
```

Output:

```text
[0.090031, 0.244728, 0.665241]
```

**Example 2**

Input:

```python
solve([1.0, 2.0, 3.0], 0.5)
```

Output:

```text
[0.015876, 0.11731, 0.866813]
```

**Example 3**

Input:

```python
solve([1.0, 2.0, 3.0], 100.0)
```

Output:

```text
[0.330006, 0.333322, 0.336672]
```

## Theory

### The simple version

Temperature controls how decisive a softmax is. Low temperatures sharpen the distribution toward the largest logit (more greedy), while high temperatures flatten it toward uniform (more random). Language models use it to tune the creativity of sampling.

### The formula

$$p_i=\frac{e^{z_i/T}}{\sum_je^{z_j/T}}$$

## Explanation

$T=1$ is ordinary softmax. As $T\to0$ all the mass goes to the largest logit, and as $T\to\infty$ the output approaches the uniform distribution (third example). The maximum is subtracted before exponentiating for numerical stability.
