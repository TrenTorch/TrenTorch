---
name: relu-layer-company-213
title: 'relu-layer — OpenAI case'
tags: [problemset, dl-core, activation-functions, openai]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'OpenAI'
hint: 'np.maximum(x, 0)'
tools: [NumPy]
---

## Statement

OpenAI-inspired neural-network experiment needs a simple nonlinear activation between two learned transformations. You need to apply ReLU elementwise so the team can verify the forward-pass behavior before moving to a larger architecture.

Replace every negative entry with $0$ and keep the others: $\max(0,x)$ element-wise.

Implement `solve(x)`.

**Returns.** Return a float NumPy array of the same shape.

### Examples

**Example 1**

Input:

```python
solve([-2, 0, 3])
```

Output:

```text
[0.0, 0.0, 3.0]
```

**Example 2**

Input:

```python
solve([[1.5, -0.5], [-3.0, 4.0]])
```

Output:

```text
[[1.5, 0.0], [0.0, 4.0]]
```

## Theory

### The simple version

Two linear layers stacked together are just one bigger linear layer, so a network needs a non-linearity in between to represent anything more interesting. ReLU is the simplest: it keeps positive signals and silences negative ones.

### The formula

$$\operatorname{ReLU}(x)=\max(0,x)$$

## Explanation

Because ReLU acts on each entry independently, it works for arrays of any shape. It is cheap, and its derivative is just $0$ or $1$, which keeps gradients from shrinking for active units.
