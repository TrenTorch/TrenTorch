---
name: problem-22-entropy-of-a-distribution
title: "Entropy of a Distribution"
tags: [problemset, maths-stats-for-ml, information-theory]
difficulty: Advanced
kind: problemset
relatedModule: "part-math|Information Theory"
topic: "information theory"
hint: "sum -p log2 p over positive probabilities"
tools: [NumPy]
---

# Entropy of a Distribution

## Statement

Implement `solve(p)`. Compute Shannon entropy in bits for a discrete probability vector. Zero-probability entries contribute zero.

## Theory

Shannon entropy is −Σ pᵢ log₂(pᵢ); the continuous extension at pᵢ=0 is zero.

## Explanation

Evaluate the specified sample or feature operation and return the result in the documented form. Inputs are passed directly to `solve`; no input parsing or printing is required.

## Examples

**Example 1**

Input:
```python
solve([0.25, 0.75])
```

Output:
```text
0.8112781244591328
```

**Example 2**

Input:
```python
solve([1.0, 0.0])
```

Output:
```text
-0.0
```
