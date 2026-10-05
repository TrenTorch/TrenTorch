---
name: problem-111-sigmoid-activation
title: 'Sigmoid Activation'
tags: [problemset, dl-core, activation-functions]
difficulty: Beginner
kind: problemset
relatedModule: 'part-deep-learning|Activation Functions'
topic: 'activation functions'
hint: 'use a numerically stable branch'
tools: [NumPy]
---

## Statement

111 Sigmoid Activation. Apply sigmoid elementwise, returning 1/(1+exp(−x)) with the same shape as x. Use a numerically stable computation for large positive or negative inputs.

### Function signature

```python
solve(x)
```

### Examples

### Examples

**Example 1**

**Input**

```python
solve(x=[-1, 0, 1])
```

**Output**

```python
[0.2689414214, 0.5, 0.7310585786]
```

**Example 2**

**Input**

```python
solve(x=[-1000, 1000])
```

**Output**

```python
[0.0, 1.0]
```

### Constraints

Inputs must follow the shapes and types described above. Arrays are NumPy-compatible values. No output is printed.

## Theory

The sigmoid maps real values to (0, 1) and is commonly used to convert logits into binary probabilities.

## Explanation

Using exp(−|x|) avoids overflow. Select 1/(1+exp(−|x|)) for nonnegative values and exp(−|x|)/(1+exp(−|x|)) for negative values.
