---
name: math-confidence-interval
title: Confidence interval for a sample mean
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`07-maximum-likelihood-estimation`'s `mle_normal_mean` gives you ONE number, the sample mean, as your best guess at the true population mean. But a single number hides an important fact: that guess is uncertain, a different sample of the same size would almost certainly give a slightly different mean. A confidence interval makes that uncertainty explicit: instead of "the average is 100," it says "the average is likely somewhere between 94 and 106," a genuinely more honest and more useful statement, especially when a decision hinges on how confident you actually are.

This is the tool that turns "here's a number" into "here's a number, and here's how much I'd trust it," essential whenever a sample is small, or a decision (does this new feature actually help users? is this new drug better?) needs to account for the possibility that an observed difference is just sampling noise.

### From theory to code

Theory needs the standard error of the mean (how much sample means themselves vary) and a critical value from the t-distribution (which correctly widens the interval for small samples, where a plain Normal approximation would be overconfident).

Implement `standard_error_of_mean(x)` first, then `confidence_interval_mean(x, confidence=0.95)` on top of it.

### Constraints

- `standard_error_of_mean` uses `ddof=1` (the unbiased/Bessel-corrected std), `02-expectation-variance`'s convention for estimating from a sample.
- `confidence_interval_mean` uses the t-distribution (`scipy.stats.t.ppf`), not a fixed z-value, so it stays valid for any sample size.
- Returns a `(lower, upper)` tuple.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`standard_error_of_mean` is `np.std(x, ddof=1) / np.sqrt(len(x))`, one line.

</details>

<details>
<summary>Hint 2</summary>

`stats.t.ppf((1 + confidence) / 2, df=len(x) - 1)` gives the t-distribution's critical value for a two-sided interval at the requested confidence level.

</details>

## Theory

### The simple version

Poll 30 random voters and 60% say they'll vote yes on a proposal. Poll a DIFFERENT 30 voters from the same population, and you might get 55%, or 65%, pure sampling variation, not because opinions actually changed. A confidence interval quantifies exactly that wobble: instead of reporting a single number as if it were exact, it reports a range wide enough that, if you repeated this whole polling process many times, the TRUE population value would fall inside your reported range roughly (say) 95% of the time.

### The formula

The **standard error of the mean** measures how much a sample mean itself varies from sample to sample (distinct from `std(x)`, which measures how much the raw DATA varies):

```text
SEM = std(x, ddof=1) / sqrt(n)
```

A confidence interval for the true mean, using the t-distribution (the correct choice for any sample size, and especially important for small ones):

```text
t_critical = t-distribution's critical value at the target confidence level, with (n-1) degrees of freedom
margin     = t_critical * SEM
interval   = (mean - margin, mean + margin)
```

A "95% confidence interval" has a precise, easy-to-misstate meaning: if you repeated the entire sampling-and-interval-construction process many times, about 95% of the resulting intervals would contain the true population mean. It does NOT mean "there's a 95% probability the true mean is in THIS particular interval" (the true mean is a fixed, unknown number, not a random variable; the interval itself is what varies from sample to sample). The t-distribution (rather than a Normal/z-distribution) is used specifically because it has heavier tails for small `n`, correctly widening the interval to account for the extra uncertainty in estimating `std` from a small sample; as `n` grows large, the t-distribution converges to the Normal distribution and the two approaches agree.

### How PyTorch actually implements this

Confidence intervals belong to the statistical-analysis stage of ML work, not training itself: `scipy.stats` (as used directly in this question) or `statsmodels` are the standard tools, used to report uncertainty around a model's evaluation metric (is a 2% accuracy improvement over a baseline real, or within the noise a different test set might have produced?), exactly the question `04-a-b-testing` (the next question in this track) formalizes for comparing two groups directly. PyTorch itself has no confidence-interval utility, by the time a metric reaches a PyTorch training loop, it's a single number; wrapping that number in a confidence interval is a downstream statistical analysis step, typically done by running an experiment multiple times (different seeds, different data splits) and treating each run's result as one sample from the "true" distribution of outcomes.

## Explanation

`standard_error_of_mean` computes `np.std(x, ddof=1) / np.sqrt(len(x))` directly.

`confidence_interval_mean` computes the sample mean and `standard_error_of_mean`, looks up the t-distribution's critical value via `stats.t.ppf((1 + confidence) / 2, df=n-1)`, multiplies it by the standard error to get the margin, and returns `(mean - margin, mean + margin)`.
