---
name: math-summarizing-distribution
title: "Summarizing a feature's distribution: mean, median, skew"
tags: [data-processing]
difficulty: Beginner
---

## Statement

### The problem, from first principles

Before training anything, a practitioner's first real look at a new feature is almost never a full plot, it's a handful of summary numbers that answer "what does this column roughly look like," fast. Mean and median (`02-expectation-variance`, `02-imputing-missing-values`) each answer "where's the center," but they can disagree, and when they disagree substantially, that disagreement itself is informative: it's the signature of a **skewed** distribution, one that's lopsided rather than symmetric.

This question builds the third piece of that quick-glance toolkit, skewness, a single number that quantifies exactly that lopsidedness, and packages all three (mean, median, skew, alongside std) into one summary a practitioner would actually reach for first.

### From theory to code

Theory defines skewness as the average CUBED z-score of every value (cubing, unlike variance's squaring, preserves sign, capturing which direction the distribution leans), and mean/median/std/skew together as the standard quick-summary bundle.

Implement `skewness(x)` first, then `summarize_distribution(x)`, which bundles it with `mean`, `median`, and `std`.

### Constraints

- `skewness` returns a plain `float`.
- `summarize_distribution` returns a dict with exactly the keys `"mean"`, `"median"`, `"std"`, `"skew"`.
- `summarize_distribution` must call `skewness`, not reimplement its formula inline.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

Compute z-scores first (`(x - mean(x)) / std(x)`), then cube them and average.

</details>

<details>
<summary>Hint 2</summary>

`summarize_distribution` is mostly a dict literal, `np.mean`, `np.median`, `np.std`, and a call to `skewness`.

</details>

## Theory

### The simple version

Household income in most countries is a classic example of a skewed distribution: most households cluster in a moderate range, but a long tail of very high earners stretches the mean upward, well above where "most" households actually sit (the median). If mean and median were close together, that would signal a roughly symmetric distribution instead, income evenly spread around its center with no dominant tail either way. Skewness is the number that captures exactly this: how lopsided a distribution is, and which direction it leans.

### The formula

```text
skew(x) = mean(((x - mean(x)) / std(x))^3)
```

Each value is converted to a z-score first (how many standard deviations from the mean), then CUBED (not squared, like variance) and averaged. Cubing matters specifically because it preserves sign: a value above the mean cubes to a positive number, a value below cubes to a negative one, symmetric distributions have these cancel out to (near) zero on average, while a long right tail (values far above the mean, few far below) leaves a net positive, and a long left tail leaves a net negative.

```text
skew > 0  -> long right tail (income-style distributions)
skew < 0  -> long left tail
skew ~= 0 -> roughly symmetric (a Normal distribution has skew exactly 0)
```

A quick summary combining `mean`, `median`, `std` (`02-expectation-variance`) and `skew` into one bundle is exactly the first thing a practitioner checks when looking at a new feature for the first time, before any plot: a large gap between mean and median, paired with a nonzero skew, immediately flags "this feature has a meaningful tail, standard techniques that assume roughly-symmetric data might need adjusting."

### How PyTorch actually implements this

`scipy.stats.skew` (the real-world tool for exactly this) and `pandas.Series.skew()` compute this identical formula (with a small technical variant, Fisher-Pearson's bias-corrected version, for small samples), used routinely during exploratory data analysis, before a single tensor is built. Skewed features are a genuinely common reason to apply a log transform (`torch.log`) before feeding data into a model, income, word frequencies, and many other real-world quantities are naturally right-skewed, and a log transform compresses that long tail, often making the transformed feature both easier to model and closer to the roughly-symmetric distributions many statistical assumptions (Gaussian noise, for instance) are built around.

## Explanation

`skewness` computes the mean and std, forms the z-score for every value, cubes each one, and averages, exactly the formula from Theory.

`summarize_distribution` returns a dict with `mean`, `median` and `std` computed directly via NumPy, and `skew` computed by calling the already-implemented `skewness` function.
