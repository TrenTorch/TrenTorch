---
name: problem-36-a-b-conversion-rate
title: "A/B Conversion Rate"
tags: [problemset, data-stats-for-ds, ab-testing]
difficulty: Advanced
kind: problemset
relatedModule: "part-data-foundations|Probability & Statistics"
topic: "ab testing"
hint: "count successes divided by group size"
tools: [NumPy]
---

# A/B Conversion Rate

## Statement

Implement `solve(control, treatment)`. Compute binary conversion rates for control and treatment groups and the absolute lift (treatment minus control).

## Theory

A group conversion rate is the mean of its binary outcomes; absolute lift is their difference.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve([0,1,1,0], [1,1,0,1])
```

Output:
```text
(0.5, 0.75, 0.25)
```

**Example 2**

Input:
```python
solve([1,1,1], [0,1,1])
```

Output:
```text
(1.0, 0.6666666666666666, -0.33333333333333337)
```
