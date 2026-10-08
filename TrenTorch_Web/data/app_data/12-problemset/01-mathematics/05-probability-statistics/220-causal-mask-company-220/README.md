---
name: causal-mask-company-220
title: 'causal-mask — Razorpay case'
tags: [problemset, transformer-llm, transformer-architecture, razorpay]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Razorpay'
hint: 'np.tril(np.ones((n, n), dtype=bool))'
tools: [NumPy]
---

## Statement

Razorpay-inspired transaction-sequence model must not allow a prediction at position t to inspect events that occur later in the sequence. You need to construct the causal attention mask that blocks those future positions.

Build the lower-triangular boolean mask of size $n\times n$: entry $(i,j)$ is `True` when position $i$ may look at position $j$, i.e. $j\le i$.

Implement `solve(n)`.

**Returns.** Return an $n\times n$ boolean NumPy array.

Build the lower-triangular boolean mask of size $n\times n$: entry $(i,j)$ is `True` when position $i$ may look at position $j$, i.e. $j\le i$.

Implement `solve(n)`.

**Returns.** Return an $n\times n$ boolean NumPy array.

### Examples

**Example 1**

Input:

```python
solve(3)
```

Output:

```text
[[True, False, False], [True, True, False], [True, True, True]]
```

**Example 2**

Input:

```python
solve(1)
```

Output:

```text
[[True]]
```

## Theory

### The simple version

A model that predicts the next event must not peek at later events. The causal mask lists, for every position, exactly which positions it is allowed to read: itself and everything before it. The forbidden entries are later replaced by a very negative number so the softmax gives them zero weight.

### The definition

$$M_{ij}=\mathbb 1[\,j\le i\,]$$

### Why it matters

- A model that predicts the next event must not peek at later events, or it would learn to copy the answer.
- The mask is applied before the softmax so the forbidden positions get zero attention weight.

### How it works

1. Make an $n\times n$ matrix of ones.
2. Keep the lower triangle, diagonal included, and zero the rest.

### Worked example

For $n=3$ position $0$ can see only itself, position $1$ sees positions $0$ and $1$, and position $2$ sees all three, so the mask is [[True, False, False], [True, True, False], [True, True, True]].

## Explanation

`np.tril` keeps the lower triangle, including the diagonal, of an all-true matrix. The diagonal is allowed because a position may use its own content.
