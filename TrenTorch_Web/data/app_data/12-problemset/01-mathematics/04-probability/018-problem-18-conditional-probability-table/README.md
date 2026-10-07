---
name: problem-18-conditional-probability-table
title: 'Conditional Probability Table'
tags: [problemset, maths-stats-for-ml, probability]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-mathematics|Probability'
topic: 'probability'
hint: 'count A and B together, divide by the count of B'
tools: [NumPy]
---

## Statement

Estimate $P(A\mid B)$ from paired binary observations: among the cases where $B$ happened, the fraction where $A$ also happened.

Implement `solve(A, B)`.

**Returns.** Return a float. Any non-zero entry counts as true. If $B$ never occurs the conditional probability is undefined and the function returns `0.0`.

### Examples

**Example 1**

Input:

```python
solve([1, 0, 1, 1], [1, 1, 1, 0])
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([1, 1], [0, 0])
```

Output:

```text
0.0
```

## Theory

### The simple version

Conditional probability restricts attention to the cases where the condition holds and asks how often the other event also holds in those cases.

### The formula

$$P(A\mid B)=\frac{\#(A\wedge B)}{\#B}$$

## Explanation

The function counts joint occurrences and divides by how often $B$ occurred. When $B$ never occurs the ratio is $0/0$, so it returns `0.0` by convention.
