---
name: math-maximum-likelihood-estimation
title: Maximum likelihood estimation for a simple distribution
tags: [probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`06-likelihood-vs-probability`'s `likelihood_curve` swept a grid of candidate means and evaluated each one, then you could squint at a plot and guess where the peak was. That's fine for one parameter and a hand-picked grid, but it doesn't scale, doesn't give an exact answer, and doesn't generalize to distributions with several parameters at once (mean AND std together).

Maximum likelihood estimation (MLE) is the principled version of "find where the likelihood curve peaks": instead of searching a grid, use calculus, set the derivative of the (log-)likelihood to zero and solve, to get an exact, closed-form answer directly. For a Normal distribution, this turns out to have a remarkably simple, familiar answer.

### From theory to code

Theory works in log-space (summing log-densities rather than multiplying raw densities, for numerical stability) and derives closed-form MLE formulas for a Normal distribution's mean and standard deviation by setting derivatives to zero. Implement the log-space objective first (so you can numerically verify the closed forms against it), then the two closed-form estimators directly.

Implement `negative_log_likelihood_normal(x, mean, std)`, `mle_normal_mean(x)` and `mle_normal_std(x)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `negative_log_likelihood_normal` works in log-space (sum of `log(density)`), not `-log(product of densities)`.
- `mle_normal_mean` and `mle_normal_std` are closed-form (no search, no calls to `negative_log_likelihood_normal`).
- `mle_normal_std` divides by `n` (the biased estimator), not `n - 1`, Theory explains why MLE gives this specific version.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`log(a * b * c) = log(a) + log(b) + log(c)`. Turn the product from `joint_density` into a sum of logs instead.

</details>

<details>
<summary>Hint 2</summary>

The MLE for the mean of a Normal distribution turns out to be exactly the plain sample average, no surprise formula needed.

</details>

## Theory

### The simple version

Imagine trying dozens of candidate "true averages" for a dataset and, for each one, asking "how likely would my actual data have been, if this were the true average?" The candidate that makes your actual, already-observed data look MOST likely is the maximum likelihood estimate. `06-likelihood-vs-probability` did exactly this by brute-force grid search; MLE does it with calculus instead, finding the peak exactly rather than approximately.

### The formula

Working with the log of the likelihood (rather than the raw product of densities) turns products into sums, both numerically safer (avoids underflow from multiplying many small numbers) and algebraically easier to differentiate:

```text
log_likelihood(mean, std | x) = sum_i(log(normal_pdf(x_i, mean, std)))
negative_log_likelihood = -log_likelihood
```

Since log is monotonic, maximizing the likelihood is equivalent to minimizing the negative log-likelihood, the form actually used here (and the form every loss function in `02-deep-learning-core` takes, cross-entropy and BCE are both negative log-likelihoods of their respective distributions).

Setting the derivative of the log-likelihood with respect to each parameter to zero and solving gives closed-form estimators for a Normal distribution:

```text
mle_mean = (1/n) * sum(x_i)                              -- the plain sample mean
mle_std  = sqrt((1/n) * sum((x_i - mle_mean)^2))          -- the BIASED standard deviation
```

The mean's MLE is exactly the ordinary average, no surprise. The std's MLE divides by `n`, not `n - 1`: `02-expectation-variance`'s Bessel's correction exists specifically to counteract a bias that MLE, by its own derivation, does not correct for, MLE optimizes purely for "what explains my exact observed data best," and that criterion alone does not care about being unbiased across many hypothetical repeated samples, which is a different (and, for many practical purposes, more important) goal.

### How PyTorch actually implements this

Training a neural network by minimizing cross-entropy or MSE loss IS maximum likelihood estimation, just for a distribution implicitly defined by the network's output rather than a simple Normal: minimizing MSE loss is exactly MLE under the assumption that residuals are Normally distributed with constant variance, and minimizing cross-entropy is exactly MLE under a categorical distribution defined by the softmax output. This is why `loss.backward()` on a well-chosen loss function isn't an arbitrary heuristic, it's gradient-based MLE, computing the same "which parameters make the observed data most likely" answer this question derives in closed form for the much simpler single-Normal case, but via numerical optimization instead of an exact formula (since a neural network's parameters don't admit one).

## Explanation

`negative_log_likelihood_normal` sums `log(normal_pdf(x_i, mean, std))` over every observation and negates, the log-space, numerically-safe version of the negative joint density.

`mle_normal_mean` returns `np.mean(x)`, the closed-form MLE derived in Theory.

`mle_normal_std` computes the mean first, then the root-mean-square deviation from it (`sqrt(mean((x - mean)^2))`), the biased closed-form MLE for standard deviation, dividing by `n` rather than `n - 1`.
