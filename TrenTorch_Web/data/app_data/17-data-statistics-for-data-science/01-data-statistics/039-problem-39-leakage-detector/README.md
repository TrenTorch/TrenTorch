---
name: problem-39-leakage-detector
title: "Leakage Detector"
tags: [problemset, data-stats-for-ds, data-leakage]
difficulty: Beginner
kind: problemset
relatedModule: "part-data-foundations|Data Processing"
topic: "data leakage"
hint: "flag names matching a supplied forbidden pattern list"
tools: [NumPy]
---

# Leakage Detector

## Statement

Implement `solve(columns)`. Return the feature names containing one of the leakage markers: target, label, future, outcome, or post_. Matching is case-insensitive and preserves input order.

## Theory

Leakage screening applies case-insensitive substring checks for names that may encode a target or future information.

## Explanation

The output is computed from the supplied observations using the method above. Values and arrays are passed directly as arguments; the function returns its result without printing.

## Examples

**Example 1**

Input:
```python
solve(["age", "future_label", "score"])
```

Output:
```text
['future_label']
```

**Example 2**

Input:
```python
solve(["post_clicks", "region", "TARGET_flag"])
```

Output:
```text
['post_clicks', 'TARGET_flag']
```
