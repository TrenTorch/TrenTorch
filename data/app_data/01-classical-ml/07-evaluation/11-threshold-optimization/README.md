---
name: evaluation-threshold-optimization
title: 'Threshold optimization for imbalanced classification'
tags: [classical-ml, evaluation, imbalanced-data]
difficulty: Intermediate
---

## Statement

Implement:

```python
def f1_metric(labels, predictions) -> float: ...
def optimize_threshold(labels, scores, metric_fn=f1_metric) -> tuple[float, float]: ...
```

- Reuse `02-classification-metrics`'s `precision_recall_f1`.

## Theory

Every classifier that outputs a probability or score (logistic regression's `sigmoid`, a tree's leaf fraction) needs a threshold to turn that score into an actual `0`/`1` decision, `predictions = scores >= threshold`. `0.5` is the default nearly every library reaches for, and it's a completely arbitrary choice, nothing about the model's math requires it.

`0.5` is a particularly bad default on **imbalanced** data: with, say, 5% positive examples, a model can predict "negative" for almost everything and still look reasonable at `0.5`, because there simply aren't many positive examples for a wrong threshold to visibly hurt. But `01-random-forest-majority-vote`'s core lesson (many opinions, cleanly combined, beat a single bad one) applies here too, in a sense: **the threshold itself is a hyperparameter**, exactly like `04-grid-search`'s `lr` or `depth`, and it can be swept and optimized the same way, against whatever metric actually matters for the problem (F1, balanced accuracy, or something task-specific), rather than left at a default that was never chosen with this dataset in mind.

```text
try every candidate threshold
   ↓ score = metric_fn(labels, scores >= threshold)
   ↓ keep the threshold with the best score
```

On a genuinely imbalanced dataset, the optimal threshold is very often well below `0.5`, catching more of the rare positive class (higher recall) is worth accepting somewhat more false positives, exactly the tradeoff `02-classification-metrics`'s precision/recall pair makes visible.

## Explanation

`f1_metric` is a one-line wrapper: call `precision_recall_f1(labels, predictions)` and return just the F1 value, the default `metric_fn` for `optimize_threshold`, useful because it balances precision and recall in one number rather than requiring the caller to pick just one to optimize.

`optimize_threshold` tries `np.unique(scores)`, every distinct score value the model actually produced (no reason to try a threshold that would give identical predictions to some nearby value that already appears in the data), and for each one, `predictions = (scores >= threshold).astype(int)`, `metric_fn(labels, predictions)`, tracking whichever threshold scores highest, the same "loop, evaluate, keep the best" pattern `04-grid-search`'s `grid_search` and `05-random-search`'s `random_search` use, applied to a single, continuous hyperparameter instead of a discrete grid or random draws.
