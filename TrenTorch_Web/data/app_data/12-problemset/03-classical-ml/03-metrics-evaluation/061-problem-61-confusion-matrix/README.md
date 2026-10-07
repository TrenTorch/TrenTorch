---
name: problem-61-confusion-matrix
title: 'Confusion Matrix'
tags: [problemset, classical-ml, metrics]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Metrics & Evaluation'
topic: 'metrics'
hint: 'four counts: (y==a)&(pred==b) for a,b in {0,1}'
tools: [NumPy]
---

## Statement

Build the $2\times2$ confusion matrix of binary labels and predictions. Rows are the **actual** class and columns are the **predicted** class.

Implement `solve(y,pred)`.

**Returns.** Return a $2\times2$ integer array `[[TN, FP], [FN, TP]]`.

### Examples

**Example 1**

Input:

```python
solve([0, 1, 1, 0], [0, 1, 0, 1])
```

Output:

```text
[[1, 1], [1, 1]]
```

**Example 2**

Input:

```python
solve([1, 1, 1, 0], [1, 1, 0, 0])
```

Output:

```text
[[1, 0], [1, 2]]
```

## Theory

### The simple version

The confusion matrix counts every combination of (what was true, what was predicted). The diagonal holds the correct predictions and the off-diagonal cells hold the two kinds of mistake. Metrics like precision, recall and accuracy are all read off this table.

### The layout

$$\begin{pmatrix}TN&FP\\FN&TP\end{pmatrix}$$

## Explanation

Each cell is a count of positions where a boolean condition on the labels and the predictions holds simultaneously. The four cells always add up to the number of samples.
