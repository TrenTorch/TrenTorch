---
name: math-data-leakage
title: 'Data leakage: a feature that accidentally encodes the label'
tags: [data-processing]
difficulty: Advanced
---

## Statement

### The problem, from first principles

Imagine building a model to predict whether a hospital patient will be readmitted, and one of your "input" features happens to be `discharge_summary_mentions_followup_scheduled`, a note that only gets written AFTER a doctor already knows the patient's outcome. Train on this feature and you'll see suspiciously, almost impossibly good accuracy, because the model isn't predicting the future, it's reading an answer that was written down after the fact. This is **data leakage**: information that wouldn't actually be available at real prediction time has snuck into the training data, making the model look far better than it will ever perform in the real world.

`03-correlation-matrix`'s own Theory flagged exactly this trap in passing; this question builds the actual detection tool: an automatable, first-pass check that flags any feature suspiciously, almost implausibly correlated with the target, the numerical fingerprint leakage very often leaves behind.

### From theory to code

Theory reuses `03-probability/03-covariance-correlation`'s correlation, applied between every feature and the target specifically (not between features, `03-correlation-matrix`'s job), and flags anything above a high threshold as suspicious.

Implement `feature_target_correlations(x, target)` first, then `find_suspicious_features(x, target, threshold=0.95)` on top of it.

### Constraints

- `x` is `(num_samples, num_features)`, `target` is `(num_samples,)`.
- `find_suspicious_features` returns the INDICES of flagged features (an array of ints), not a boolean mask.
- `threshold` compares against absolute correlation (a suspiciously strong NEGATIVE correlation counts too).

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`feature_target_correlations` loops over each feature column, computing `correlation(x[:, i], target)` for each, and collects the results into an array.

</details>

<details>
<summary>Hint 2</summary>

`np.where(np.abs(correlations) > threshold)[0]` gives you exactly the indices where a condition holds.

</details>

## Theory

### The simple version

A hospital wants to predict which patients will be readmitted. One "feature" available in the dataset turns out to be a note a doctor only writes AFTER deciding a follow-up appointment is needed, which itself strongly implies they expect complications. Training on that feature makes the model look astonishingly accurate, because it isn't predicting anything, it's reading a note that already encodes the future outcome. The model would be useless the moment it's deployed: at real prediction time, that note doesn't exist yet.

### The formula

Data leakage's numerical fingerprint is often a suspiciously strong correlation between a feature and the target:

```text
feature_target_correlations[i] = correlation(x[:, i], target)
find_suspicious_features = indices where |feature_target_correlations| > threshold
```

A correlation with the target near `+1` or `-1` (much stronger than any single, honest feature usually manages) is a strong signal, though not proof, that the feature is somehow derived from or entangled with the target itself, rather than a genuine, independently-measured predictor. This exact numerical check is a real, standard first-pass audit step: not a substitute for actually understanding WHERE each feature comes from and WHEN it would be available at real prediction time, but a fast, automatable flag worth investigating before trusting a suspiciously good result.

Leakage takes many forms beyond this single-feature case: `04-feature-scaling`'s Theory already named one (fitting scaling parameters on test data), `12-nested-cross-validation` (Evaluation & Model Selection, Classical ML) covers a subtler structural version (hyperparameter search accidentally seeing test data through the back door of an improperly-nested cross-validation loop). What they all share: information that wouldn't genuinely be available at real prediction time somehow influenced training, producing evaluation numbers that look great but don't reflect real-world performance.

### How PyTorch actually implements this

There is no PyTorch API that detects data leakage, it is fundamentally a data-provenance problem (does this feature's value genuinely exist, unaltered, at the moment a real prediction would be made), not a modeling or numerical one. The practical discipline that prevents it: every feature's timestamp must be checked against the prediction target's timestamp (nothing computed AFTER the target's own outcome is known may be used as an input), and any preprocessing statistic (`04-feature-scaling`'s mean/std, `03-one-hot-encoding`'s category list) must be fit exclusively on training data, then applied unchanged to validation and test data, never refit on data the model will later be evaluated against. A model that performs suspiciously well during development, and noticeably worse after real deployment, is the single most common real-world symptom that leakage slipped through despite every automated check.

## Explanation

`feature_target_correlations` loops over every feature column and computes its correlation with `target` via the imported `correlation` function, collecting the results into a length-`num_features` array.

`find_suspicious_features` computes those correlations, then returns the indices (via `np.where`) where the absolute correlation exceeds `threshold`, flagging any feature suspiciously entangled with the target.
