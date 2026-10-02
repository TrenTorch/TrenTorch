---
name: math-generating-functions
title: Moment & Probability Generating Functions
tags: [calculus, series, probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

A distribution can be described by its probabilities, or by a handful of summary numbers such as the mean and variance. A generating function is a third description that packs the whole distribution into one function. It looks like a strange thing to do until it pays off: the mean, the variance and every higher moment fall out of the function by differentiating it, and the distribution of a sum of independent variables, which normally needs a convolution, falls out by multiplying two functions. This question builds both flavours for discrete variables and uses them to read off moments and to add random variables.

### From theory to code

Implement `mgf(values, probabilities, t)`, the moment generating function, then `pgf(probabilities, z)`, the probability generating function, then `mgf_moments(mgf_fn, step)`, the first two moments recovered by differentiating a moment generating function numerically at zero, then `pgf_mean_variance(probabilities)`, the mean and variance from the derivatives of a probability generating function at one, then `sum_distribution(p, q)`, the distribution of the sum of two independent variables. The signatures and docstrings are already in the editor.

### Constraints

- `values` is a 1D array-like of the outcomes a variable can take, and `probabilities` is a 1D array-like of the same length that is non-negative and sums to `1.0`.
- `mgf` accepts `t` as a float or an array and returns the same shape. `mgf(values, probabilities, 0)` is exactly `1.0`.
- For `pgf`, the variable takes the values `0, 1, 2, ...` and `probabilities[k]` is `P(X = k)`. `z` is a float or an array.
- `mgf_moments` receives a function `mgf_fn(t)` of one float, and returns `(first_moment, second_moment)` as floats, estimated with central finite differences around `t = 0` using the given `step`.
- `pgf_mean_variance` returns `(mean, variance)` as floats and must not first compute the mean as a plain weighted average of the values. It works from the derivatives of the generating function at `z = 1`.
- `sum_distribution` takes two probability lists as in `pgf` and returns the probability list for `X + Y`, of length `len(p) + len(q) - 1`.

### Hints

<details>
<summary>Hint 1</summary>

Both functions are expectations of something raised to the value: `e^{t x}` for the moment generating function and `z^x` for the probability generating function. An expectation is a probability-weighted sum.

</details>

<details>
<summary>Hint 2</summary>

Differentiating `E[e^{tX}]` once at `t = 0` brings down one factor of `X` and leaves `E[X]`. A central difference `(M(h) - M(-h)) / (2h)` approximates that derivative, and `(M(h) - 2M(0) + M(-h)) / h**2` approximates the second.

</details>

<details>
<summary>Hint 3</summary>

The first and second derivatives of a polynomial `sum(p_k z^k)` at `z = 1` are `sum(k p_k)` and `sum(k (k - 1) p_k)`. The variance needs the second derivative, plus the mean, minus the mean squared.

</details>

<details>
<summary>Hint 4</summary>

Multiplying two polynomials multiplies their coefficient lists as a convolution, and the product of two probability generating functions is the generating function of the sum.

</details>

## Theory

### The simple version

A generating function is a clothesline for a sequence of numbers: instead of listing the numbers, you hang each one on a successive power of a variable and carry the whole sequence around as one expression. For a probability distribution the numbers are the probabilities, and the clothesline lets you do things with the whole distribution at once, like adding two random variables by multiplying their clotheslines.

### The formulas

The **moment generating function** of a random variable $X$ is

$$
M_X(t) = \mathbb{E}\!\left[e^{tX}\right] = \sum_x p(x)\, e^{tx}
$$

Expanding $e^{tx}$ as a power series (`02-taylor`) shows where the name comes from:

$$
M_X(t) = \sum_{n=0}^{\infty} \frac{t^n}{n!}\,\mathbb{E}[X^n]
$$

so the $n$-th moment is the $n$-th derivative at zero, $\mathbb{E}[X^n] = M_X^{(n)}(0)$.

For a variable that takes the values $0, 1, 2, \dots$ the **probability generating function** is

$$
G_X(z) = \mathbb{E}\!\left[z^X\right] = \sum_{k=0}^{\infty} P(X = k)\, z^k
$$

It is a power series whose coefficients are the probabilities themselves, so the distribution can be read straight off it. Its derivatives at $z = 1$ give factorial moments:

$$
G_X'(1) = \mathbb{E}[X], \qquad G_X''(1) = \mathbb{E}[X(X-1)], \qquad \mathrm{Var}(X) = G_X''(1) + G_X'(1) - G_X'(1)^2
$$

### Sums of independent variables

If $X$ and $Y$ are independent, then $z^{X+Y} = z^X z^Y$ and the expectation of a product of independent quantities is the product of expectations, so

$$
G_{X+Y}(z) = G_X(z)\,G_Y(z), \qquad M_{X+Y}(t) = M_X(t)\,M_Y(t)
$$

Multiplying two polynomials multiplies their coefficients as a **convolution**, so the probabilities of the sum are the convolution of the two probability lists:

$$
P(X + Y = n) = \sum_{k} P(X = k)\,P(Y = n - k)
$$

Two generating functions that agree everywhere describe the same distribution, which is how these tools are used to prove that a sum of independent normals is normal or that a sum of independent Poissons is Poisson.

### Where this shows up in machine learning

Chernoff and Hoeffding bounds, the workhorses behind generalization guarantees, are built from the moment generating function: bounding $\mathbb{E}[e^{tX}]$ and then optimizing over $t$ bounds the chance of a rare large deviation. Convolving distributions is how the distribution of a total (a sum of event counts, a sum of per-token losses) is computed exactly rather than by simulation.

### How NumPy/PyTorch actually implements this

`np.convolve(p, q)` computes the coefficient list of the product of two generating functions, which is `sum_distribution`. `np.polynomial.polynomial.polyval(z, p)` evaluates a probability generating function and `np.polynomial.polynomial.polyder` differentiates it. `scipy.stats` exposes `.moment(n)` and `.mean()` on every distribution. Differentiating a moment generating function numerically is rarely done in practice, because step sizes small enough for a good derivative eventually lose digits to rounding.

## Explanation

`mgf` converts `values` and `probabilities` to arrays and returns `sum(p * exp(t * x))` with `t` broadcast against the values, so a scalar `t` gives a scalar and an array gives an array. `pgf` does the same with `z ** k` for `k = 0, 1, 2, ...`, which is a polynomial evaluation with the probabilities as coefficients. `mgf_moments` takes a central difference for the first derivative and a second central difference for the second derivative around zero, both of which have error proportional to `step` squared; the second moment is the second derivative because every power of `t` in the expansion carries a `1 / n!`. `pgf_mean_variance` forms `G'(1)` and `G''(1)` directly from `k * p_k` and `k * (k - 1) * p_k`, then assembles the variance as `G''(1) + G'(1) - G'(1)**2`, which is the identity from Theory. `sum_distribution` is a single `np.convolve`, since the product of the two generating functions is exactly a convolution of their coefficient lists.
