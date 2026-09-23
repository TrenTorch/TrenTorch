---
name: math-sampling-estimating-distribution
title: Sampling from a random variable and estimating its distribution
tags: [probability]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Every weight in a freshly-created neural network starts at a random value, drawn from some chosen distribution (a later question in Deep Learning: Training covers exactly which one, and why). Every dropout mask, every data augmentation, every train/test split shuffle, all of it is sampling: producing concrete numbers from a distribution you never see directly, only through the numbers it happens to hand you.

You can't inspect a distribution's true shape directly, you only ever get to see samples FROM it. So the practical skill this question builds is: draw samples reproducibly, then reconstruct an approximate picture of the distribution those samples came from, purely from the numbers themselves.

### From theory to code

Theory names the tool for reproducible sampling (a seeded random generator, not global mutable random state) and the tool for approximating a distribution's shape from samples (a histogram: bucket values into bins, count how many land in each).

Implement `sample_normal(mean, std, size, seed=None)` and `empirical_histogram(samples, bins=10)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Use `np.random.default_rng(seed)`, not the legacy `np.random.seed`/`np.random.normal` global-state functions.
- The same `seed` must always produce the same samples (reproducibility is the entire point).
- `empirical_histogram` returns `(counts, bin_edges)`, matching `np.histogram`'s own return shape.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.random.default_rng(seed)` returns a generator object. Call `.normal(...)` on that object, not on the `np.random` module directly.

</details>

<details>
<summary>Hint 2</summary>

`np.histogram` already does exactly the counting-into-buckets work this question describes, in one call.

</details>

## Theory

### The simple version

You can never directly observe "the distribution of adult heights", you only ever get to measure specific people. But measure enough people, sort their heights into buckets (5'0"-5'2", 5'2"-5'4", and so on), and count how many fall in each bucket, and the resulting bar chart starts to look like the true, underlying shape of "how heights are distributed", even though you never saw that shape directly.

### The formula

A **random variable** is a rule for producing numbers according to some distribution. **Sampling** means drawing concrete numbers from it. For a Normal (Gaussian) distribution with mean `mu` and standard deviation `sigma`, samples cluster around `mu`, with about 68% falling within one `sigma` of it, and about 95% within two.

Reproducibility matters: a **seeded** random generator produces the exact same sequence of "random" numbers every time it's given the same seed, essential for debugging (a bug that only appears with specific random weights needs to be reproducible to fix) and for fair comparisons between two training runs that should differ only in the thing you're actually testing, not in incidental randomness.

An **empirical histogram** approximates a distribution's shape from samples alone: divide the range of observed values into equal-width bins, count how many samples land in each, and the resulting bar heights approximate the distribution's true probability density, getting more accurate as the sample count grows.

### How PyTorch actually implements this

`torch.nn.init.normal_` (and every other weight-initialization scheme, Kaiming, Xavier, uniform) is exactly this question's `sample_normal`, applied to a real weight tensor at model-construction time, `linear`'s own README already flagged that real `nn.Linear` initializes its weights this way rather than at zero. Reproducibility in real PyTorch training runs is controlled via `torch.manual_seed`, which seeds PyTorch's own internal generator (a separate concern from NumPy's `default_rng` used here, but the identical idea): without it, two runs of the "same" experiment can silently diverge in every random weight, every dropout mask, and every data shuffle, making it impossible to tell whether a change in results came from your actual code change or just from different random luck.

## Explanation

`sample_normal` creates a fresh, seeded generator via `np.random.default_rng(seed)` and calls its `.normal(loc=mean, scale=std, size=size)` method, avoiding NumPy's legacy global random state entirely.

`empirical_histogram` calls `np.histogram(samples, bins=bins)` directly, which does the bucket-and-count work from Theory and returns exactly the `(counts, bin_edges)` pair this question's signature promises.
