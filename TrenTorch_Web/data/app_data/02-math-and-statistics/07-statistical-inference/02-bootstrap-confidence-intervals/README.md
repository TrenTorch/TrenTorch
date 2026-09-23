---
name: math-bootstrap-confidence-intervals
title: Bootstrap confidence intervals
tags: [probability]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-confidence-interval`'s t-based formula works specifically because the sample MEAN has a known, well-understood sampling distribution (the t-distribution). But what if you want a confidence interval for the MEDIAN? Or the standard deviation? Or some custom statistic entirely, like "the 90th percentile" or "the ratio of two other statistics"? None of these have the same convenient closed-form math the mean does. You'd need a different, hand-derived formula for every single statistic, if one even exists.

The bootstrap sidesteps this entirely with a strikingly simple idea: since you can't easily draw more real samples from the true population, resample from the one sample you DO have, treating it as a stand-in for the population itself. Do this thousands of times, computing your statistic of interest on each resample, and the SPREAD of those thousands of computed statistics directly tells you how uncertain your original estimate is, no closed-form formula required, for literally any statistic you can write a function for.

### From theory to code

Theory resamples the original data WITH replacement (same size as the original), computes the statistic of interest on each resample, and uses percentiles of the resulting distribution of statistics as the interval bounds.

Implement `bootstrap_resample(x, rng)` first, then `bootstrap_confidence_interval(x, statistic_fn, n_bootstrap=1000, confidence=0.95, seed=None)` on top of it.

### Constraints

- `bootstrap_resample` samples WITH replacement, same size as `x`.
- `bootstrap_confidence_interval` works for ANY `statistic_fn` (a function taking an array and returning a scalar), not just the mean.
- Uses `np.percentile` on the collected bootstrap statistics for the interval bounds.
- Same `seed` must produce the same interval (reproducibility).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`rng.choice(x, size=len(x), replace=True)` is exactly "with replacement, same size."

</details>

<details>
<summary>Hint 2</summary>

After collecting `n_bootstrap` computed statistics, the interval bounds are `np.percentile(statistics, (1-confidence)/2 * 100)` and `np.percentile(statistics, (1+confidence)/2 * 100)`.

</details>

## Theory

### The simple version

You have one bag of 100 marbles drawn from a much bigger population, and want to know how uncertain your estimate of "average marble weight" really is, without access to more real marbles. The bootstrap's trick: reach into YOUR bag, grab 100 marbles WITH replacement (so some get picked twice, others not at all, an entirely new "resample" the same size as your original), compute the average, and repeat this thousands of times. The spread of all those recomputed averages IS your uncertainty estimate, built entirely from the one sample you actually have, standing in as a proxy for the whole population you couldn't otherwise access.

### The formula

```text
bootstrap_resample(x)  = draw len(x) values from x, WITH replacement

repeat n_bootstrap times:
    resample = bootstrap_resample(x)
    bootstrap_statistics[i] = statistic_fn(resample)

confidence_interval = (
    percentile(bootstrap_statistics, (1 - confidence) / 2 * 100),
    percentile(bootstrap_statistics, (1 + confidence) / 2 * 100),
)
```

The key generalization over `01-confidence-interval`: `statistic_fn` can be ANYTHING, `np.mean`, `np.median`, `np.std`, a custom function computing a model's evaluation metric, anything at all that reduces an array to a single number. There's no closed-form math to derive separately for each one, the same resampling procedure works uniformly, at the cost of computation (thousands of resamples) instead of an exact formula.

The tradeoff worth knowing: bootstrap confidence intervals are an APPROXIMATION, their accuracy depends on `n_bootstrap` being large enough and the original sample being reasonably representative of the true population, unlike `01-confidence-interval`'s t-based interval, which has an exact mathematical guarantee for the mean specifically. In practice, for the mean, both methods usually agree closely on a reasonably-sized sample, the bootstrap's real value shows up for statistics without a known closed form.

### How PyTorch actually implements this

Bootstrap resampling is a standard technique for estimating uncertainty around ANY evaluation metric a model produces, model accuracy, F1 score, AUC, all lack simple closed-form confidence intervals the way the mean does, but bootstrapping the evaluation set (resample the TEST SET with replacement, recompute the metric on each resample, repeat) gives a genuine confidence interval for how much that metric might vary on a different test set drawn from the same underlying distribution. This is exactly how a practitioner answers "is this 2% accuracy improvement real, or could it just be noise from which particular test examples happened to be included," a direct, practical extension of the exact resampling idea implemented here, applied to whatever metric actually matters for a given model.

## Explanation

`bootstrap_resample` calls `rng.choice(x, size=len(x), replace=True)`, the direct with-replacement resample from Theory.

`bootstrap_confidence_interval` creates one seeded generator, draws `n_bootstrap` resamples, computes `statistic_fn` on each, and returns the `(1-confidence)/2` and `(1+confidence)/2` percentiles of the resulting array of statistics, exactly the percentile-based interval from Theory.
