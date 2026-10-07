---
name: problem-60-f1-score
title: 'F1 Score'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: '2*p*r/(p+r), with 0.0 when p+r is 0'
tools: [NumPy]
---

## Statement

Compute the F1 score, the harmonic mean of precision and recall.

Implement `solve(precision, recall)`.

**Returns.** Return a float in $[0,1]$. If precision and recall are both $0$ return `0.0`.

### Examples

**Example 1**

Input:

```python
solve(0.5, 0.5)
```

Output:

```text
0.5
```

**Example 2**

Input:

```python
solve(1.0, 0.25)
```

Output:

```text
0.4
```

**Example 3**

Input:

```python
solve(0.0, 0.0)
```

Output:

```text
0.0
```

## Theory

### The simple version

F1 squeezes precision and recall into one number. It uses the _harmonic_ mean, which is dragged toward the smaller of the two, so you cannot get a high F1 by being great at one and terrible at the other.

### The formula

$$F_1=\frac{2PR}{P+R}$$

## Explanation

With $P=1$ and $R=0.25$ the arithmetic mean would be $0.625$, but F1 is only $0.4$, reflecting the weak recall. The zero guard prevents $0/0$ when both inputs are zero.
