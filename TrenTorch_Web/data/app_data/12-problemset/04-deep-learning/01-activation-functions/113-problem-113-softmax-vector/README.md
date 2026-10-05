---
name: problem-113-softmax-vector
title: 'Softmax Vector'
tags: [problemset, dl-core, activation-functions]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'subtract the maximum logit before exponentiation'
tools: [NumPy]
---

## Statement

113 Softmax Vector. Convert a one-dimensional vector of logits x into probabilities with softmax. Return exp(xᵢ−max(x))/sumⱼ exp(xⱼ−max(x)); the output sums to one.

### Function signature

```python
solve(x)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(x=[1, 2, 3])
```

**Output**

```python
[0.0900305732, 0.2447284711, 0.6652409558]
```

**Example 2**

**Input**

```python
solve(x=[0, 0])
```

**Output**

```python
[0.5, 0.5]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

Softmax converts a vector of unnormalized scores into a categorical probability distribution. Adding the same constant to every logit leaves the probabilities unchanged.

## Explanation

Subtract the maximum logit before exponentiation, then divide each shifted exponential by their sum.
