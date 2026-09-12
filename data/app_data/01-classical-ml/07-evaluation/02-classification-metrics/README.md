---
name: evaluation-classification-metrics
title: 'Precision, Recall, F1, ROC, AUC'
tags: [classical-ml, evaluation, classification-metrics]
difficulty: Intermediate
---

## Statement

Implement:

```python
def precision_recall_f1(labels, predictions) -> tuple[float, float, float]: ...
def roc_curve(labels, scores) -> tuple[np.ndarray, np.ndarray, np.ndarray]: ...
def auc(fpr, tpr) -> float: ...
```

## Theory

Plain accuracy hides a lot: on a dataset that's 95% negative, predicting "negative" for everything scores 95% accuracy while catching zero positives. Precision, recall, and F1 look at the _kinds_ of mistakes a classifier makes, not just how many:

```text
                 actually 1        actually 0
predicted 1   true positive (TP)  false positive (FP)
predicted 0   false negative (FN) true negative (TN)

precision = TP / (TP + FP)   "of everything I predicted positive, how much really was?"
recall    = TP / (TP + FN)   "of everything that really was positive, how much did I catch?"
F1        = 2 * precision * recall / (precision + recall)   (harmonic mean of the two)
```

Precision and recall trade off against each other as the decision threshold moves, predicting `1` more readily (a lower threshold) catches more true positives (higher recall) but also more false positives (lower precision). The **ROC curve** plots this entire tradeoff: true positive rate (`TPR`, the same thing as recall) against false positive rate (`FPR = FP / (FP + TN)`), one point per possible threshold, from "predict everything negative" (`0, 0`) to "predict everything positive" (`1, 1`).

**AUC** (area under the ROC curve) compresses that whole curve into one number: `1.0` is a perfect classifier (there's some threshold that separates the classes completely), `0.5` is exactly as good as guessing randomly, no matter what decision threshold is chosen. A model's AUC doesn't depend on choosing any particular threshold at all, it measures how well-separated the two classes' scores are, in general.

## Explanation

`precision_recall_f1` counts the four confusion-matrix quantities directly with boolean masks (`(predictions == 1) & (labels == 1)`, summed), then applies the formulas above, guarded against division by zero (`0.0` when a denominator is `0`, e.g. a model that never predicts `1` has undefined precision by the raw formula, `0.0` is the standard convention).

`roc_curve` tries every distinct score value as a threshold (plus `+infinity`, "classify nothing as positive," the curve's starting point), from highest to lowest, `thresholds = [inf] + sorted(unique(scores), descending)`. At each threshold, `predictions = scores >= threshold`, and `tpr`/`fpr` divide by the _total_ actual positive/negative counts (`n_positive`, `n_negative`, fixed for the whole dataset), not by the current threshold's predicted counts, `tpr`/`fpr` measure "what fraction of the true class did this threshold catch," which only makes sense against the true class totals.

`auc` sorts by `fpr` first (`roc_curve`'s natural order is by threshold, descending, which isn't necessarily ascending `fpr`), then `np.trapezoid(tpr[order], fpr[order])` integrates the area under the curve using the trapezoidal rule, connecting consecutive points with straight lines and summing the resulting trapezoids' areas.
