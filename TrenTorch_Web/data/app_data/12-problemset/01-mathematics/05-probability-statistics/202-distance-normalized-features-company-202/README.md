---
name: distance-normalized-features-company-202
title: 'distance-normalized-features — Uber case'
tags: [problemset, maths-stats-for-ml, linear-algebra, uber]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Uber'
hint: 'divide by the L2 norm (leave a zero vector as zeros)'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Uber** ranking and experimentation team might handle; it is not a real interview question or a claim that Uber uses this exact task. The team needs a reliable implementation for embedding preprocessing in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Normalize each numeric feature vector to unit L2 norm before it enters a similarity model.

Scale the vector so its Euclidean (L2) length is exactly 1 while its direction stays the same. The all-zero vector has no direction, so it is returned unchanged.

Implement `solve(x)`.

**Returns.** Return a float NumPy vector of the same shape.

### Examples

**Example 1**

Input:

```python
solve([3.0, 4.0])
```

Output:

```text
[0.6, 0.8]
```

**Example 2**

Input:

```python
solve([0.0, 0.0])
```

Output:

```text
[0.0, 0.0]
```

## Theory

### The simple version

After L2 normalisation only the _direction_ of a vector matters, not its size. That is what similarity search wants: the dot product of two unit vectors is their cosine similarity, regardless of how large the raw embeddings were.

### The formula

$$\hat x=\frac{x}{\|x\|_2}$$

## Explanation

The vector $(3,4)$ has length $5$, so it becomes $(0.6,0.8)$. A zero vector would require $0/0$; returning zeros avoids `nan` flowing into the similarity model.
