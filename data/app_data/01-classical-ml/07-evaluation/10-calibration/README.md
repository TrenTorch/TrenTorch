---
name: evaluation-calibration
title: 'Calibration: does a predicted probability of 0.8 mean 80% of the time'
tags: [classical-ml, evaluation, calibration]
difficulty: Advanced
---

## Statement

### The problem, from first principles

`02-classification-metrics`'s AUC only ever asks about ranking: does class 1 tend to score higher than class 0. It's silent on whether a specific predicted number, `0.8`, means what it claims to mean. That question, whether a stated probability is a trustworthy frequency, is its own separate property called **calibration**, and a model can be excellent by AUC while being badly calibrated: its `0.8` might really behave like `0.95`, or like `0.6`, when you look at what actually happens to everyone it assigned that number to.

This is worth checking whenever the probability itself gets used downstream, not just the predicted class, sizing a bet, setting an insurance premium, deciding how urgently to flag a medical result. All of those need `0.8` to genuinely mean "about 80% of the time," not just "more likely than not."

### From theory to code

Theory groups predictions by their predicted probability and compares, within each group, the average predicted probability against the actual fraction that were class 1. Implement `reliability_diagram(labels, probabilities, n_bins)`, which builds exactly those per-bin numbers, and `expected_calibration_error(labels, probabilities, n_bins)`, which compresses the whole diagram into the single weighted-average gap Theory describes.

### Constraints

- `labels`: `{0, 1}`-valued, same shape as `probabilities`.
- `probabilities`: predicted `P(class=1)`, values in `[0, 1]`.
- `reliability_diagram` returns `(bin_confidences, bin_accuracies, bin_counts)`, each shape `(n_bins,)`.
- Bins are equal-width over `[0, 1]`; a sample with probability `p` falls in bin `i` if `edges[i] <= p < edges[i+1]`, except the last bin, which also includes `p == 1.0` exactly.
- An empty bin (`bin_counts[i] == 0`) leaves `bin_confidences[i]` and `bin_accuracies[i]` at `0`, not `nan` and not skipped.
- `expected_calibration_error` returns a single float: the sample-count-weighted average of `|accuracy - confidence|` across bins, `0` for perfect calibration.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

The mean of a `{0, 1}`-valued array is exactly the fraction of entries that are `1`. That's not a coincidence you need a separate formula for, it's exactly what "actual fraction of class 1 in this bin" already is.

</details>

<details>
<summary>Hint 2</summary>

`np.linspace(0, 1, n_bins + 1)` gives the bin edges. Every bin except the last uses `edges[i] <= p < edges[i+1]`; the last bin needs `<=` on both ends, or a probability of exactly `1.0` falls into no bin at all.

</details>

<details>
<summary>Hint 3</summary>

Guard the per-bin mean behind `if bin_counts[i] > 0`. Since `expected_calibration_error` weights each bin by `bin_count / n_total`, an empty bin's leftover `0` confidence/accuracy contributes weight `0` regardless, no special-casing needed downstream.

</details>

## Theory

### The simple version

Imagine a weather forecaster who says "80% chance of rain" on 100 different days. If it actually rained on about 80 of those days, the forecaster is well-calibrated for that number. If it only rained on 30 of them, "80%" was really more like "30%" in disguise, even if the forecaster was, on those 100 days, still right more often than not about which way to guess. A reliability diagram runs this same check across every probability a model ever outputs, grouped into buckets.

### The formula

For each of `n_bins` equal-width bins over `[0, 1]`:

```text
confidence_i = mean(probabilities in bin i)   # what the model claimed
accuracy_i   = mean(labels in bin i)          # what actually happened
count_i      = number of samples in bin i
```

A perfectly calibrated model has `confidence_i == accuracy_i` for every non-empty bin, plotting one against the other traces the diagonal `y = x`.

```text
ECE = sum over bins of (count_i / n_total) * |accuracy_i - confidence_i|
```

`0` exactly when every non-empty bin's confidence matches its accuracy.

### How PyTorch actually implements this

PyTorch itself has no built-in calibration function; this is the same computation scikit-learn's `sklearn.calibration.calibration_curve` performs (`reliability_diagram`'s `bin_confidences`/`bin_accuracies` are exactly its `prob_pred`/`prob_true`), and `tests.py`'s `test_matches_real_sklearn_calibration_curve_on_a_baked_dataset` bakes in that exact library's output on a fixed dataset (generated once, offline, per the comment in the test) as a genuine cross-check, not an invented number.

## Explanation

`reliability_diagram` in `solution.py` builds `bin_edges = np.linspace(0.0, 1.0, n_bins + 1)`, then loops `i` over `range(n_bins)`. For each bin it builds a boolean mask: `(probabilities >= lower) & (probabilities < upper)` for every bin except the last, and `(probabilities >= lower) & (probabilities <= upper)` when `i == n_bins - 1`, so a probability of exactly `1.0` still lands somewhere instead of falling outside every bin. `bin_counts[i] = in_bin.sum()`, and only `if bin_counts[i] > 0` does it set `bin_confidences[i] = probabilities[in_bin].mean()` and `bin_accuracies[i] = labels[in_bin].mean()`, leaving an empty bin's two values at their initial `0`.

`expected_calibration_error` calls `reliability_diagram` to get all three arrays, computes `weights = bin_counts / n_total` where `n_total = probabilities.shape[0]`, and returns `float(np.sum(weights * np.abs(bin_accuracies - bin_confidences)))`, exactly the weighted-average gap from Theory. Because an empty bin's `weights[i]` is `0`, its leftover `bin_confidences[i] == bin_accuracies[i] == 0` never contributes anything to the sum, which is why `reliability_diagram` doesn't need `nan` or a separate empty-bin branch. `tests.py`'s `test_confidence_and_accuracy_are_not_swapped` pins down that `bin_confidences` comes from `probabilities.mean()` and `bin_accuracies` from `labels.mean()`, not the other way around, a mistake that would otherwise be numerically silent whenever the two happen to be close.
