---
name: gradient-check-one-parameter-company-250
title: 'gradient-check-one-parameter — Google case'
tags: [problemset, dl-core, backpropagation, google]
difficulty: Intermediate
kind: problemset
relatedModule: 'part-deep-learning|Optimization'
topic: 'Optimization'
caseCompany: 'Google'
hint: '(f(x + h*e0) - f(x - h*e0)) / (2h), compared with analytic[0]'
---

## Statement

Google-inspired optimization team is debugging a custom differentiable component whose analytical gradient may be wrong. You need to compute a numerical finite-difference gradient for one parameter so the team can compare it with the implementation.

Estimate the derivative of the function `f` with respect to the **first** coordinate of `x` by a centred finite difference, $\dfrac{f(x+h e_1)-f(x-h e_1)}{2h}$, and compare it with the claimed analytic derivative `analytic[0]`. `f` takes an array and returns a scalar; `h` defaults to $10^{-5}$.

Implement `solve(f, x, analytic, h=1e-5)`.

**Returns.** Return a tuple `(numeric, analytic, abs_error)` of Python floats.

Estimate the derivative of the function `f` with respect to the **first** coordinate of `x` by a centred finite difference, $\dfrac{f(x+h e_1)-f(x-h e_1)}{2h}$, and compare it with the claimed analytic derivative `analytic[0]`. `f` takes an array and returns a scalar; `h` defaults to $10^{-5}$.

Implement `solve(f, x, analytic, h=1e-5)`.

**Returns.** Return a tuple `(numeric, analytic, abs_error)` of Python floats.

### Examples

**Example 1**

Input:

```python
solve(lambda v: float(np.sum(v ** 2)), [1.5], [3.0])
```

Output:

```text
(3.0, 3.0, 1.96532e-11)
```

**Example 2**

Input:

```python
solve(lambda v: float(np.sum(v ** 2)), [1.5], [2.0])
```

Output:

```text
(3.0, 2.0, 1.0)
```

## Theory

### The simple version

When you write the backward pass of a layer by hand, bugs hide easily. A gradient check compares your analytic gradient with a numerical one obtained by nudging one parameter up and down and watching how the output changes. If the two agree to several digits, the formula is almost certainly right.

### The formula

$$\frac{\partial f}{\partial x_1}\approx\frac{f(x+he_1)-f(x-he_1)}{2h}$$

### Why it matters

- A hand-written derivative can be wrong in a way that no test of the forward pass will reveal.
- Nudging one parameter and watching the output gives a derivative you can trust to compare against.

### How it works

1. Evaluate $f$ at $x+he_1$ and $x-he_1$.
2. Divide the difference by $2h$.
3. Compare with the analytic value.

### Worked example

For $f(x)=x^2$ at $x=1.5$: $(1.50001^2-1.49999^2)/(2\cdot10^{-5})=3.0000$, the analytic value $3$, and the absolute error is about $2\cdot10^{-11}$: (3.0, 3.0, 1.96532e-11).

## Explanation

The centred difference has error of order $h^2$, much smaller than the one-sided difference with error of order $h$. In the first example the derivative of $x^2$ at $1.5$ is $3$ and the check reports a tiny error; in the second a wrong claimed gradient of $2$ is flagged by an error of about $1$. Too small an $h$ eventually loses accuracy to floating-point cancellation.
