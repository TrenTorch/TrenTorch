---
name: adam-one-step-company-239
title: 'adam-one-step — Coinbase case'
tags: [problemset, dl-training-theory, optimizers, coinbase]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Coinbase'
hint: 'm_hat = g, v_hat = g^2 on the first step; theta - lr*m_hat/(sqrt(v_hat)+eps)'
tools: [NumPy]
---

## Statement

Coinbase-inspired fraud-model training service is validating an Adam optimizer implementation before running longer experiments. You need to perform the first Adam update (all moments start at zero) from the supplied parameters, gradient, learning rate and hyperparameters.

Perform the **first** Adam update, starting from zero moments ($m_0=v_0=0$, step $t=1$): $m=(1-\beta_1)g$, $v=(1-\beta_2)g^2$, bias-correct them, and return $\theta-\eta\,\hat m/(\sqrt{\hat v}+\varepsilon)$.

Implement `solve(theta,g,lr,b1,b2,eps)`.

**Returns.** Return the updated parameters as a NumPy array.

### Examples

**Example 1**

Input:

```python
solve([1.0, 2.0], [0.5, -1.0], 0.1, 0.9, 0.999, 1e-8)
```

Output:

```text
[0.9, 2.1]
```

**Example 2**

Input:

```python
solve([1.0], [0.0], 0.1, 0.9, 0.999, 1e-8)
```

Output:

```text
[1.0]
```

## Theory

### The simple version

Adam keeps running averages of the gradient (direction) and of the squared gradient (typical size) and divides one by the square root of the other, so each parameter moves by roughly the learning rate regardless of how large its gradient is. At the very first step the running averages are biased toward their zero starting value; bias correction undoes that.

### The first step

$$\hat m_1=\frac{(1-\beta_1)g}{1-\beta_1}=g,\qquad \hat v_1=g^2,\qquad \theta_1=\theta_0-\eta\,\frac{g}{|g|+\varepsilon}$$

## Explanation

After correction the moments are exactly $g$ and $g^2$, so the first update is about $\eta\cdot\operatorname{sign}(g)$ for every parameter, whatever its gradient size: in the first example both parameters move by $0.1$. A zero gradient moves nothing (second example).
