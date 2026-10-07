---
name: problem-51-logistic-gradient
title: 'Logistic Gradient'
tags: [problemset, classical-ml, logistic-regression]
difficulty: Beginner
kind: problemset
relatedModule: 'part-classical-ml|Regression'
topic: 'logistic regression'
hint: 'residual = sigmoid(X @ w) - y; grad_w = X.T @ residual / n; grad_b = mean(residual)'
tools: [NumPy]
---

## Statement

Compute the gradient of the mean logistic (cross-entropy) loss for a linear model with weights `w`, evaluated at bias $b=0$. The prediction is $p=\sigma(Xw)$ and the labels `y` are 0/1.

Implement `solve(X,y,w)`.

**Returns.** Return a tuple `(grad_w, grad_b)`: a NumPy vector with one entry per feature, and a float. Both are averaged over the $n$ rows.

### Examples

**Example 1**

Input:

```python
solve([[1.0, 2.0], [3.0, 4.0]], [1, 0], [0.0, 0.0])
```

Output:

```text
([0.5, 0.5], 0.0)
```

**Example 2**

Input:

```python
solve([[1.0], [2.0], [3.0]], [0, 1, 1], [0.5])
```

Output:

```text
([-0.154233], 0.057031)
```

## Theory

### The simple version

Logistic regression predicts a probability $p=\sigma(z)$ from the linear score $z$. The remarkable fact is that the gradient of the cross-entropy loss with respect to the score is just _prediction minus label_, $p-y$. The gradient for each weight is that residual weighted by the matching feature.

### The formulas

$$p=\sigma(Xw),\qquad r=p-y,\qquad \nabla_w=\frac1n X^\top r,\qquad \frac{\partial L}{\partial b}=\frac1n\sum_i r_i$$

## Explanation

The sigmoid and its derivative cancel inside the cross-entropy, which is why no extra factors appear. At $w=0$ every prediction is $0.5$, so the gradient is simply the average of $(0.5-y_i)x_i$ (the first example). The bias gradient is the mean residual.
