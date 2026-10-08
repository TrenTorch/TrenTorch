---
name: problem-56-svm-subgradient-step
title: 'SVM Subgradient Step'
tags: [problemset, classical-ml, svm]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-classical-ml|Classification'
topic: 'svm'
hint: 'active = y*(X@w) < 1; g = w - reg * sum(y_i x_i over active); return w - lr*g'
tools: [NumPy]
---

## Statement

Perform one linear-SVM subgradient step on the weights `w`. The objective is $\tfrac12\|w\|^2+\text{reg}\sum_i\max(0,\,1-y_i\,w\!\cdot\!x_i)$ with labels in $\{-1,+1\}$ and no bias. Examples whose margin $y_i\,w\!\cdot\!x_i$ is at least 1 contribute nothing to the hinge part.

Implement `solve(X, y, w, lr, reg)`.

**Returns.** Return the updated weights $w-\text{lr}\cdot g$ as a NumPy array, where $g=w-\text{reg}\sum_{i:\,y_iw\cdot x_i<1}y_ix_i$. The input `w` is not modified.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 0.0], [0.0, 1.0]], [1, -1], [0.0, 0.0], 0.1, 1.0)
```

Output:

```text
[0.1, -0.1]
```

**Example 2**

Input:

```python
solve([[2.0, 0.0]], [1], [1.0, 0.0], 0.1, 1.0)
```

Output:

```text
[0.9, 0.0]
```

## Theory

### The simple version

The hinge loss has a kink, so it has no gradient there, but any value between the left and right slopes is a valid _subgradient_. Gradient descent works with subgradients just as well. Only points that violate the margin push on the weights; points already on the right side with room to spare are ignored.

### The formulas

$$g=w-\text{reg}\sum_{i:\;y_i\,w\cdot x_i<1}y_i\,x_i,\qquad w_{\text{new}}=w-\text{lr}\cdot g$$

### Why it matters

- The hinge loss has a kink, but a subgradient still lets gradient descent train an SVM.
- Only points that violate the margin push on the weights, which is what makes SVMs sparse in the data.

### How it works

1. Find the points with margin $y\,w\cdot x<1$.
2. Subgradient $g=w-\text{reg}\sum y\,x$ over those points.
3. Step: $w-\text{lr}\cdot g$.

### Worked example

With $w=0$ both margins are $0<1$, so both points are active. $\sum yx=(1,0)-(0,1)=(1,-1)$, so $g=0-1\cdot(1,-1)=(-1,1)$ and the new weights are $0-0.1\cdot(-1,1)=[0.1, -0.1]$.

## Explanation

The term $w$ comes from the regulariser $\tfrac12\|w\|^2$ and shrinks the weights; the sum pulls them toward correctly classifying the violators. At margin exactly $1$ the hinge loss is not violated, so the strict inequality `margin < 1` is used. In the second example the margin is $2\ge1$, so only the shrinking term acts.
