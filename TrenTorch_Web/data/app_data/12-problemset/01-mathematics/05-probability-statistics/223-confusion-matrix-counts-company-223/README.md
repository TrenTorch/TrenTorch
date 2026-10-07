---
name: confusion-matrix-counts-company-223
title: 'confusion-matrix-counts — Salesforce case'
tags: [problemset, classical-ml, metrics-and-evaluation, salesforce]
difficulty: Beginner
kind: problemset
relatedModule: 'part-mathematics|Probability & Statistics'
topic: 'Probability & Statistics'
caseCompany: 'Salesforce'
hint: 'four boolean-mask counts, returned as (tp, tn, fp, fn)'
tools: [NumPy]
---

## Statement

Salesforce-inspired model evaluation dashboard receives predicted and true binary labels from a validation run. You need to compute the confusion-matrix counts so the team can derive the metrics shown to model owners.

Compare the true labels `y` with the predicted labels `p` (both 0/1) and count the four outcomes. The tuple order is **(TP, TN, FP, FN)**.

Implement `solve(y,p)`.

**Returns.** Return a tuple of four Python integers `(tp, tn, fp, fn)`.

### Examples

**Example 1**

Input:

```python
solve([1, 0, 1, 0], [1, 0, 0, 1])
```

Output:

```text
(1, 1, 1, 1)
```

**Example 2**

Input:

```python
solve([1, 1, 1, 0], [1, 1, 0, 0])
```

Output:

```text
(2, 1, 0, 1)
```

## Theory

### The simple version

Every prediction is either right or wrong in one of two ways. A _false positive_ is an alarm that should not have been raised; a _false negative_ is a case that was missed. The four counts together give every metric: accuracy, precision, recall, specificity and more.

### The definitions

$$TP=\#[y=1,p=1],\;TN=\#[y=0,p=0],\;FP=\#[y=0,p=1],\;FN=\#[y=1,p=0]$$

## Explanation

In the first example each combination occurs exactly once. Note the order of the returned tuple, which differs from the matrix layout $[[TN,FP],[FN,TP]]$ used elsewhere. The four counts always add up to the number of samples.
