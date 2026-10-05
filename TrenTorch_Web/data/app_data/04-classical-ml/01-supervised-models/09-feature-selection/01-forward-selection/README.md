---
name: feature-selection-forward-selection
title: 'Forward selection with a model in the loop'
tags: [classical-ml, feature-selection, wrapper-methods, greedy-search, linear-regression]
difficulty: Intermediate
---

## Statement

### Let the model decide which feature to add next

A wrapper method judges a feature set by actually fitting a model on it. Forward selection starts from nothing and, at each step, adds the single feature that gives the best fit when combined with the features already chosen.

Implement `forward_selection(X, y, k)`. It returns the list of `k` selected column indices, in the order they were picked.

At each step, for every feature not yet chosen:

1. Fit ordinary least squares with an intercept on the chosen columns plus this one.
2. Score the fit by `R^2 = 1 - SS_res / SS_tot`. If `SS_tot` is zero, the score is `0.0`.

Pick the feature with the highest score. Ties go to the smallest index.

### Constraints

- `X` is 2-D with `d` columns, `y` has one value per row.
- `1 <= k <= d`, otherwise raise `ValueError`.
- Do not modify the inputs.

### Hints

<details>
<summary>Hint 1</summary>

Use `np.linalg.lstsq` on a design matrix with a column of ones prepended.

</details>

## Theory

Forward selection is greedy, so it can miss the best subset, but it needs only `k * d` fits instead of searching all subsets. Because `R^2` never decreases when a column is added, the score alone cannot decide when to stop. That is why the number of features is fixed in advance here, and in practice it is chosen with a validation set or a penalty such as AIC.

### Where this shows up in production

Stepwise feature selection for regression-based risk scores in lending and clinical models, where a small set of inputs must be explained to a regulator. It is also used when each feature has a collection cost at serving time, such as a paid data vendor or a sensor that must be installed.

### Using it to make decisions

Use it when you must cap the number of features for cost, latency or explainability, and you can afford roughly d times k model fits. Pick k from validation performance, not from training R², which always rises as features are added. Run the whole selection inside each cross-validation fold. If you select on the full data first and then cross-validate, the score is optimistic, and the gap is often large enough to ship a bad model.

### Pros and cons

**Pros:** it optimises the metric you actually care about, produces compact models, and is simple to implement and audit.

**Cons:** it is greedy, so it can miss the best pair of features that only works together. It is slow compared with filters, and when features are correlated the chosen set changes from one resample to the next, which makes the model look unstable to stakeholders.

## Explanation

The solution keeps a list of chosen indices. Each step evaluates every remaining candidate with a small `R^2` helper and keeps the first candidate that achieves the best strict improvement, which gives the smallest-index tie-break.
