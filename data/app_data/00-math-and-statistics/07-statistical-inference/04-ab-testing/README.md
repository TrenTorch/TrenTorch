---
name: math-ab-testing
title: 'A/B testing: is the difference between two groups real or noise'
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A website shows 1,000 visitors the old checkout button, 120 buy. It shows 1,000 different visitors a new button design, 150 buy. Is the new design genuinely better, or would two random 1,000-visitor samples from a page with NO real change plausibly land 30 conversions apart just from chance? This is the exact question `03-hypothesis-testing-t-test` answered for continuous measurements (like page-load times); A/B testing is the same question, specialized to CONVERSION RATES, proportions, not continuous numbers, which needs a slightly different formula.

This is quite possibly the single most common real-world application of statistical hypothesis testing: nearly every product decision informed by data ("did the new feature increase signups," "did the redesign hurt checkout completion") ultimately reduces to exactly this comparison.

### From theory to code

Theory pools both groups' conversion counts into one combined rate (the correct approach under the assumption both groups truly share the same underlying rate, the null hypothesis being tested), uses it to compute a standard error, and converts the observed gap into a z-statistic and two-sided p-value.

Implement `conversion_rate(conversions, visitors)` first, then `two_proportion_z_test(conversions_a, visitors_a, conversions_b, visitors_b)` on top of it.

### Constraints

- Uses the POOLED proportion (combining both groups) for the standard error, not each group's own rate separately.
- Returns a two-sided `(z_statistic, p_value)` pair.
- Uses `scipy.stats.norm.cdf` for the p-value (a Normal approximation is standard and appropriate here, unlike the t-distribution `03-hypothesis-testing-t-test` needed for small continuous samples).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)`, treating both groups as one combined sample for the purpose of estimating the shared rate under the null hypothesis.

</details>

<details>
<summary>Hint 2</summary>

The standard error uses the pooled proportion twice: `sqrt(p_pooled * (1 - p_pooled) * (1/visitors_a + 1/visitors_b))`.

</details>

## Theory

### The simple version

Two coins are flipped 1,000 times each. Coin A lands heads 120 times, coin B lands heads 150 times. If both coins were secretly identical (equally likely to land heads), how surprising would a 30-flip gap actually be, given ordinary coin-flipping randomness? If it's genuinely surprising (very unlikely to happen by chance alone), that's evidence the coins really are different. If it's not that surprising (well within the range random chance alone would produce), the gap could just be noise. A/B testing asks precisely this question about two website variants' conversion rates instead of two coins' heads counts.

### The formula

```text
conversion_rate = conversions / visitors

p_pooled = (conversions_a + conversions_b) / (visitors_a + visitors_b)
SE = sqrt(p_pooled * (1 - p_pooled) * (1/visitors_a + 1/visitors_b))
z = (rate_a - rate_b) / SE
p_value = 2 * (1 - normal_cdf(|z|))
```

Pooling matters: under the null hypothesis being tested ("both variants have the SAME true conversion rate"), the best estimate of that single shared rate comes from combining BOTH groups' data, not treating each group's own observed rate as if it were already known to be correct (`03-hypothesis-testing-t-test`'s Welch's test, by contrast, deliberately does NOT pool variances, because it's testing means where equal variance isn't assumed; A/B testing's pooling is a different, specifically-appropriate choice for the proportion case, since the null hypothesis itself claims one shared rate).

The same interpretation caveats from `03-hypothesis-testing-t-test` apply directly: a small p-value is evidence the difference is unlikely to be pure noise, it is not proof of causation on its own (`03-correlation-matrix`'s warning), and a large p-value means "not enough evidence of a difference," never "proof there is no difference." A genuinely important practical point this formula doesn't enforce on its own: the sample sizes need to be decided BEFORE running the test (a proper "power analysis"), repeatedly peeking at results and stopping as soon as `p < 0.05` happens to appear ("p-hacking") inflates the false-positive rate far above the nominal 5%, one of the most common real-world statistical mistakes in A/B testing practice.

### How PyTorch actually implements this

A/B testing is a product-analytics and statistics discipline (`scipy.stats`, `statsmodels.stats.proportion.proportions_ztest`, or a dedicated experimentation platform), entirely upstream of any PyTorch model. Where it DOES intersect with ML directly: comparing two model variants' business-relevant outcomes (does model A or model B produce a higher user click-through rate, in a live, randomized deployment) uses exactly this test, and comparing two models' offline evaluation METRICS across repeated runs uses `03-hypothesis-testing-t-test`'s continuous-measurement version instead, the choice between the two tests hinges entirely on whether the outcome being compared is a proportion (convert or not) or a continuous number (a loss value, an accuracy score).

## Explanation

`conversion_rate` returns `conversions / visitors` directly.

`two_proportion_z_test` computes each group's conversion rate, pools both groups' totals into `p_pooled`, computes the standard error from that pooled value, forms the z-statistic from the difference in observed rates divided by that standard error, and converts it to a two-sided p-value via `scipy.stats.norm.cdf`.
