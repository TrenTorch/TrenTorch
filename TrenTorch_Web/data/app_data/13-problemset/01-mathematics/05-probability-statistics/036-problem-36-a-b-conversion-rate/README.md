---
name: problem-36-a-b-conversion-rate
title: 'A/B Conversion Rate'
tags: [problemset, data-stats-for-ds, ab-testing]
difficulty: Advanced
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'ab testing'
hint: 'the mean of a 0/1 list is its conversion rate; lift is treatment minus control'
tools: [NumPy]
---

## Statement

Compute the conversion rate of a control group and a treatment group in an A/B test, and the absolute lift between them. Each group is a list of 0/1 outcomes (1 = the user converted).

Implement `solve(control, treatment)`.

**Returns.** Return a tuple `(control_rate, treatment_rate, lift)` of floats where `lift = treatment_rate - control_rate`. Each group must be a non-empty 1-D sequence of 0/1 values; otherwise `ValueError` is raised.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 0, 0, 1], [1, 1, 0, 1, 1])
```

Output:

```text
(0.4, 0.8, 0.4)
```

**Example 2**

Input:

```python
solve([1, 0, 0, 0], [1, 0, 0, 0])
```

Output:

```text
(0.25, 0.25, 0.0)
```

**Example 3**

Input:

```python
solve([0, 2], [1, 0])
```

Output: Raises `ValueError`.

## Theory

### The simple version

A conversion rate is just the fraction of users who did the thing you care about (sign up, buy, click). In an A/B test you compare that fraction between the group that saw the old version (control) and the group that saw the new one (treatment).

### The formulas

$$\hat p_c=\frac1{n_c}\sum_i c_i,\qquad \hat p_t=\frac1{n_t}\sum_j t_j,\qquad \text{lift}=\hat p_t-\hat p_c$$

### Why it matters

- An A/B test asks whether the new version converts better than the old one, so the first step is measuring both rates.
- The lift in percentage points is the number a product decision is made on.

### How it works

1. Average the control outcomes to get its rate.
2. Average the treatment outcomes to get its rate.
3. The lift is treatment minus control.

### Worked example

Control $(0,1,0,0,1)$ has two conversions in five, so rate $0.4$. Treatment $(1,1,0,1,1)$ has four in five, so rate $0.8$. The lift is $0.8-0.4=0.4$, giving (0.4, 0.8, 0.4).

## Explanation

Because the outcomes are 0/1, the mean of each group is exactly its conversion rate, so the groups may have different sizes. The lift is an absolute difference in percentage points, not a relative improvement. The function does not say whether the lift is statistically significant; that is what the tests in the neighbouring problems are for.
