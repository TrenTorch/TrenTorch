---
name: math-feature-scaling
title: 'Feature scaling: standardization vs min-max normalization'
tags: [data-processing]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

A dataset with "age in years" (roughly 0-100) and "income in dollars" (roughly 0-500,000) hands a model two features on wildly different scales. Gradient descent (`04-gd-step`) takes one learning rate for ALL parameters, but a small step for the income-weight moves the prediction a huge amount (income values are huge), while the same-sized step for the age-weight barely does anything, the loss surface is a long, thin, badly-conditioned valley instead of a nice round bowl, and training crawls or oscillates. Distance-based methods (`01-knn`, later in Classical ML) have an even more direct problem: "distance" between two points is dominated entirely by whichever feature happens to have the largest raw numeric range, regardless of which feature actually matters more.

Feature scaling fixes both problems by putting every feature on a comparable numeric footing before training ever starts. This question implements the two standard approaches and sets up the exact "fit on training data only" discipline `04-data-leakage`, later in this track, treats as a hard requirement, not a suggestion.

### From theory to code

Theory gives two rescaling formulas, standardization (mean 0, std 1) and min-max normalization (squashed into `[0, 1]`), and both need to work in two modes: computing scaling parameters fresh from a dataset, or REUSING previously-computed parameters on new data.

Implement `standardize(x, mean=None, std=None)` and `min_max_normalize(x, min_val=None, max_val=None)` against that reasoning. The signatures and docstrings are already in the editor.

### Constraints

- Both functions compute per-column (per-feature) statistics, `axis=0`, not a single global statistic across the whole array.
- If the relevant parameters (`mean`/`std`, or `min_val`/`max_val`) are supplied, use them as-is, don't recompute from `x`.
- Both return a 3-tuple: `(scaled_x, param1, param2)`, so a caller can reuse the returned parameters later.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`np.mean(x, axis=0)` and `np.std(x, axis=0)` give one number per column, exactly the per-feature statistics both formulas need.

</details>

<details>
<summary>Hint 2</summary>

Check `if mean is None` (and similarly for the other parameters) before computing, if a caller already supplied a value, don't overwrite it.

</details>

## Theory

### The simple version

Comparing a person's age (say, 30) to their income (say, $60,000) as if they were on the same scale is meaningless, a "distance" calculation that treats them equally would be almost entirely dominated by the income number, age would barely register at all. Rescaling both onto a common footing, so a "typical" swing in age looks numerically comparable to a "typical" swing in income, is what feature scaling does, letting a model, or a distance calculation, treat every feature fairly regardless of its original units.

### The formula

**Standardization** ("z-scoring") rescales each column to have mean 0 and standard deviation 1:

```text
standardized = (x - mean) / std
```

using `03-probability/02-expectation-variance`'s own mean and std, computed per column.

**Min-max normalization** rescales each column into the fixed range `[0, 1]`:

```text
normalized = (x - min) / (max - min)
```

The two have different personalities: standardization is unbounded (a new data point outside the original range still produces a sensible, if large, standardized value) and is less sensitive to the exact min/max (which can be noisy, especially with outliers); min-max normalization guarantees a fixed range but is sensitive to outliers (one huge value stretches the whole scale, compressing everything else toward 0).

Both formulas need a **fit vs. apply** distinction that matters enormously in practice: compute `mean`/`std` (or `min`/`max`) from the TRAINING data only, then apply those SAME fixed numbers to scale validation and test data too. Recomputing statistics separately on test data (letting test data "see" its own mean/std) is a subtle form of data leakage, `04-data-leakage`, later in this track, names this exact mistake directly. This is exactly why both functions here accept optional pre-computed parameters instead of always deriving them fresh.

### How PyTorch actually implements this

`sklearn.preprocessing.StandardScaler`/`MinMaxScaler` implement precisely this fit/transform split as an explicit API: `.fit(X_train)` computes and stores the parameters, `.transform(X_test)` applies the STORED parameters (never recomputing from `X_test`), exactly the `mean`/`std` reuse pattern this question's signature is built around. Inside a real PyTorch model, `torch.nn.BatchNorm1d`/`2d` performs an analogous rescaling automatically, layer by layer, with a crucial refinement: during training it uses the CURRENT mini-batch's statistics, but it also accumulates a running average of those statistics specifically so that, at inference time (`model.eval()`), it uses the fixed, accumulated statistics rather than recomputing from whatever batch happens to be running through it, the exact same "fit once, apply consistently" discipline this question's `mean=None`/`std=None` parameters set up by hand.

## Explanation

`standardize` computes `mean`/`std` via `np.mean`/`np.std` (per column, `axis=0`) only when not supplied, applies `(x - mean) / std`, and returns the scaled result along with whichever `mean`/`std` were used, so a caller can reuse them.

`min_max_normalize` follows the identical structure with `np.min`/`np.max` and the min-max formula in place of standardization's.
