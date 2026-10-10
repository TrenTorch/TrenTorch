---
name: problem-55-linear-svm-hinge-loss
title: 'Linear SVM Hinge Loss'
tags: [problemset, classical-ml, svm]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'svm'
hint: 'mean of max(0, 1 - y*score)'
tools: [NumPy]
---

## Statement

Compute the mean hinge loss of a linear classifier. Labels `y` are in $\{-1,+1\}$ and `scores` are the real-valued model outputs.

Implement `solve(y,scores)`.

**Returns.** Return a non-negative Python float $\;\frac1n\sum_i\max(0,\,1-y_is_i)$.

### Examples

**Example 1**

Input:

```python
solve([1, -1, 1], [1.0, -1.0, -1.0])
```

Output:

```text
0.666667
```

**Example 2**

Input:

```python
solve([1, -1], [3.0, -0.5])
```

Output:

```text
0.25
```

## Theory

### The simple version

The hinge loss is what a support vector machine minimises. A prediction costs nothing if it is on the correct side of the boundary by a margin of at least 1; otherwise the cost grows linearly with how far inside the margin (or on the wrong side) it falls.

### The formula

$$\ell(y,s)=\max(0,\,1-ys)$$

### Why it matters

- Hinge loss is what an SVM minimises, and it only cares about points inside or beyond the margin.
- Correct points outside the margin cost exactly zero, which is why only support vectors matter.

### How it works

1. Multiply each label by its score to get the margin.
2. Loss $=\max(0,1-\text{margin})$.
3. Average.

### Worked example

Margins are $1\cdot1=1$, $(-1)(-1)=1$ and $1\cdot(-1)=-1$. The losses are $0$, $0$ and $2$, and their mean is $2/3=0.666667$.

## Explanation

The product $y\,s$ is positive when the score has the right sign, so $1-ys<0$ means a confident correct prediction (loss $0$). In the first example the three losses are $0$, $0$ and $2$ (the last prediction has the wrong sign), giving a mean of $2/3$.
