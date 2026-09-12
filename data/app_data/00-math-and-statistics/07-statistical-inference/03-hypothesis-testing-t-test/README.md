---
name: math-hypothesis-testing-t-test
title: 'Hypothesis testing: a two-sample t-test from scratch'
tags: [probability]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Group A (a new website layout) averages 52 seconds on-page, group B (the old layout) averages 48 seconds. Is the new layout genuinely better, or would two random samples from the SAME underlying population, with no real difference at all, plausibly show a 4-second gap just from ordinary sampling noise? `01-confidence-interval` quantified uncertainty around ONE group's mean; a hypothesis test directly answers the "is this difference real" question for TWO groups, by asking exactly how surprising the observed gap would be if there were actually no true difference at all.

This is the formal machinery behind essentially every "does this change actually help" decision made with data: an A/B test comparing two website variants, a clinical trial comparing a drug to a placebo, an ML experiment comparing a new model architecture against a baseline, they're all, underneath, this exact same two-sample comparison.

### From theory to code

Theory builds Welch's t-test (the version that doesn't assume equal variance between groups, the safer, more commonly recommended default) from two pieces: a t-statistic measuring how many standard errors apart the two means are, and the Welch-Satterthwaite equation for the (non-integer) effective degrees of freedom needed to convert that statistic into a p-value.

Implement `welch_t_statistic(a, b)` and `welch_degrees_of_freedom(a, b)` first, then `two_sample_t_test(a, b)`, which combines them into a `(t_statistic, p_value)` pair.

### Constraints

- Do not assume equal variance between `a` and `b` (this is specifically Welch's t-test, not the classic Student's equal-variance version).
- `two_sample_t_test` computes a two-sided p-value.
- Use `scipy.stats.t.cdf` for the p-value lookup, not a hand-rolled approximation.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The t-statistic's numerator is just the difference of the two means; the denominator is a "combined standard error," `sqrt(var_a/n_a + var_b/n_b)`.

</details>

<details>
<summary>Hint 2</summary>

The two-sided p-value is `2 * (1 - stats.t.cdf(abs(t), df))`, the probability, under the "no real difference" assumption, of seeing a t-statistic at least this extreme in either direction.

</details>

## Theory

### The simple version

Flip a fair coin 10 times and get 7 heads, that's not shocking, fair coins do that sometimes. Flip it 10,000 times and get 7,000 heads, that WOULD be shocking, a fair coin essentially never does that. Hypothesis testing formalizes exactly this intuition for comparing two groups: assume, for the sake of argument, that there's NO real difference between them (the "null hypothesis"), then ask how surprising the ACTUALLY OBSERVED difference would be under that assumption. A small p-value means "very surprising if there were truly no difference", evidence the difference is real, not noise.

### The formula

Welch's t-statistic measures how many "combined standard errors" apart two sample means are:

```text
t = (mean(a) - mean(b)) / sqrt(var(a, ddof=1)/n_a + var(b, ddof=1)/n_b)
```

Larger `|t|` means the observed gap is large relative to how much noise you'd expect from sampling alone, more surprising under "no real difference."

Converting `t` into a p-value requires knowing which t-distribution to compare against, specifically its degrees of freedom, which Welch's version computes via the Welch-Satterthwaite equation (generally NOT a whole number, unlike the simpler equal-variance t-test):

```text
df = (var_a/n_a + var_b/n_b)^2
     / ( (var_a/n_a)^2/(n_a-1) + (var_b/n_b)^2/(n_b-1) )
```

The two-sided p-value is then the probability of seeing a t-statistic at least this extreme, in either direction, if the null hypothesis (no real difference) were true:

```text
p = 2 * (1 - t_distribution_cdf(|t|, df))
```

A small p-value (conventionally, `< 0.05`) is interpreted as evidence AGAINST the null hypothesis, "this difference is unlikely to be pure noise." A large p-value does NOT prove the groups are the same, it just means the data doesn't provide strong evidence they differ, an important, commonly-misstated distinction: "failing to find evidence of a difference" is not the same claim as "proving there is no difference."

### How PyTorch actually implements this

`scipy.stats.ttest_ind(a, b, equal_var=False)` computes exactly this test (this question's implementation matches it, entry for entry, on real data). This is the standard tool for asking "is my new model architecture ACTUALLY better than the baseline, or did it just get lucky on this particular evaluation run": run both models several times with different random seeds, collect each run's final metric, and run a t-test between the two sets of results, exactly the same comparison this question builds from first principles, applied to model comparison instead of website layouts. `04-a-b-testing` (the next question in this track) is the direct, product-focused specialization of this exact same statistical machinery.

## Explanation

`welch_t_statistic` computes both means and unbiased (`ddof=1`) variances, then `(mean_a - mean_b) / sqrt(var_a/n_a + var_b/n_b)`, exactly Theory's formula.

`welch_degrees_of_freedom` computes the same variances and applies the Welch-Satterthwaite formula directly.

`two_sample_t_test` calls both, then computes the two-sided p-value via `2 * (1 - stats.t.cdf(abs(t_statistic), df))`, returning `(t_statistic, p_value)`.
