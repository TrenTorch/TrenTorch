---
name: math-expectation-variance
title: Expectation and variance from a sample
tags: [probability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

"What's the average test score" and "how spread out were the scores" are two different questions about the same list of numbers, and they're both estimates: you're using the students who actually took the test to guess something about "students in general," a quantity you can never observe directly. The average of your actual data is your best guess at the expectation; how far the data typically strays from that average is your best guess at the variance.

The subtlety worth catching early: there are two slightly different ways to compute "typical spread" from a sample, and using the wrong one for the wrong purpose silently biases every downstream calculation that depends on it, standard errors, confidence intervals, t-tests, all built later in this curriculum.

### From theory to code

Theory gives the mean as a direct average, and variance as average squared deviation from that mean, with one adjustable parameter (`ddof`) controlling which of the two standard divisors gets used.

Implement `sample_mean(x)` and `sample_variance(x, ddof=0)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- `x` is a 1D array of numeric samples.
- `sample_variance` must respect `ddof`: `ddof=0` divides by `n`, `ddof=1` divides by `n-1`.
- Both functions return a plain Python `float`.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.mean` and `np.var` already exist and already accept a `ddof` argument, you are wrapping them, not deriving the formulas from a loop.

</details>

<details>
<summary>Hint 2</summary>

Don't hardcode `ddof=0` inside your implementation, pass the parameter straight through to `np.var`.

</details>

## Theory

### The simple version

Ask ten random people their height and average the results: that average is your best guess at "the average height of everyone," even though you only measured ten people. Now ask "how much do heights vary": measure how far each of your ten people's heights sits from that average, square those distances (so a height 3 inches off counts the same whether it's 3 inches too tall or too short), and average the squared distances. That's variance, "typical squared distance from the average."

### The formula

The **sample mean** estimates a distribution's expectation:

```text
mean(x) = (1/n) * sum(x_i)
```

The **sample variance** estimates its variance, the average squared deviation from the mean:

```text
variance(x) = (1/D) * sum((x_i - mean(x))^2)
```

where `D` is either `n` (dividing by the sample count directly, `ddof=0`) or `n - 1` (Bessel's correction, `ddof=1`). The `n-1` version exists because using the SAME sample to compute both the mean and the variance systematically underestimates the true variance, the sample mean is, by construction, the point closest to your own data, so deviations measured from it are slightly smaller than deviations from the true (unknown) population mean would be. Dividing by `n-1` instead of `n` exactly corrects that bias, on average. `np.var`'s default is `ddof=0` (a common source of quiet mismatches with `np.std(x, ddof=1)`-style code elsewhere), so `04-statistical-inference`'s confidence intervals and hypothesis tests, later in this curriculum, explicitly need to specify `ddof=1` for a statistically correct unbiased estimate.

### How PyTorch actually implements this

`torch.var` mirrors this exact `ddof`/`correction` distinction (`correction=1` is PyTorch's modern default, matching the statistically unbiased convention, unlike NumPy's `ddof=0` default), and `torch.nn.BatchNorm1d`/`2d` internally computes a running mean and variance over each mini-batch using exactly these formulas, then uses them to normalize activations, one of the most common places "which variance convention" quietly matters in a real training loop: BatchNorm's running statistics (accumulated with `ddof=0`-style biased estimates, matching how the original paper defines it) and a manually-computed "unbiased" variance for reporting purposes are not interchangeable, and mixing them up produces subtly wrong normalization at inference time.

## Explanation

`sample_mean` wraps `np.mean(x)`, the direct average.

`sample_variance` wraps `np.var(x, ddof=ddof)`, passing the caller's `ddof` straight through rather than hardcoding either convention, so the same function serves both the biased and unbiased use cases from Theory.
