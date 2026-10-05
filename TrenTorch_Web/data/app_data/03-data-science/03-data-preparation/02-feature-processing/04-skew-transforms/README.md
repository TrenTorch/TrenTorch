---
name: data-science-skew-transforms
title: Skew Transforms
tags: [data-science, feature-transformation]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`03-feature-scaling` puts features on a common scale, but scaling does not change a distribution's shape. Incomes, prices, counts and response times pile up near zero with a long tail of huge values, and in that shape a handful of extreme rows dominate the mean, the variance and any linear model's fit. A transform that compresses the tail, a logarithm or a power, pulls such a feature closer to symmetric and makes the extreme rows ordinary again. This question measures skewness and builds the transforms that reduce it.

### From theory to code

Implement `skewness(x)`, which measures how lopsided a sample is, then `log1p_transform(x)` and its inverse `inverse_log1p(z)`, then `box_cox(x, lam)`, a family of power transforms controlled by one number, then `best_box_cox_lambda(x, candidates)`, which picks the candidate that makes the sample most symmetric. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D float array. `skewness` returns the population skewness, the mean of cubed standardized values, `mean(((x - mean) / std) ** 3)` with `std` the population standard deviation. It returns `0.0` when `std` is zero.
- `log1p_transform(x)` returns `log(1 + x)` and raises `ValueError` if any value is negative. `inverse_log1p(z)` returns `exp(z) - 1`. Use `np.log1p` and `np.expm1`.
- `box_cox(x, lam)` requires every value to be strictly positive and raises `ValueError` otherwise. It returns `(x ** lam - 1) / lam` for `lam != 0` and `log(x)` for `lam == 0`.
- `best_box_cox_lambda(x, candidates)` returns the value in `candidates` whose Box-Cox transform has the smallest absolute skewness. On a tie it returns the earliest candidate in the list.
- Inputs must not be modified.

### Hints

<details>
<summary>Hint 1</summary>

A symmetric sample has skewness near zero. A long right tail gives a positive number, a long left tail a negative one.

</details>

<details>
<summary>Hint 2</summary>

`log1p` is used instead of `log` because it accepts zero, which counts, clicks and many amounts contain. It is also more accurate than `log(1 + x)` for tiny `x`.

</details>

<details>
<summary>Hint 3</summary>

Box-Cox with `lam = 1` is the identity up to a shift, `lam = 0.5` is a square-root-like transform and `lam = 0` is the logarithm, so trying a short list of lambdas covers the usual choices.

</details>

## Theory

### The simple version

Imagine plotting everyone's income on a ruler. Most people crowd near one end while a few billionaires stretch the ruler out to enormous lengths. A model that fits straight lines treats a billionaire as a huge lever and bends the line toward them. Measuring income on a logarithmic ruler, where each step multiplies instead of adds, squeezes the tail in so that the typical person and the extreme one sit within sensible distance of each other.

### The formula

The **skewness** of a sample is the average cubed standardized value:

$$
g_1 = \frac{1}{n}\sum_{i=1}^{n}\left(\frac{x_i - \bar{x}}{s}\right)^{3}
$$

Cubing keeps the sign, so a long right tail gives $g_1 > 0$, a long left tail gives $g_1 < 0$ and a symmetric sample gives about $0$.

The **log transform** and its inverse are

$$
z = \ln(1 + x), \qquad x = e^{z} - 1
$$

The **Box-Cox** family puts the logarithm and the power transforms in one formula for $x > 0$:

$$
x^{(\lambda)} = \begin{cases} \dfrac{x^{\lambda} - 1}{\lambda} & \lambda \neq 0 \\[2mm] \ln x & \lambda = 0 \end{cases}
$$

- $\lambda = 1$ leaves the shape alone, $\lambda = \tfrac12$ is a gentle compression and $\lambda = 0$ is the logarithm.
- The division by $\lambda$ makes the family continuous in $\lambda$: as $\lambda \to 0$ the first branch tends to $\ln x$.
- Choosing $\lambda$ by trying a grid and keeping the one with skewness closest to zero is a simple way to pick the transform.

### When a transform helps & when it does not

Linear and distance-based models, and anything that assumes roughly symmetric noise, benefit from de-skewed inputs. Tree-based models only look at the order of values, so a monotonic transform changes nothing for them. A transform learned on training data has to be applied unchanged to validation and test data, and predictions made in the transformed space need the inverse transform to come back to the original units.

### Zeros & negative values

The plain logarithm is undefined at zero and below, which is why `log1p` shifts by one. Box-Cox needs strictly positive input. The Yeo-Johnson transform extends the same idea to values of any sign, and adding a constant before a Box-Cox transform is the other common workaround.

### How NumPy/PyTorch actually implements this

`np.log1p` and `np.expm1` are the accurate log and inverse. `scipy.stats.skew` computes skewness (with an optional bias correction) and `scipy.stats.boxcox` chooses lambda by maximum likelihood instead of a grid. `sklearn.preprocessing.PowerTransformer(method='box-cox')` and `method='yeo-johnson'` fit lambda per column and expose `inverse_transform`. `sklearn.preprocessing.FunctionTransformer(np.log1p)` wraps the log transform inside a pipeline.

## Explanation

`skewness` standardizes the sample with the population standard deviation, cubes the result and averages, returning zero for a constant sample so there is no division by zero. `log1p_transform` rejects negative values and otherwise applies `np.log1p`, and `inverse_log1p` applies `np.expm1`, which round-trips exactly. `box_cox` checks positivity first, then picks the power branch or the logarithm depending on whether `lam` is exactly zero. `best_box_cox_lambda` computes the absolute skewness of the transform for each candidate and returns the first candidate with the smallest value, using `min` over the list in order so ties go to the earliest.
