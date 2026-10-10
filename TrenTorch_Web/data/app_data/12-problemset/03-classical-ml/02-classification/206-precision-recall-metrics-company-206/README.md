---
name: precision-recall-metrics-company-206
title: 'precision-recall-metrics — Amazon case'
tags: [problemset, classical-ml, metrics-and-evaluation, amazon]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'Classification'
caseCompany: 'Amazon'
hint: 'TP, FP, FN counts; guard each division'
tools: [NumPy]
---

## Statement

This is a hypothetical engineering scenario inspired by the kind of work a **Amazon** ranking and experimentation team might handle; it is not a real interview question or a claim that Amazon uses this exact task. The team needs a reliable implementation for fraud alert evaluation in a production-oriented ML workflow. A small implementation error can change the model input or metric enough to make a downstream result misleading.

Given binary predictions and labels, compute precision and recall without using a metrics library.

Count true positives, false positives and false negatives (label `1` is positive) and return precision and recall. A ratio whose denominator is zero is reported as `0.0`.

Implement `solve(y_true,y_pred)`.

**Returns.** Return a tuple `(precision, recall)` of Python floats.

Count true positives, false positives and false negatives (label `1` is positive) and return precision and recall. A ratio whose denominator is zero is reported as `0.0`.

Implement `solve(y_true,y_pred)`.

**Returns.** Return a tuple `(precision, recall)` of Python floats.

### Examples

**Example 1**

Input:

```python
solve([1, 1, 0, 0], [1, 0, 1, 0])
```

Output:

```text
(0.5, 0.5)
```

**Example 2**

Input:

```python
solve([1, 1, 0], [0, 0, 0])
```

Output:

```text
(0.0, 0.0)
```

## Theory

### The simple version

For fraud alerts, precision answers "of the alerts we raised, how many were real fraud?" and recall answers "of all the real fraud, how much did we catch?". Raising more alerts catches more fraud (recall up) but also wastes more analyst time (precision down).

### The formulas

$$\text{precision}=\frac{TP}{TP+FP},\qquad \text{recall}=\frac{TP}{TP+FN}$$

### Why it matters

- For fraud alerts, precision measures wasted analyst time and recall measures missed fraud.
- Which matters more depends on the cost of each kind of mistake.

### How it works

1. Count true positives, false positives and false negatives.
2. Precision $=TP/(TP+FP)$ and recall $=TP/(TP+FN)$.
3. Report $0$ when a denominator is $0$.

### Worked example

Labels $(1,1,0,0)$ and predictions $(1,0,1,0)$ give one true positive, one false positive (third item) and one false negative (second item). Both ratios are $1/2$: (0.5, 0.5).

## Explanation

In the first example there is one true positive, one false positive and one false negative, so both ratios are $1/2$. In the second the model raises no alerts at all: precision is undefined (reported as $0$) and recall is $0$ because both real cases were missed.
