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

### Why it matters

- Conditional probabilities are how we ask "given that this happened, how likely is that?", the basis of Bayes' rule and of feature-conditional statistics.
- Estimating them from counts is the simplest form of learning from data.

### How it works

1. Keep only the cases where $B$ happened.
2. Among them, count the cases where $A$ also happened.
3. Divide; if $B$ never happened the answer is defined as $0$.

### Worked example

With $A=(1,0,1,1)$ and $B=(1,1,1,0)$, $B$ happens in cases 1, 2 and 3. $A$ is true in cases 1 and 3, so the estimate is $2/3=0.666667$.

## Explanation

The function counts joint occurrences and divides by how often $B$ occurred. When $B$ never occurs the ratio is $0/0$, so it returns `0.0` by convention.
