---
name: problem-88-blended-prediction
title: 'Blended Prediction'
tags: [problemset, classical-ml-trees-ensembles, blending]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'blending'
hint: '(weights / weights.sum()) @ predictions'
tools: [NumPy]
---

## Statement

Blend the predictions of several models with fixed weights. `predictions` has shape `(n_models, n_samples)` and `weights` has one non-negative entry per model; the weights are normalised to sum to 1 before use.

Implement `solve(predictions,weights)`.

**Returns.** Return a NumPy array of length `n_samples`, the weighted average of the models' predictions.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [1.0, 3.0])
```

Output:

```text
[2.5, 3.5]
```

**Example 2**

Input:

```python
solve([[10.0, 20.0], [0.0, 0.0]], [1.0, 1.0])
```

Output:

```text
[5.0, 10.0]
```

## Theory

### The simple version

Blending is the simplest way to combine models: take a weighted average of their predictions, giving more weight to the ones you trust more. The weights are usually chosen on a validation set.

### The formula

$$\hat y=\sum_m\tilde w_m\,\hat y^{(m)},\qquad \tilde w_m=\frac{w_m}{\sum_k w_k}$$

### Why it matters

- Blending is the simplest ensemble: a weighted average that favours better models.
- Normalising the weights makes the result independent of their scale.

### How it works

1. Divide the weights by their sum.
2. Take the weighted sum of the predictions.

### Worked example

Weights $(1,3)$ normalise to $(0.25,0.75)$. First sample: $0.25\cdot1+0.75\cdot3=2.5$; second: $0.25\cdot2+0.75\cdot4=3.5$, so [2.5, 3.5].

## Explanation

Normalising the weights makes the result independent of their scale: weights `[1, 3]` and `[0.25, 0.75]` give the same blend. Equal weights reduce to a plain average.
