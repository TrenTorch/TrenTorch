---
name: standardize-column-company-224
title: 'standardize-column — Shopify case'
tags: [problemset, data-stats-for-ds, data-cleaning, shopify]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Shopify'
hint: '(x - mean) / std, zeros if std is 0'
tools: [NumPy]
---

## Statement

Shopify-inspired forecasting pipeline combines numerical features collected from merchants with different units and scales. You need to standardize a feature using its mean and standard deviation so the training pipeline receives a consistent representation.

Standardise one feature: subtract its mean and divide by its **population** standard deviation. A constant feature is mapped to zeros.

Implement `solve(x)`.

**Returns.** Return a float NumPy vector with mean $0$ and standard deviation $1$ (or all zeros for a constant input).

Standardise one feature: subtract its mean and divide by its **population** standard deviation. A constant feature is mapped to zeros.

Implement `solve(x)`.

**Returns.** Return a float NumPy vector with mean $0$ and standard deviation $1$ (or all zeros for a constant input).

### Examples

**Example 1**

Input:

```python
solve([1, 2, 3])
```

Output:

```text
[-1.224745, 0.0, 1.224745]
```

**Example 2**

Input:

```python
solve([4.0, 4.0, 4.0])
```

Output:

```text
[0.0, 0.0, 0.0]
```

## Theory

### The simple version

Features in different units (rupees, minutes, counts) should not dominate a model merely because their numbers are bigger. Standardising expresses each value as "how many standard deviations from the average", putting all features on a common scale.

### The formula

$$z_i=\frac{x_i-\mu}{\sigma}$$

### Why it matters

- Features in different units (rupees, minutes, counts) should not dominate a model just because their numbers are larger.
- Standardised values read as "standard deviations from the mean", so features become directly comparable.

### How it works

1. Compute the mean and the population standard deviation.
2. Subtract the mean and divide by the standard deviation.
3. A constant feature maps to zeros.

### Worked example

For $(1,2,3)$ the mean is $2$ and $\sigma=\sqrt{2/3}=0.8165$. The values become $-1/0.8165$, $0$ and $1/0.8165$, which is [-1.224745, 0.0, 1.224745].

## Explanation

For $[1,2,3]$ the mean is $2$ and the population standard deviation is $\sqrt{2/3}$, giving $\approx(-1.2247,0,1.2247)$. A constant feature has $\sigma=0$; mapping it to zeros avoids `nan` and reflects that it carries no information.
