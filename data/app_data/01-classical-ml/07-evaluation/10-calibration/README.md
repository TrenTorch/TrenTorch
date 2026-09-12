---
name: evaluation-calibration
title: 'Calibration: does a predicted probability of 0.8 mean 80% of the time'
tags: [classical-ml, evaluation, calibration]
difficulty: Advanced
---

## Statement

Implement:

```python
def reliability_diagram(labels, probabilities, n_bins=10) -> tuple[np.ndarray, np.ndarray, np.ndarray]: ...
def expected_calibration_error(labels, probabilities, n_bins=10) -> float: ...
```

## Theory

`02-classification-metrics`'s AUC only cares about the _ranking_ of predicted scores, does class 1 tend to score higher than class 0. It says nothing about whether a specific predicted probability means what it claims to mean. **Calibration** asks exactly that: among every sample the model said had probability `0.8` of being class 1, was roughly 80% of them actually class 1? A model can have excellent AUC (it ranks correctly) while being badly calibrated (its `0.8` might really mean `0.95`, or `0.6`), and calibration matters a great deal whenever the actual probability number gets used downstream, deciding how much money to bet, or how urgently to flag a medical result, not just which class to predict.

A **reliability diagram** checks this directly: group predictions into bins by their predicted probability (`0.0-0.1`, `0.1-0.2`, ..., `0.9-1.0`), and within each bin compare two numbers:

```text
confidence (this bin) = the average PREDICTED probability of samples in this bin
accuracy   (this bin) = the ACTUAL fraction of those samples that were really class 1
```

A perfectly calibrated model has `confidence == accuracy` in every bin, plotting one against the other traces the diagonal line `y = x`. Bins that fall below the diagonal are overconfident (predicted probability higher than the real frequency), bins above are underconfident.

**Expected Calibration Error (ECE)** compresses the whole reliability diagram into one number: the sample-count-weighted average gap between confidence and accuracy, across every bin. `0` is perfect calibration, larger means the model's stated probabilities are further from being trustworthy frequencies.

## Explanation

`reliability_diagram` builds `n_bins` equal-width bins over `[0, 1]` (`np.linspace(0, 1, n_bins+1)` for the edges), then for each bin, a boolean mask selects the samples whose probability falls in `[lower, upper)`, except the very last bin, which also includes `probability == 1.0` exactly (`<=` on the upper edge only there), otherwise a prediction of exactly `1.0` would fall outside every bin. `bin_confidences[i] = probabilities[in_bin].mean()` and `bin_accuracies[i] = labels[in_bin].mean()` (the mean of a `{0,1}` array is exactly the fraction that are `1`, no separate "compute a rate" step needed), computed only when the bin actually has samples (`bin_counts[i] > 0`), an empty bin's confidence/accuracy are left at `0`, meaningless but harmless since `expected_calibration_error` weights every bin by its own count, an empty bin contributes weight `0` regardless.

`expected_calibration_error` weights each bin by `bin_count / n_total`, its share of the whole dataset, and sums `weight * |accuracy - confidence|` across every bin, the sample-weighted average absolute gap Theory describes, `0` exactly when every non-empty bin's confidence matches its accuracy perfectly.
