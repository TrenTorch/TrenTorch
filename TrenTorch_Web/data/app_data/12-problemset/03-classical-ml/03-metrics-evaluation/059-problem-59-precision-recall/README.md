---
name: problem-59-precision-recall
title: 'Precision Recall'
tags: [problemset, classical-ml, metrics]
difficulty: Advanced
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'count TP, FP, FN; guard each division against a zero denominator'
tools: [NumPy]
---

## Statement

Compute precision and recall of binary predictions. Labels and predictions are 0/1 arrays of equal length; the positive class is `1`.

Implement `solve(y,pred)`.

**Returns.** Return a tuple `(precision, recall)`. Precision is $0.0$ if nothing was predicted positive, and recall is $0.0$ if there are no actual positives.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1, 0], [0, 1, 0, 1])
```

Output:

```text
(0.5, 0.5)
```

**Example 2**

Input:

```python
solve([1, 1, 0, 0], [0, 0, 0, 0])
```

Output:

```text
(0.0, 0.0)
```

## Theory

### The simple version

Precision asks: _of everything I flagged as positive, how much was really positive?_ Recall asks: _of everything that was really positive, how much did I catch?_ They pull in opposite directions: flagging more raises recall but usually lowers precision.

### The formulas

$$\text{precision}=\frac{TP}{TP+FP},\qquad \text{recall}=\frac{TP}{TP+FN}$$

### Why it matters

- Accuracy alone hides how a classifier fails; precision and recall separate false alarms from misses.
- Which one matters depends on the cost of each error.

### How it works

1. Count true positives, false positives and false negatives.
2. Precision $=TP/(TP+FP)$, recall $=TP/(TP+FN)$.
3. Use $0$ when a denominator is $0$.

### Worked example

Labels $(0,1,1,0)$ and predictions $(0,1,0,1)$: one true positive, one false positive and one false negative. Precision is $1/2$ and recall is $1/2$, so (0.5, 0.5).

## Explanation

The counts $TP,FP,FN$ come from comparing the two arrays element-wise. When a denominator is $0$ the ratio is undefined; returning `0.0` is the common convention and avoids NaNs. In the second example the model predicts no positives at all, so precision is $0$ by convention and recall is $0$ because both real positives were missed.
