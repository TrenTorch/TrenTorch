---
name: problem-3-cosine-similarity
title: "Cosine Similarity"
tags: [problemset, maths-stats-for-ml, linear-algebra]
difficulty: Beginner
kind: problemset
relatedModule: "part-math|Linear Algebra"
topic: "linear algebra"
hint: "reuse the two norms and guard against a zero vector"
tools: [NumPy]
---

# Cosine Similarity

## Statement

Implement `solve(a, b)`. Compute cosine similarity for two equal-length vectors. If either vector is zero, return 0.0.

## Theory

Cosine similarity is the dot product divided by the product of Euclidean lengths; it measures angle rather than magnitude.

## Explanation

Convert the inputs to numeric arrays where appropriate, apply the stated operation, and return its result without printing. The examples show the required argument order and output form.

## Examples

**Example 1**

Input:
```python
solve([1.0, 0.0], [0.0, 1.0])
```

Output:
```text
0.0
```

**Example 2**

Input:
```python
solve([1.0, 2.0], [2.0, 4.0])
```

Output:
```text
0.9999999999999998
```
