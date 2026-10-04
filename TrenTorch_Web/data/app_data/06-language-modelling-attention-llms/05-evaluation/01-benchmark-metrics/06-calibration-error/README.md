---
name: lm-calibration-error
title: Calibration & ECE
tags: [evaluation, calibration, uncertainty]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

Accuracy says how often a model is right. **Calibration** says whether its confidence means anything: when a model says "90% sure", is it right about 90% of the time? An overconfident model is dangerous because users trust the stated confidence. To measure it, group predictions into confidence bins and compare, in each bin, the average confidence with the actual accuracy. The **expected calibration error** (ECE) is the average gap, weighted by how many predictions fall in each bin. Language models are famously well calibrated before fine-tuning and often overconfident afterwards, which makes this a standard post-training diagnostic.

### From theory to code

Implement `expected_calibration_error` and `brier_score`.

### Constraints

- `confidences` is an array in `(0, 1]` holding the model's probability for its predicted answer. `correct` is a 0/1 array of the same length.
- Use `n_bins` equal-width bins over `[0, 1]`: bin `b` covers `(b / n_bins, (b + 1) / n_bins]` (upper edge included). A confidence exactly `0` goes in the first bin.
- `expected_calibration_error(confidences, correct, n_bins=10)` returns `sum over non-empty bins of (bin size / n) * |accuracy - mean confidence|`.
- `brier_score(probs, outcomes)` is the mean of `(probs - outcomes) ** 2` for binary outcomes.
- Return Python floats.

### Hints

<details>
<summary>Hint 1</summary>

Bin index is `ceil(conf * n_bins) - 1`, clipped to `[0, n_bins - 1]`.

</details>

<details>
<summary>Hint 2</summary>

Skip empty bins so you never divide by zero.

</details>

## Theory

### The simple version

A weather forecaster is calibrated if, among all the days they said "70% chance of rain", it rained on about 70 of every 100. Calibration does not care whether the forecaster is smart, only whether the numbers can be believed.

### The formula

$$
\text{ECE} = \sum_{b=1}^{B}\frac{|S_b|}{n}\,\big|\,\text{acc}(S_b) - \text{conf}(S_b)\,\big|, \qquad
\text{Brier} = \frac{1}{n}\sum_i (p_i - y_i)^2
$$

A perfectly calibrated model has ECE 0, but so does a model that always predicts the base rate, so calibration is always read alongside accuracy.

### How this is done in practice

Reliability diagrams plot accuracy against confidence per bin, and ECE is its one-number summary. Fixes include temperature scaling on a held-out set, label smoothing and ensembling. ECE depends on the number of bins, so reports state `n_bins`.

## Explanation

Predictions are assigned to bins with a ceiling operation so that the upper edge is inclusive, then each non-empty bin contributes its weighted confidence-accuracy gap. The Brier score is included because it is a proper scoring rule with no binning at all, a useful cross-check.
