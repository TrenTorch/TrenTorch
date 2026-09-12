---
name: evaluation-classification-metrics
title: 'Precision, Recall, F1, ROC, AUC'
tags: [classical-ml, evaluation, classification-metrics]
difficulty: Intermediate
---

## Statement

### The problem, from first principles

`01-splitting-and-resampling` gives a clean way to get held-out predictions; it doesn't say how to judge them. Plain accuracy hides a lot: on a dataset that's 95% negative, predicting "negative" for everything scores 95% accuracy while catching zero positives. A metric that only counts "right vs. wrong" can't tell that apart from a genuinely useful classifier.

What's actually needed is a way to look at the *kinds* of mistakes a classifier makes — how many real positives it misses, how many negatives it wrongly flags — and, since most classifiers output a score rather than a hard `0`/`1`, a way to judge that whole range of possible decision thresholds at once rather than locking in just one.

### From theory to code

Implement `precision_recall_f1(labels, predictions)` for a fixed set of hard predictions, then `roc_curve(labels, scores)` and `auc(fpr, tpr)` for the threshold-swept view built from continuous scores. Theory below derives the confusion-matrix counts and the curve; here the job is just counting matches with boolean masks and applying the resulting formulas.

### Constraints

- `labels`, `predictions` in `precision_recall_f1`: `{0, 1}`-valued, same shape.
- Returns `(precision, recall, f1)`, each `0.0` if its denominator would be `0` (no positive predictions for precision, no actual positives for recall) rather than raising or returning `nan`.
- `scores` in `roc_curve`: continuous, higher means "more likely class 1."
- `roc_curve` returns `(fpr, tpr, thresholds)`, one entry per threshold tried: every distinct score value from highest to lowest, plus `+inf` (the threshold that classifies everything as `0`).
- `tpr`/`fpr` at each threshold are computed against the *total* actual positive/negative counts, fixed for the whole dataset — not against the current threshold's predicted counts.
- `auc(fpr, tpr)` must not assume `fpr` already arrives sorted ascending.

### Hints

Open one at a time. Each gives away a little more than the last.

<details>
<summary>Hint 1</summary>

`precision_recall_f1` only needs three boolean-mask counts: predicted 1 and actually 1, predicted 1 and actually 0, predicted 0 and actually 1. Everything else is arithmetic on those three numbers, with a zero-denominator guard.

</details>

<details>
<summary>Hint 2</summary>

For `roc_curve`, sweep every distinct score as a threshold, from highest to lowest, plus `+inf` at the start. At each threshold, `predictions = (scores >= threshold)`, then reuse the same TP/FP counting idea as `precision_recall_f1` — but divide by the fixed total positive/negative counts, not the counts among current predictions.

</details>

<details>
<summary>Hint 3</summary>

`roc_curve`'s natural order is descending by threshold, which isn't necessarily ascending `fpr`. `auc` needs to sort both arrays by `fpr` first, then integrate with the trapezoidal rule (`np.trapezoid`).

</details>

## Theory

### The simple version

Picture a spam filter. Flagging everything as spam catches every real spam message (perfect recall) but also buries every real email (terrible precision). Flagging nothing as spam is the opposite failure. Precision and recall each look at one *kind* of error in isolation — "of what I flagged, how much was really spam?" versus "of what was really spam, how much did I flag?" — and F1 is a single number that punishes an approach for winning one at the total expense of the other.

Because most classifiers output a continuous score rather than a hard decision, the threshold that turns "spam-ness score" into "flag or don't" can slide. The ROC curve traces out precision/recall's cousins (TPR, FPR) across every possible slide of that threshold, and AUC compresses the whole curve into one number.

### The formula

```text
                 actually 1        actually 0
predicted 1   true positive (TP)  false positive (FP)
predicted 0   false negative (FN) true negative (TN)

precision = TP / (TP + FP)   "of everything I predicted positive, how much really was?"
recall    = TP / (TP + FN)   "of everything that really was positive, how much did I catch?"
F1        = 2 * precision * recall / (precision + recall)

TPR (=recall) = TP / (TP + FN)     FPR = FP / (FP + TN)
ROC curve: (FPR, TPR) at every threshold, from "predict all 0" (0,0) to "predict all 1" (1,1)
AUC = area under that curve, via the trapezoidal rule
```

`AUC = 1.0` means some threshold separates the classes completely; `AUC = 0.5` means the classifier is exactly as good as random guessing, regardless of threshold — it measures how well-separated the two classes' scores are in general, not the quality of any one cutoff.

### How PyTorch actually implements this

Context only, untested by your submission: these are evaluation metrics, not `torch.nn` layers, so there's no forward pass equivalent. `torchmetrics.Precision`/`Recall`/`F1Score`/`AUROC` compute the same confusion-matrix-based quantities and curve; no baked numeric oracle from that library is used here.

## Explanation

`precision_recall_f1` counts the three confusion-matrix quantities directly with boolean masks — `true_positives = sum((predictions == 1) & (labels == 1))`, and similarly for `false_positives`/`false_negatives` — then applies the formulas above, each guarded against division by zero with a conditional expression (`0.0` when the relevant denominator is `0`, e.g. a model that never predicts `1` has undefined precision by the raw formula, `0.0` is the standard convention the test `test_precision_is_zero_when_no_positive_predictions` locks in).

`roc_curve` builds `thresholds = np.concatenate([[np.inf], np.sort(np.unique(scores))[::-1]])` — every distinct score value, descending, with `+inf` prepended so the very first threshold classifies nothing as positive (`fpr[0] == tpr[0] == 0.0`, checked by `test_roc_curve_endpoints`). At each threshold, `predictions = (scores >= threshold).astype(int)`, and `tpr_list`/`fpr_list` divide the resulting TP/FP counts by `n_positive`/`n_negative` — the *total* actual positive/negative counts, fixed once outside the loop — not by the current threshold's predicted counts, because TPR/FPR measure "what fraction of the true class did this threshold catch," which only makes sense against the true class totals.

`auc` calls `order = np.argsort(fpr)` before integrating, since `roc_curve`'s natural order is by threshold descending, not necessarily ascending `fpr`. `np.trapezoid(tpr[order], fpr[order])` then integrates the area under the curve using the trapezoidal rule — connecting consecutive points with straight lines and summing the resulting trapezoids' areas. `tests.py`'s `test_matches_real_sklearn_roc_curve_and_auc_on_a_baked_dataset` pins this against a genuine `sklearn.metrics.roc_auc_score` value (`0.500805152979066`) computed offline, so the sort-then-integrate order isn't just a style choice — it's what makes the result match the real library.
