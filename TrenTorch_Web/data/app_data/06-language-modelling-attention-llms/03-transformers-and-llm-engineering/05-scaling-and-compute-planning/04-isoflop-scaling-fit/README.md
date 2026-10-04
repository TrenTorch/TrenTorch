---
name: lm-isoflop-scaling-fit
title: Compute-Optimal Scaling Fits
tags: [scaling-laws, curve-fitting, chinchilla]
difficulty: Advanced
---

## Statement

### The problem, from first principles

For a fixed compute budget you can train a small model on many tokens or a large model on few. Plotting the final loss against model size for one budget (an **IsoFLOP curve**) gives a U-shape: too small underfits, too large is undertrained. The bottom of the U is the compute-optimal model size for that budget. Repeating this for several budgets gives pairs of (budget, optimal size), and the relationship is a power law `N_opt = a * C^b`, which is a straight line on log-log axes. Fitting this line is how scaling-law papers extrapolate to budgets too large to run. Two small fits are needed: a parabola for each IsoFLOP curve and a line for the power law.

### From theory to code

Implement `isoflop_optimum` and `fit_power_law`.

### Constraints

- `isoflop_optimum(params, losses)`: fit a quadratic `loss = a * x**2 + b * x + c` with `x = ln(params)` by least squares (`np.polyfit`, degree 2) and return the minimizing size `exp(-b / (2 * a))`. Require `a > 0` and raise `ValueError` otherwise.
- `fit_power_law(x, y)`: fit `ln y = ln a + b * ln x` by least squares and return `(a, b)` with `a = exp(intercept)`.
- Inputs are NumPy arrays of positive numbers with enough points for the fits.

### Hints

<details>
<summary>Hint 1</summary>

`np.polyfit(np.log(x), np.log(y), 1)` returns `[slope, intercept]`.

</details>

<details>
<summary>Hint 2</summary>

For the quadratic, the vertex is at `-b / (2a)` in log space.

</details>

## Theory

### The simple version

For every fuel budget there is an ideal balance between engine size and distance driven. Mark the ideal balance for several budgets, draw a line through the marks and you can predict the ideal engine for a budget you have never spent.

### The formula

$$
x = \ln N,\quad L(x) \approx a x^2 + b x + c \;\Rightarrow\; N^\ast = e^{-b/(2a)}, \qquad
N^\ast(C) = \alpha\, C^{\beta}
$$

In the Chinchilla analysis the fitted exponent is close to $0.5$: doubling compute should grow model size and data by about $\sqrt 2$ each.

### How this is done in practice

The two approaches in Hoffmann et al. (IsoFLOP profiles and parametric fits) agree on the exponent, and later work refined the constants. The recipe is cheap, but only as reliable as the small-scale runs behind it, which is why papers report fit uncertainty.

## Explanation

Quadratic fits locate the minimum without needing a run exactly at the optimum, and the power-law fit is a straight line in log space. Synthetic data generated from a known law gives tests that must recover the exact constants.
