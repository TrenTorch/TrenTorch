---
name: problem-38-sample-size-for-proportion
title: "Sample Size for Proportion"
tags: [problemset, data-stats-for-ds, experiment-design]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "experiment design"
hint: "use the standard normal-approximation formula"
tools: [NumPy]
---

# Sample Size for Proportion

## Statement

Implement `solve(p1, p2)`. Estimate the required sample size per arm for a two-sided test of two proportions, using z=1.96 and power z=0.84.

## Theory

The normal-approximation formula combines the null pooled variance and the two alternative variances, then divides by squared effect size.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve(0.10, 0.20)
```

Output:
```text
398
```

**Example 2**

Input:
```python
solve(0.50, 0.55)
```

Output:
```text
3126
```
